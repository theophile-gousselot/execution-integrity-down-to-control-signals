#!/usr/bin/env python3
"""
riscv-elf-encryption.py

This script encrypts sections of an elf file (fct: encrypt_elf()). The algorithm used is ASCON.
"""

import os
import subprocess
import argparse
from ascon_fct import ascon_initialize, ascon_process_one_encryption, ascon_permutation, bytes_to_int, reverse_bytes, int_to_bytes, state2str, instr2fct7_3_opcode
from riscv_code import Code, zfint
from riscv_instruction import *


###### Arguments ######
parser = argparse.ArgumentParser(description="Encrypt an elf file.")
parser.add_argument(
    "elf_path",
    help="path to the elf file",
    type=str,
    nargs='?',
    const="",
    default="")
parser.add_argument(
    "-v",
    "--verbose",
    help="increase output verbosity",
    action="store_true")
parser.add_argument(
    "-b",
    "--pb_rounds",
    help="Rounds for pb",
    type=int,
    default=6)
parser.add_argument(
    "-c",
    "--control_signals",
    help="XOR control_signal to patch",
    type=str, nargs='?', const="", default="")
args = parser.parse_args()

cs_id_mode = "id" in args.control_signals
cs_ex_mode = "ex" in args.control_signals
if args.control_signals != '':
    CS_MODE = True
else:
    CS_MODE = False


###### Paths ######
ELF_PATH = args.elf_path
OBJ_PATH = os.path.dirname(ELF_PATH)
CS_PATH = f"SRC/PROGRAM_TOOLS/CONTROL_SIGNALS/control_signals.csv"
STATES_DEC_CSV_PATH = f"{ELF_PATH[:-4]}_states_dec.csv"
STATES_HEX_CSV_PATH = f"{ELF_PATH[:-4]}_states_hex.csv"
STATES_HEX_DBG_CSV_PATH = f"{ELF_PATH[:-4]}_states_hex_debug.csv"


###### Parameters ######
key = int(0x000102030405060708090a0b0c0d0e0f).to_bytes(
    16, 'big')  # get_random_bytes(keysize)
nonce = int(0x000102030405060708090a0b0c0d0e0f).to_bytes(
    16, 'big')  # get_random_bytes(16)


###### Global variables ######
S = [0, 0, 0, 0, 0]
k = len(key) * 8   # bits
a = 12   # rounds
b = args.pb_rounds   # rounds
rate = 4

###### Paths ######
CS_VECTOR_ARCH = {'alu_en': {'position': 7, 'width': 1, 'reset_val': 0b0, 'id_invalid_ex_ready': 0b1}, 'alu_operator': {'position': 0, 'width': 7, 'reset_val': 0b11, 'id_invalid_ex_ready': 0b11, 'ex_en':'alu_en'}}

DEASSERT_WE_AFFECTED_SIGNALS = ['alu_en']
EN_AFFECTED_SIGNALS = {
    'alu_en': ['alu_operator', 'alu_operand_a', 'alu_operand_b', 'alu_operand_c',
               'bmask_a_id', 'bmask_b_id', 'imm_vec_ext_id', 'alu_vec_mode',
               'is_clpx', 'alu_clpx_shift', 'is_subrot'],
    'mult_int_en': ['mult_operator', 'mult_sel_subword', 'mult_signed_mode',
                    'alu_operand_a', 'alu_operand_b', 'alu_operand_c', 'mult_imm_id'],
    'mult_dot_en': ['mult_operator', 'mult_dot_signed', 'alu_operand_a', 'alu_operand_b',
                    'alu_operand_c', 'is_clpx', 'clpx_shift_ex_o', 'clpx_img_ex_o'],
    'apu_en': ['apu_op', 'apu_lat', 'apu_operands', 'apu_flags', 'apu_waddr'],
    'regfile_we_id': ['regfile_waddr_id'],
    'regfile_alu_we_id': ['regfile_alu_waddr_id'],
    'data_req_id': ['data_we_id', 'data_type_id', 'data_sign_ext_id',
                    'data_reg_offset_id', 'data_load_event_id', 'atop_id']}

