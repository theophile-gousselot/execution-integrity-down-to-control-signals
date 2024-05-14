#!/usr/bin/env python3

"""
riscv-elf-encryption.py

This script encrypts sections of an elf file (fct: encrypt_elf()). The algorithm used is ASCON.
"""

import os
import subprocess
import argparse
from ascon_fct import ascon_initialize, ascon_process_one_encryption, ascon_permutation, bytes_to_int, reverse_bytes, int_to_bytes, state2str, instr2fct3_7_opcode
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

DEBUG = True

def log(string):
    if DEBUG:
        print(string)


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


###### CMD/SECTION NAMES ######
READ_ELF_CMD = "/opt/corev/bin/riscv32-corev-elf-readelf -S "
FIRST_SECTION_EXECUTABLE = ".vectors"
FIRST_SECTION_TO_ENC = ".init"
LAST_SECTION_TO_ENC = ".text"


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

def check_load_stall(instr, next_instr):
    load_stall = False
    if instr.inst in LOAD_INSTR:
        if next_instr.inst in INSTR_TYPE["R"] + INSTR_TYPE["S"] + INSTR_TYPE["B"]:
            if instr.rd == next_instr.rs1 or instr.rd == next_instr.rs2:
                load_stall = True
        if next_instr.inst in INSTR_TYPE["I_arith"] + INSTR_TYPE["I_load_jalr"]:
            if instr.rd == next_instr.rs1:
                load_stall = True
    return load_stall

INSTR_TYPE["I_arith"] + INSTR_TYPE["I_load_jalr"]


