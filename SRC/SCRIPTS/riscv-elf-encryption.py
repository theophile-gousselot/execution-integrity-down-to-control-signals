#!/usr/bin/env python3

"""
riscv-elf-encryption.py

This script encrypts sections of an elf file (fct: encrypt_elf()). The algorithm used is ASCON.
"""

import subprocess
import argparse
from ascon_fct import ascon_initialize, ascon_process_one_encryption, ascon_permutation, bytes_to_int, reverse_bytes, int_to_bytes, state2str, instr2fct3_7_opcode

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
    action="store_true")
args = parser.parse_args()

###### Paths ######
ELF_PATH = args.elf_path
CS_PATH = f"SRC/PROGRAM_TOOLS/CONTROL_SIGNALS/control_signals.csv"
STATES_DEC_CSV_PATH = f"{ELF_PATH[:-4]}_states_dec.csv"
STATES_HEX_CSV_PATH = f"{ELF_PATH[:-4]}_states_hex.csv"
STATES_HEX_DBG_CSV_PATH = f"{ELF_PATH[:-4]}_states_hex_debug.csv"

DEBUG = True


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
FIRST_SECTION = ".init"
LAST_SECTION = ".text"


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

            if FIRST_SECTION == section_info[2]:
                address_start_encrypt = int(section_info[5], 16)

            if LAST_SECTION == section_info[2]:
                # Ending address = beginning address + offset
                address_stop_encrypt = int(
                    section_info[5], 16) + int(section_info[6], 16)

    return address_start_encrypt, address_stop_encrypt


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
            cs_list.append({'cs_vector': int(cs_file_line[2], 16), 'is_multicycle': int(cs_file_line[3])})


    # S, k, rate, a, b, key, nonce are global variables
    ascon_initialize(S, k, rate, a, 6, key, nonce) # todo replace 6 per b

    # The area to be encrypted is determined
    address_start_encrypt, address_stop_encrypt = find_sections_to_encrypt()

    # Before the area of encryption the elf is not encrypted (just copy/paste)
    cipher_elf = plain_elf[:address_start_encrypt]

    ascon_states_hex = ""
    ascon_states_dec = ""
    ascon_states_hex_dbg = ""
    cs_vector = 0 # default in case there is no "--control_signals" option
    prev_instr = 0x7


    for i in range(address_start_encrypt, address_stop_encrypt, 4):
        instr = int(reverse_bytes(plain_elf[i:i + 4]).hex(), 16)
        pc_pc_instr = f"{hex(i-4096)[2:]},{i-4096},{reverse_bytes(plain_elf[i:i + 4]).hex()}"
        other_lines_dbg = f"{'state_not_patched':<24}:{pc_pc_instr},{state2str(S)}\n"

        if args.control_signals:
            cs_vector = cs_list[instr2fct3_7_opcode(prev_instr)]['cs_vector']
            is_prev_instr_multicycle = cs_list[instr2fct3_7_opcode(prev_instr)]['is_multicycle']
            is_instr_multicycle = cs_list[instr2fct3_7_opcode(instr)]['is_multicycle']

            if is_prev_instr_multicycle == 1 or i == address_start_encrypt:
                # A multicycle instruction generates a deassert_we = 1, from its second cycle of execution, 
                # the following instruction will be decrypted using control signals masked by deassert_we, 
                # thus, encryption must apply the mask. Deassert_we is null when first instr is decoded
                cs_vector_mask = cs_vector & 0b01111111
            else:
                cs_vector_mask = cs_vector

            prev_instr = instr
            if (cs_vector_mask >> 32) != 0:
                raise ValueError(f"Error, cs_vector should fit on 32 bits")


            # XOR CONTROL_SIGNALS WITH STATE
            S[0] ^= cs_vector_mask

            other_lines_dbg += f"{'state_cs2cipher':<24}:{pc_pc_instr},{state2str(S)},"
            other_lines_dbg += f"{hex(cs_vector_mask)[2:]},{is_instr_multicycle}\n"

            # PC(hex), PC(dec), instr, cs_vector, is_instr_multicycle, state
            ascon_states_dec +=f"{pc_pc_instr},{cs_vector_mask},{is_instr_multicycle},{','.join(map(str, S))}\n"
            ascon_states_hex +=f"{pc_pc_instr},{hex(cs_vector_mask)[2:]},{is_instr_multicycle},{state2str(S)}\n"
        else:
            # PC(hex), PC(dec), instr, state
            ascon_states_dec +=f"{pc_pc_instr},{','.join(map(str, S))}\n"
            ascon_states_hex +=f"{pc_pc_instr},{state2str(S)}\n"



        # Iterate the encryption of one instruction (xor plain) rate = 4
        S[0] ^= bytes_to_int(reverse_bytes(plain_elf[i:i + 4])) << 32
        instr_cipher = int_to_bytes(S[0] >> 32, 4)
        cipher_elf += reverse_bytes(instr_cipher)

        other_lines_dbg += f"{'state_cipher2mux_fast':<24}:{pc_pc_instr},{state2str(S)},{instr_cipher.hex()}\n"


        # Process a permutation)
        ascon_permutation(S, b)


        other_lines_dbg += f"{'state_perm2reg':<24}:{pc_pc_instr},{state2str(S)}\n"

        if args.control_signals:
            first_line_dbg = f"{'='*125}{reverse_bytes(plain_elf[i:i + 4]).hex()}==="
            first_line_dbg += f"CS:{hex(cs_list[instr2fct3_7_opcode(instr)]['cs_vector'])[2:]}"
            first_line_dbg += f"===Mul:{is_instr_multicycle == 1}\n"
        else:
            first_line_dbg = f"{'='*125}{reverse_bytes(plain_elf[i:i + 4]).hex()}\n"
        ascon_states_hex_dbg += first_line_dbg + other_lines_dbg


    # After the area of encryption the elf is not encrypted (just copy/paste)
    cipher_elf += plain_elf[address_stop_encrypt:]

    with open(ELF_PATH, 'wb') as file:
        file.write(cipher_elf)

    with open(STATES_DEC_CSV_PATH, 'w', encoding="utf-8") as file:
        file.write(ascon_states_dec)

    with open(STATES_HEX_CSV_PATH, 'w', encoding="utf-8") as file:
        file.write(ascon_states_hex)

    if DEBUG:
        with open(STATES_HEX_DBG_CSV_PATH, 'w', encoding="utf-8") as file:
            file.write(ascon_states_hex_dbg)


if __name__ == "__main__":
    encrypt_elf()