#if not 'data_req_id'  thus:  data_load_event_ex_o <= 1'b0;


mask = ''
for cs in CS_VECTOR_ARCH:
    if cs in DEASSERT_WE_AFFECTED_SIGNALS:
        mask += '0'*CS_VECTOR_ARCH[cs]['width']
    else:
        mask += '1'*CS_VECTOR_ARCH[cs]['width']
DEASSERT_WE_MASK = int(mask,2)


cs_vector_reset = ''
cs_vector_width = 0
for cs in CS_VECTOR_ARCH:
    cs_vector_reset += bin(CS_VECTOR_ARCH[cs]['reset_val'])[2:].zfill(CS_VECTOR_ARCH[cs]['width'])
    cs_vector_width += CS_VECTOR_ARCH[cs]['width']
CS_VECTOR_RESET = int(cs_vector_reset, 2)
CS_VECTOR_WIDTH = cs_vector_width
CS_VECTOR_ALL_ONE = (1 << 8) - 1


cs_vector_id_invalid_ex_ready = ''
mask_cs_vector_id_invalid_ex_ready = ''
for cs in CS_VECTOR_ARCH:
    if 'id_invalid_ex_ready' in CS_VECTOR_ARCH[cs].keys():
        cs_vector_id_invalid_ex_ready += bin(CS_VECTOR_ARCH[cs]['id_invalid_ex_ready'])[2:].zfill(CS_VECTOR_ARCH[cs]['width'])
        mask_cs_vector_id_invalid_ex_ready += '0'*CS_VECTOR_ARCH[cs]['width']
    else:
        cs_vector_id_invalid_ex_ready += '0'*CS_VECTOR_ARCH[cs]['width']
        mask_cs_vector_id_invalid_ex_ready += '1'*CS_VECTOR_ARCH[cs]['width']
CS_VECTOR_ID_INVALID_EX_READY = int(cs_vector_id_invalid_ex_ready, 2)
MASK_CS_VECTOR_ID_INVALID_EX_READY = int(mask_cs_vector_id_invalid_ex_ready, 2)


def make_mask_ex_en(cs_vector_id):
    mask = ''
    for cs in CS_VECTOR_ARCH:
        if not 'ex_en' in CS_VECTOR_ARCH[cs]:
            mask += '1'*CS_VECTOR_ARCH[cs]['width']
        else:
            en_ex = (cs_vector_id >> CS_VECTOR_ARCH[CS_VECTOR_ARCH[cs]['ex_en']]['position']) & 1
            mask += str(en_ex)*CS_VECTOR_ARCH[cs]['width']
    return int(mask, 2)

###### CMD/SECTION NAMES ######
READ_ELF_CMD = "/opt/corev/bin/riscv32-corev-elf-readelf -S "
FIRST_SECTION_EXECUTABLE = ".vectors"
FIRST_SECTION_TO_ENC = ".init"
LAST_SECTION_TO_ENC = ".text"


###### Toggle DEBUG #####
DEBUG = True

def log(string):
    '''
    Function to print debug info if DEBUG == True

    Parameters
    ----------
    string : str
        String to print if DEBUG == True
    '''
    if DEBUG:
        print(string)

###### Usefull functions #####