###### Main ######
def encrypt_elf():
    '''
    Encrypt the executable sections (= instructions) of an elf file.


    Informations
    ------------
    According to cv32e40p/bsp/link.ld, there are 2 memories:
    - dbg (rwxai) : ORIGIN = 0x1A110800, LENGTH = 0x1000
    - ram (rwxai) : ORIGIN = 0x00000000, LENGTH = 0x400000

    Therefore:
    - dbg fills the first 0x1000 bits
    - RAM begins at 0x1000 = 4096, thus i-4096 is used to index the ram only

    Parameters
    ----------

    Returns
    ----------
        Generate a new elf file: the encrypted one
    '''

    # Read the original elf file
    with open(ELF_PATH, 'rb') as file:
        plain_elf = file.read()

    # READ CONTROL SIGNALS
    if args.control_signals:
        with open(CS_PATH, "r") as file:
            cs_file = file.read()
        cs_file_list = list(filter(('').__ne__, list(cs_file.split('\n'))))

        cs_list = []
        for fct3_7_opcode in range(len(cs_file_list)):
            cs_file_line = list(cs_file_list[fct3_7_opcode].split(','))
            if int(cs_file_line[1], 16) != fct3_7_opcode:
                raise ValueError(f'Error, {CS_PATH} is bad-formated.')
            cs_list.append({'cs_vector': int(cs_file_line[2], 16), 'is_multicycle': int(cs_file_line[3]), 'ctrl_transfer': int(cs_file_line[4])})
            # control_transfer(BRANCH_NONE) = 2'b00
            # control_transfer(BRANCH_JAL) = 2'b01
            # control_transfer(BRANCH_JALR) = 2'b10
            # control_transfer(BRANCH_COND) = 2'b11


    # DISAS INSTRUCTIONS
    code = Code(OBJ_PATH, OBJ_PATH, args.control_signals)
    code.read_itb()


    # S, k, rate, a, b, key, nonce are global variables
    ascon_initialize(S, k, rate, a, 6, key, nonce) # todo replace 6 per b

    # The area to be encrypted is determined
    address_start_executable, address_start_encrypt, address_stop_encrypt = find_sections_to_encrypt()

    # Before the area of encryption the elf is not encrypted (just copy/paste)
    cipher_elf = plain_elf[:address_start_encrypt]

    ascon_states_hex = ""
    ascon_states_dec = ""
    ascon_states_hex_dbg = ""
    cs_vector = 0 # default in case there is no "--control_signals" option
    prev_prev_instr = 0x7
    prev_instr = 0x7
    alu_en = True
    alu_en_ex = False

    for addr_elf in range(address_start_encrypt, address_stop_encrypt, 4):
        addr_hex = addr_elf - address_start_executable
        instr = int(reverse_bytes(plain_elf[addr_elf:addr_elf + 4]).hex(), 16)
        pc_pc_instr = f"{hex(addr_hex)[2:]},{addr_hex},{reverse_bytes(plain_elf[addr_elf:addr_elf + 4]).hex()}"
        other_lines_dbg = f"{'state_not_patched':<24}:{pc_pc_instr},{state2str(S)}\n"

        if CS_MODE:
            cs_vector_instr = cs_list[instr2fct3_7_opcode(instr)]['cs_vector']
            cs_vector_prev_instr = cs_list[instr2fct3_7_opcode(prev_instr)]['cs_vector']
            cs_vector_prev_prev_instr = cs_list[instr2fct3_7_opcode(prev_prev_instr)]['cs_vector']

            is_prev_prev_instr_multicycle = cs_list[instr2fct3_7_opcode(prev_prev_instr)]['is_multicycle']
            is_prev_instr_multicycle = cs_list[instr2fct3_7_opcode(prev_instr)]['is_multicycle']
            is_instr_multicycle = cs_list[instr2fct3_7_opcode(instr)]['is_multicycle']

            is_prev_instr_disc = cs_list[instr2fct3_7_opcode(prev_instr)]['ctrl_transfer'] in [1, 2, 3]


            #print(f"{hex(i-4096)},{is_prev_instr_disc}")


            # CS FROM THE PREVIOUS INSTRUCTION @PC-4  (THE ONE IN DECODE)
            if cs_id_mode or cs_ex_mode:
                # A multicycle instruction generates a deassert_we = 1, thus alu_en = False
                alu_en = not (is_prev_instr_multicycle == 1 or addr_elf == address_start_encrypt)

                #log(f"{hex(addr_hex)},{code.instrs[addr_hex].inst},{is_prev_instr_multicycle ==1 or addr_elf == address_start_encrypt},{not alu_en}")

                cs_vector_prev_instr_mask = cs_vector_prev_instr if alu_en else cs_vector_prev_instr & 0b01111111


            # CS FROM THE PREVIOUS PREVIOUS INSTRUCTION @PC-8  (THE ONE IN EXECUTE)
            if cs_ex_mode:
                #log(f"{hex(addr_hex)},{code.instrs[addr_hex-8].inst},{code.instrs[addr_hex-4].inst},{code.instrs[addr_hex-8].rd},{code.instrs[addr_hex-4].rs1},{code.instrs[addr_hex-8].rd},{code.instrs[addr_hex-4].rs2}")


                id_invalid = check_load_stall(code.instrs[addr_hex-8], code.instrs[addr_hex-4]) # load_stall -> id_invalid -> CSex = default

                #log(f"{hex(addr_hex)},{code.instrs[addr_hex].inst},{zfint(cs_vector_prev_prev_instr_mask,4)}")

                if id_invalid:
                    cs_vector_prev_prev_instr_mask = 0x83 #default value


                elif code.instrs[addr_hex-8].inst in ["div", "divu"]: #alu_en = 0, therefore  mult-instruction CS are not propageted to EX stage, the one of previous instr are frozen in
                    cs_vector_prev_prev_instr_mask = cs_vector_prev_prev_instr

                elif code.instrs[addr_hex-8].inst in MULTIPLICATION_INSTR: #alu_en = 0, therefore  mult-instruction CS are not propageted to EX stage, the one of previous instr are frozen in
                    #cs_vector_prev_prev_instr_mask = cs_vector_prev_instr & 0b01111111
                    cs_vector_prev_prev_instr_mask = cs_vector_prev_prev_instr_mask & 0b01111111

                elif is_prev_instr_multicycle == 1 and not is_prev_instr_disc:
                    # In case of a multicycle, the instruction is still in the decode but with deassert (->mask)
                    # and the instruction is in execute, withtout deassert, thus ex=CS_decode (without mask)
                    cs_vector_prev_prev_instr_mask = cs_vector_prev_instr

                elif is_prev_prev_instr_multicycle == 1 or addr_elf <= address_start_encrypt+4:
                    cs_vector_prev_prev_instr_mask = cs_vector_prev_prev_instr & 0b01111111

                elif addr_elf <= address_start_encrypt+4:
                    cs_vector_prev_prev_instr_mask = cs_vector_prev_prev_instr & 0b01111111
                else:

                    cs_vector_prev_prev_instr_mask = cs_vector_prev_prev_instr


                alu_en_ex = alu_en


            if cs_id_mode and cs_ex_mode:
                cs_vector_xored = (cs_vector_prev_prev_instr_mask << 8) | cs_vector_prev_instr_mask
            elif cs_id_mode:
                cs_vector_xored = cs_vector_prev_instr_mask
            elif cs_ex_mode:
                cs_vector_xored = cs_vector_prev_prev_instr_mask


            prev_prev_instr = prev_instr
            prev_instr = instr
            if (cs_vector_xored >> 32) != 0:
                raise ValueError(f"Error, cs_vector should fit on 32 bits")


            # XOR CONTROL_SIGNALS WITH STATE
            S[0] ^= cs_vector_xored

            other_lines_dbg += f"{'state_cs2cipher':<24}:{pc_pc_instr},{state2str(S)},"
            other_lines_dbg += f"{hex(cs_vector_xored)[2:]},{is_instr_multicycle}\n"

            # PC(hex), PC(dec), instr, instr_cs_vector, cs_vector_used, is_instr_multicycle, state
            ascon_states_dec +=f"{pc_pc_instr},{cs_vector_instr},{cs_vector_xored},{is_instr_multicycle},{','.join(map(str, S))}\n"
            ascon_states_hex +=f"{pc_pc_instr},{hex(cs_vector_instr)[2:]},{hex(cs_vector_xored)[2:]},{is_instr_multicycle},{state2str(S)}\n"
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
            first_line_dbg += f"CS:{hex(cs_list[instr2fct3_7_opcode(instr)]['cs_vector'])[2:]}"
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