def find_sections_to_encrypt():
    '''
    For a program, determined the addresses of beginning and ending of encryption.
    This is performed by using the /opt/corev/bin/riscv32-corev-elf-readelf command.

    Parameters
    ----------

    Returns
    ----------
    address_start_encrypt : int
        The address of the beginning of the first section to be encrypted.
    address_stop_encrypt : int
        The address of the ending of the last section to be encrypted.
    '''

    read_elf_cmd = list((READ_ELF_CMD + ELF_PATH).split(" "))
    read_elf = subprocess.run(
        read_elf_cmd,
        capture_output=True,
        text=True,
        check=True)
    read_elf_lines = list(read_elf.stdout.split('\n'))

    for section in read_elf_lines:
        section_info = list(filter(('').__ne__, list(section.split(" "))))
        if len(section_info) > 2:

            if FIRST_SECTION_EXECUTABLE == section_info[2]:
                address_start_executable = int(section_info[5], 16)

            if FIRST_SECTION_TO_ENC == section_info[2]:
                address_start_encrypt = int(section_info[5], 16)

            if LAST_SECTION_TO_ENC == section_info[2]:
                # Ending address = beginning address + offset
                address_stop_encrypt = int(
                    section_info[5], 16) + int(section_info[6], 16)

    return address_start_executable, address_start_encrypt, address_stop_encrypt



def read_decoding_table():
    '''
    Read the decoding table (.csv file) generated outside of this project.

    Parameters
    ----------

    Returns
    ----------
    cs_decoder : list of dict
        Index of list is the fct7_3_opcode (= concatenation of instr[31:25] | instr[14:12] | instr[6:2])
        Every dict has 3 fields: cs_vector on N bits, is_multicycle on 1 bit, ctrl_transfer on 2 bits.
            - control_transfer(BRANCH_NONE) = 2'b00
            - control_transfer(BRANCH_JAL) = 2'b01
            - control_transfer(BRANCH_JALR) = 2'b10
            - control_transfer(BRANCH_COND) = 2'b11
    '''
    with open(CS_PATH, "r") as file:
        cs_file = file.read()
    cs_file_list = list(filter(('').__ne__, list(cs_file.split('\n'))))

    cs_decoder = []
    for fct7_3_opcode in range(len(cs_file_list)):
        cs_file_line = list(cs_file_list[fct7_3_opcode].split(','))
        if int(cs_file_line[1], 16) != fct7_3_opcode:
            raise ValueError(f'Error, {CS_PATH} is bad-formated.')
        cs_decoder.append({'cs_vector': int(cs_file_line[2], 16), 'is_multicycle': int(cs_file_line[3]), 'ctrl_transfer': int(cs_file_line[4])})
    return (cs_decoder)



###### RISC-V asm analysis ######
def check_load_stall(instr, next_instr):
    '''
    Check if a load_stall will happen at execution time.
    When a rs1/rs2 of an instruction is the same of a LW rd.

    Parameters
    ----------
    instr : Instruction
    next_instr : Instruction

    Returns
    ----------
    load_stall : bool
    '''
    load_stall = False # Instructions without rs1 or rs2 cannot generate a load_stall after a LW.
    if instr.inst in LOAD_INSTR:
        if next_instr.inst in INSTR_TYPE["R"] + INSTR_TYPE["S"] + INSTR_TYPE["B"]: # Instruction with rs1 and rs2
            if instr.rd == next_instr.rs1 or instr.rd == next_instr.rs2:
                load_stall = True
        if next_instr.inst in INSTR_TYPE["I_arith"] + INSTR_TYPE["I_load_jalr"]: # Instruction with rs1 only
            if instr.rd == next_instr.rs1:
                load_stall = True
    return load_stall



###### Main ######
def encrypt_elf():
    '''
    Encrypt the executable sections (= instructions) of an elf file.


    Informations
    ------------
    According to link.ld, there are 2 memories:
    - dbg (rwxai) : ORIGIN = 0x1A110800, LENGTH = 0x1000
    - ram (rwxai) : ORIGIN = 0x00000000, LENGTH = 0x10000

    Therefore:
    - dbg fills the first 0x1000 bits
    - RAM begins at 0x1000 = 4096, thus addr_elf-4096 (= addr_hex) is used to index the ram only

    Parameters
    ----------

    Returns
    ----------
        Generate a new elf file: the encrypted one
    '''

    # Read the original elf file
    with open(ELF_PATH, 'rb') as file:
        plain_elf = file.read()

    # fct7_3_opcode to control signal decoding table
    if args.control_signals:
        cs_decoder = read_decoding_table()

    # Code class instanciation
    code = Code(OBJ_PATH, OBJ_PATH, args.control_signals)
    code.read_itb()

    # S, k, rate, a, b, key, nonce are global variables
    ascon_initialize(S, k, rate, a, 6, key, nonce) # todo replace 6 per b

    # The area to be encrypted is determined
    address_start_executable, address_start_encrypt, address_stop_encrypt = find_sections_to_encrypt()

    # Before the area of encryption the elf is not encrypted (just copy/paste)
    cipher_elf = plain_elf[:address_start_encrypt]

    # String to be written in files
    ascon_states_hex = ""
    ascon_states_dec = ""
    ascon_states_hex_dbg = ""

    cs_vector = 0 # default in case there is no "--control_signals" option
    instr_minus4 = 0x7

    cs_vector_id = 0x3
    cs_vector_ex = 0x3
    cs_decoder_instr = 0x03
    is_instr_multicycle = 0
    is_instr_minus4_multicycle = 0
    is_instr_minus8_multicycle = 0
    is_instr_minus12_multicycle = 0

    alu_en_id = True
    alu_en_ex = False

    # Encrypt every instruction in the range
    for addr_elf in range(address_start_encrypt, address_stop_encrypt, 4):
        addr_hex = addr_elf - address_start_executable
        instr = int(reverse_bytes(plain_elf[addr_elf:addr_elf + 4]).hex(), 16)
        pc_pc_instr = f"{hex(addr_hex)[2:]},{addr_hex},{reverse_bytes(plain_elf[addr_elf:addr_elf + 4]).hex()}"
        other_lines_dbg = f"{'state_not_patched':<24}:{pc_pc_instr},{state2str(S)}\n"

        if CS_MODE:
            # Extract info from cs_decoder 
            cs_vector_if = cs_decoder_instr
            cs_decoder_instr = cs_decoder[instr2fct7_3_opcode(instr)]['cs_vector']

            is_instr_minus8_multicycle = is_instr_minus4_multicycle
            is_instr_minus4_multicycle = is_instr_multicycle
            is_instr_multicycle = cs_decoder[instr2fct7_3_opcode(instr)]['is_multicycle']

            prev_instr_ctrl_transfer = cs_decoder[instr2fct7_3_opcode(instr_minus4)]['ctrl_transfer']


            """
            Setup cs_vector_xored to be xored with ascon state. cs_vector is concatenation of :
                - cs_vector_id : from ID stage
                - cs_vector_ex : from EX stage
            CS Generate cs_vector_id: CS FROM THE PREVIOUS INSTRUCTION @PC-4  (THE ONE IN DECODE)
            """
            #when ex_ready = 0 => id_ready = if_ready = id_valid = 0 => no decryption
            ex_ready = True 

            # Update CS_VECTOR_EX
            if cs_ex_mode:
                id_invalid = check_load_stall(code.instrs[addr_hex-8], code.instrs[addr_hex-4]) # load_stall -> id_invalid

                if id_invalid:
                    if ex_ready:
                        cs_vector_ex = (cs_vector_ex & MASK_CS_VECTOR_ID_INVALID_EX_READY) | CS_VECTOR_ID_INVALID_EX_READY
                    else:
                        cs_vector_ex = cs_vector_ex

                # When instr at PC+4 of a multicycle instruction is decrypted, the multicycle instr is still in EX
                elif is_instr_minus4_multicycle == 1:# and not is_prev_instr_disc:
                    cs_vector_ex = cs_vector_if

                else:
                # Update specific EX signals from ID according to the their enable signals. Look at 'ex_en' in CS_VECTOR_ARCH.
                    cs_vector_ex = (cs_vector_id & make_mask_ex_en(cs_vector_id)) | \
                                   (cs_vector_ex & (CS_VECTOR_ALL_ONE ^ make_mask_ex_en(cs_vector_id)))


            # Update CS_VECTOR_ID
            deassert_we = (is_instr_minus4_multicycle == 1) | (prev_instr_ctrl_transfer in [0b01, 0b10])
            #log(f"#{hex(addr_hex)},{code.instrs[addr_hex].inst},{deassert_we},{prev_instr_ctrl_transfer}")
            cs_vector_id = cs_vector_if & DEASSERT_WE_MASK if deassert_we else cs_vector_if


            # Build cs_vector depending of the mode of control signal association
            if cs_id_mode and cs_ex_mode:
                cs_vector_xored = (cs_vector_ex << 8) | cs_vector_id
            elif cs_id_mode:
                cs_vector_xored = cs_vector_id
            elif cs_ex_mode:
                cs_vector_xored = cs_vector_ex


            alu_en_ex = alu_en_id
            instr_minus4 = instr
            if (cs_vector_xored >> 32) != 0:
                raise ValueError(f"Error, cs_vector should fit on 32 bits")

            # XOR CONTROL_SIGNALS WITH STATE
            S[0] ^= cs_vector_xored

            other_lines_dbg += f"{'state_cs2cipher':<24}:{pc_pc_instr},{state2str(S)},"
            other_lines_dbg += f"{hex(cs_vector_xored)[2:]},{is_instr_multicycle}\n"

            # PC(hex), PC(dec), instr, instr_cs_vector, cs_vector_used, is_instr_multicycle, state
            ascon_states_dec +=f"{pc_pc_instr},{cs_decoder_instr},{cs_vector_xored},{is_instr_multicycle},{','.join(map(str, S))}\n"
            ascon_states_hex +=f"{pc_pc_instr},{hex(cs_decoder_instr)[2:]},{hex(cs_vector_xored)[2:]},{is_instr_multicycle},{state2str(S)}\n"
        else:
            # PC(hex), PC(dec), instr, state
            ascon_states_dec +=f"{pc_pc_instr},{','.join(map(str, S))}\n"
            ascon_states_hex +=f"{pc_pc_instr},{state2str(S)}\n"



        # Iterate the encryption of one instruction (xor plain) rate = 4
        S[0] ^= bytes_to_int(reverse_bytes(plain_elf[addr_elf:addr_elf + 4])) << 32
        instr_cipher = int_to_bytes(S[0] >> 32, 4)
        cipher_elf += reverse_bytes(instr_cipher)

        other_lines_dbg += f"{'state_cipher2mux_fast':<24}:{pc_pc_instr},{state2str(S)},{instr_cipher.hex()}\n"


        # Process a permutation)
        ascon_permutation(S, b)


        other_lines_dbg += f"{'state_perm2reg':<24}:{pc_pc_instr},{state2str(S)}\n"

        if CS_MODE:
            first_line_dbg = f"{'='*125}{reverse_bytes(plain_elf[addr_elf:addr_elf + 4]).hex()}==="
            first_line_dbg += f"CS:{hex(cs_decoder_instr)[2:]}"
            first_line_dbg += f"===Mul:{is_instr_multicycle == 1}\n"
        else:
            first_line_dbg = f"{'='*125}{reverse_bytes(plain_elf[addr_elf:addr_elf + 4]).hex()}\n"
        ascon_states_hex_dbg += first_line_dbg + other_lines_dbg


    # After the area of encryption the elf is not encrypted (just copy/paste)
    cipher_elf += plain_elf[address_stop_encrypt:]

    with open(ELF_PATH, 'wb') as file:
        file.write(cipher_elf)

    with open(STATES_DEC_CSV_PATH, 'w', encoding="utf-8") as file:
        file.write(ascon_states_dec)

    with open(STATES_HEX_CSV_PATH, 'w', encoding="utf-8") as file:
        file.write(ascon_states_hex)

    with open(STATES_HEX_DBG_CSV_PATH, 'w', encoding="utf-8") as file:
        file.write(ascon_states_hex_dbg)



if __name__ == "__main__":
    encrypt_elf()

