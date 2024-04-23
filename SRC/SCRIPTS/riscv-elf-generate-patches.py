#!/usr/bin/python3
"""
riscv-elf-generate_patches.py

This script generates patches from a <program>.itb and <program>_c_states_dec.csv files.
Patches are wroten in <program>_encrypted_patches.mem file.
"""

import os
import sys
import argparse
import networkx as nx
import matplotlib.pyplot as plt

# In some programs the get_ret_successors_rec function is call more than
# 1000 times recursively
sys.setrecursionlimit(10000)

###### Arguments ######
parser = argparse.ArgumentParser(description="generate patch from itb file")
parser.add_argument("src_path", help="specify the source path",
                    type=str, nargs='?', const="", default="")
parser.add_argument("obj_path", help="specify the object path",
                    type=str, nargs='?', const="", default="")
parser.add_argument("-c", "--control_signals", help="use control signal in encryption?",
                    action="store_true")
parser.add_argument("-v", "--verbose",
                    help="increase output verbosity", action="store_true")
args = parser.parse_args()

###### Paths ######
PROGRAM = "program"
OBJ_PATH = args.obj_path
SRC_PATH = args.src_path
CS_FLAG = "_cs" if args.control_signals else ""
ITB_PATH = f"{OBJ_PATH}/{PROGRAM}.itb"
STATES_DEC_CSV_PATH = f"{OBJ_PATH}/{PROGRAM}_encrypted{CS_FLAG}_states_dec.csv"
EDGES_PATH = f"{OBJ_PATH}/{PROGRAM}_edges.csv"
PATCHES_HEX_PATH = f"{OBJ_PATH}/{PROGRAM}_encrypted{CS_FLAG}_patches.mem"
PATCHES_HEX_CSV_PATH = f"{OBJ_PATH}/{PROGRAM}_encrypted{CS_FLAG}_patches_hex.csv"
SUCCESSORS_PATH = f"{OBJ_PATH}/{PROGRAM}.successors"
JALR_SUCCESSORS_PATH = f"{OBJ_PATH}//{PROGRAM}_jalr_successors.csv"
FILE_GET_JALR_SUCC_PATH = "a script"

##### RISC-V Dict #####
PATCH_POLICIES = ['NL']  # Patch when No Linear

INSTR_FIELDS = {}
INSTR_FIELDS["R"] = ['rd', 'rs1', 'rs2']
INSTR_FIELDS["I_arith"] = ['rd', 'rs1', 'imm']
INSTR_FIELDS["I_load_jalr"] = ['rd', 'imm', 'rs1']
INSTR_FIELDS["I_env"] = []
INSTR_FIELDS["S"] = ['rs2', 'imm', 'rs1']
INSTR_FIELDS["B"] = ['rs1', 'rs2', 'imm']
INSTR_FIELDS["U"] = ['rd', 'imm']
INSTR_FIELDS["J"] = ['rd', 'imm']
INSTR_FIELDS["SYSTEM"] = []


INSTR_TYPE = {}
INSTR_TYPE['I_arith'] = ['addi', 'xori', 'ori', 'andi', 'slli', 'srli', 'srai', 'slti', 'sltiu']
INSTR_TYPE['I_load_jalr'] = ['lb', 'lh', 'lw', 'lbu', 'lhu', 'jalr']
INSTR_TYPE['I_env'] = ['ecall', 'ebreak']
INSTR_TYPE['S'] = ['sb', 'sh', 'sw']
INSTR_TYPE['B'] = ['beq', 'bne', 'blt', 'bge', 'bltu', 'bgeu']
INSTR_TYPE['J'] = ['jal']
INSTR_TYPE['U'] = ['lui', 'auipc']
INSTR_TYPE['SYSTEM'] = ['csrrw', 'csrrs', 'csrrc', 'csrrwi', 'csrrsi', 'csrrci', 'mret', 'wfi']
INSTR_TYPE['R'] = [
    'add',
    'sub',
    'xor',
    'or',
    'and',
    'sll',
    'srl',
    'sra',
    'slt',
    'sltu',
    'mul',
    'mulh',
    'mulhsu',
    'mulhu',
    'div',
    'divu',
    'rem',
    'remu']


DISC_INSTR = ['jalr', 'jal', 'beq', 'bne', 'blt', 'bge', 'bltu', 'bgeu']


##### CONTANTS & SIGNAL WIDTH #####
ASCON_STATE_WIDTH = 320
ADDR_ENC_BEGIN = 124
WIDTH_ADDR = 14
NB_ADDR_REDIRECTED_MAX = 11
REDIRECTION_TAG_SIZE = int((ASCON_STATE_WIDTH - WIDTH_ADDR * NB_ADDR_REDIRECTED_MAX * 2))
REDIRECTION_TAG = '1' * REDIRECTION_TAG_SIZE


##### Parameters for graph plotting #####
DISTANCE_MAX = 2
NODE0 = 200


def zfint(i):
    """ Convert a int into a str filled with 0 to reach 5 caracters. """
    return hex(i)[2:].zfill(5)


class Instruction:
    """
    A class to decode the instructions.

    ...

    Attributes
    ----------
    addr : int
        Addr of the PC in memory
    fname : str
       fname
    current_src_file : str
        current source file
    current_src_line : int
        current source line
    mcode : str
         instruction (hex)
    asm_len : str
        number of words in self.asm
    asm : str
         assembler mnemonics
    asm_list : list of str
         list of self.asm words
    inst : str
         inst of the instruction

    (provided by get_type method)
    disc : bool
         true if it is an discontinuity instruction
    type : str
         type of the instruction (R, I_arith, I_load_jalr, I_env, S, B, J, U, SYSTEM)
         as described in the Volume 1, Unprivileged Specification version 20191213
         Chapter 24 "RV32/64G Instruction Set Listings":
         https://github.com/riscv/riscv-isa-manual/releases/download/Ratified-IMAFDQC/riscv-spec-20191213.pdf
    rd : int
        Destination register
    rs1 : int
        Source 1 register
    rs2 : int
        Source 2 register
    imm : int
        Immediate

    (provided by get_successors method)
    successors : list of int
        list of addresses which are available destinations
    successors_n : int
        number of successors
    predecessors : list of int
        list of addresses which are available previous instructions
    predecessors_n : int
        number of predecessors

    (provided by get_states method)
    state : list of int (len = 5)
        list of internal state for every instruction when encrypted

    Methods
    -------
    get_type
    get_successors
    """

    def __init__(self, addr, fname, current_src_file, current_src_line, mcode, asm_len, asm):
        self.addr = int(addr)
        self.fname = fname
        self.current_src_file = current_src_file
        self.current_src_line = int(current_src_line)
        self.mcode = mcode
        self.asm_len = int(asm_len)
        self.asm = asm

        # Build a list of instr, fields and comments
        self.asm_list = list(self.asm.split(' '))
        self.inst = self.asm_list[0]
        self.get_type()
        self.get_fields()
        self.get_successors()

    def get_type(self):
        """
        Get the type (R, I_arith, I_load_jalr, I_env, S, B, J, U, SYSTEM) of the instruction,
        and if it is a dicontinuity instruction.
        """
        self.disc = (self.inst in DISC_INSTR)

        self.type = None
        for instr_type in INSTR_TYPE:
            if self.inst in INSTR_TYPE[instr_type]:
                self.type = instr_type
                break
        if self.type is None:
            raise print(
                f"Error, {self.inst} is not referenced, please insert it in INSTR_TYPE dict")

    def get_fields(self):
        """
        Get the fields (rs1, rs2, rd, imm) of the instruction.
        """
        self.fields = [] if self.asm_len == 1 else list(filter(('').__ne__, list(
            self.asm_list[1].replace('(', ',').replace(')', ',').split(','))))

        self.rd, self.rs1, self.rs2, self.imm = None, None, None, None
        for i, field in enumerate(INSTR_FIELDS[self.type]):
            if field == 'imm':
                self.imm = int(self.fields[i], 16)
            elif field == 'rs1':
                self.rs1 = int(self.fields[i].replace('x', ''))
            elif field == 'rs2':
                self.rs2 = int(self.fields[i].replace('x', ''))
            elif field == 'rd':
                self.rd = int(self.fields[i].replace('x', ''))

        if self.inst == 'jalr' and self.rd != 0 and self.imm != 0 and self.rs1 != 1:
            print(
                f"The instruction '{self.addr}: {self.asm}' is an unsupported indirect jump.")

    def get_successors(self):
        """
        Get the successors of the instruction.
        """
        self.successors = []
        self.successors_n = 0
        if self.disc:
            if self.type == 'B':
                self.successors = [self.addr + 4, self.imm]
                self.successors_n = 2
            elif self.inst == 'jal':
                self.successors = [self.imm]
                self.successors_n = 1
            else:
                self.successors = []
                self.successors_n = 0

        else:
            self.successors = [self.addr + 4]
            self.successors_n = 1

        self.predecessors = []
        self.predecessors_n = 0


class Code:
    """
    A class to describe a program containing instructions.

    ...

    Attributes
    ----------
    instrs : dict of instruction instances.
        Keys are the address of instructions.
        Predecessors of every instructions instances are compeleted.
    """

    def __init__(self):
        self.instrs = {}

    def add_instr(self, addr, instr):
        '''
        Add the instruction to the dict self.instrs. Key is the address, and an Instruction is the value.

        Parameters
        ----------
        addr : int
            address of the instruction

        instr : Instruction (instance)
            instance of classe Instruction
        '''
        self.instrs[addr] = instr

    def read_itb(self):
        """
        Read a itb file, for every line (= instruction) create a Instruction instance
        and add it to self.instrs
        """
        with open(ITB_PATH, 'r', encoding="utf-8") as file:
            itb = file.read()
        itb_list = list(itb.split("\n"))

        for itb_l in itb_list:

            # If itb_l is an instruction
            if itb_l != "" and itb_l[0] != '#':

                # Convert the itb string metadata into a list
                instr_arg = list(
                    filter(('').__ne__, list(itb_l.split(" ", 6))))

                addr = int(instr_arg[0])
                self.add_instr(addr, Instruction(*instr_arg))

    def get_predecessors(self):
        """
        Get the predecessors for every instruction from successors of every instruction.
        """
        for addr in self.instrs:
            for s in self.instrs[addr].successors:
                if addr not in self.instrs[s].predecessors:
                    self.instrs[s].predecessors.append(addr)
                    self.instrs[s].predecessors_n += 1

    def get_ret_successors(self):
        """
        Get the succcessors of ret (= jalr x0,0(x1)) (indirect jumps).
        Successors of ret are identified by exploring recursively the successors of jal and jalr with rd=x1 .
        """
        self.get_jalr_successors_from_nominal_exec()

        for addr in self.instrs:
            if self.instrs[addr].inst in ['jal', 'jalr'] and self.instrs[addr].rd == 1:
                for s in self.instrs[addr].successors:
                    self.get_ret_successors_rec(s, addr, [])

    def get_ret_successors_rec(self, addr, jump_addr, already_visited):
        '''
        Recursive function to identify the ret(s) associated to a jump with rd=1 (which induce a return).
        From a jump with rd=1 (J1), all the successors and their successors families are explored until
        a return is reached for each branch. If another jump with x1=1 (J2) is met, we consider that
        the excution flow will go through J2 destination until to meet a return which will lead
        the PC to J2 + 4. So J2 + 4, will be the next instruction explored after J1.

        Parameters
        ----------
        addr : int
            address of the instruction

        jump_addr : int
            address of the jump with rd = 1

        already_visited list of int
            list of address already explored (no need to explore to times the same instruction)
        '''
        if addr not in already_visited:
            already_visited.append(addr)

            instr = self.instrs[addr]

            # Return is found, @(jal rs1=1)+4 is added to its successors
            if instr.inst == 'jalr' and instr.rd == 0 and instr.rs1 == 1:
                if jump_addr + 4 not in instr.successors:
                    instr.successors.append(jump_addr + 4)
                    instr.successors_n += 1

            # Antother jump with rd=1 is found, the flow must pass through @(jump with rd=1) + 4
            elif instr.inst in ['jal', 'jalr'] and instr.rd == 1:
                self.get_ret_successors_rec(addr + 4, jump_addr, already_visited)

            else:
                for s in instr.successors:
                    self.get_ret_successors_rec(s, jump_addr, already_visited)

    def get_jalr_successors_from_nominal_exec(self):
        """
        The function use a nominal execution to discover the successores of every jalr function
        (except ret which are tackled by get_ret_successors_rec.
        """

        if not os.path.exists(JALR_SUCCESSORS_PATH):
            raise ValueError(f"{JALR_SUCCESSORS_PATH} does not exist," +
                             f"please execute {FILE_GET_JALR_SUCC_PATH} before.")

        with open(JALR_SUCCESSORS_PATH, "r", encoding="utf-8") as f:
            jalr_successors = list(
                filter(
                    ('').__ne__, list(
                        f.read().split('\n'))))

        # s content: "jalr_addr,number of extra cycles to be executed successors"
        for s in jalr_successors:
            s = list(map(int, s.split(',')))

            self.instrs[s[0]].successors = s[1:]
            self.instrs[s[0]].successors_n += len(s[1:])

    def write_successors(self):
        '''
        Write the successor file, which contains for every instruction its predecessors
        and its successors addresses.
        '''

        patches = ""
        patches += " Addr  Instruction      Predecessors Successors\n"
        patches += "=" * 48 + "\n"
        for addr in self.instrs:
            addr_str = f"{hex(self.instrs[addr].addr)[2:]}|{self.instrs[addr].addr}:"
            patches += f"{addr_str:>10}"
            patches += f"{self.instrs[addr].asm[:min(15, len(self.instrs[addr].asm))]:<15}   "
            patches += f"{self.instrs[addr].predecessors_n}:"
            patches += f"{' '.join(map(str, self.instrs[addr].predecessors)):<8}   "
            patches += f"{self.instrs[addr].successors_n}:"
            patches += f"{' '.join(map(str, self.instrs[addr].successors)):<8}    \n"

        with open(SUCCESSORS_PATH, 'w', encoding="utf-8") as file:
            file.write(patches)

    def read_states(self):
        '''
        Read state file (generated by riscv-elf-encryption). For each instruction the state used
        to encrypted  it is added as a attribute of the Instruction class.
        '''
        with open(STATES_DEC_CSV_PATH, 'r', encoding="utf-8") as file:
            states = file.read()

        states_list = list(states.split("\n"))

        for state_l in states_list:
            if len(state_l) > 0:
                if args.control_signals:
                    addr_hex, addr_dec, instr, cs_vector_prev_instr, is_multicycle, state = list(state_l.split(",", 5))
                    self.instrs[int(addr_dec)].state = list(
                        map(int, list(state.split(",", 4))))
                    self.instrs[int(addr_dec)].is_multicycle = is_multicycle == "1"
                    # cs_vector used to encrypt instr at PC is instr at PC-4
                    self.instrs[int(addr_dec)-4].cs_vector = int(cs_vector_prev_instr)
                else:
                    addr_hex, addr_dec, instr, state = list(state_l.split(",", 3))
                    self.instrs[int(addr_dec)].state = list(map(int, list(state.split(",", 4))))

    def add_patch_if_free(self, addr_patch, addr_src, addr_dest):
        '''
        If an addr_patch is free in hex_patches, a new patch, to reach addr_dest from addr_src is added.

        ----------
        addr_patch : int
            address to store the patch in the patches memory
        addr_src : int
            address of the instruction executed just before the addr_dest
        addr_dest : int
            address of the destination
        '''
        if not self.hex_patches_free[addr_patch >> 2]:
            print(f"WARNING, conflict for patching address (@{addr_patch} to @{addr_dest})")

        else:
            patch = ''
            for i in range(5):
                state1, state2 = self.instrs[addr_src].state[i], self.instrs[addr_dest].state[i]
                sub_state_patch = state1 ^ state2

                # When a branch is in EXECUTE, even if instr in DECODE is not a multicycle instruction, 
                # the signal we_deassert will be raised! Therefore, if the instr in DECODE was multicycle
                # CS was already masked: nothing to do. However, if not, as mask is applied by xoring 
                # cs_vector bits to mask to itself (as it is already in the patch through cs2cipher.
                if args.control_signals and i == 0 and (self.instrs[addr_patch].type == 'B'):
                        sub_state_patch ^= (self.instrs[addr_patch+4].cs_vector & 0x80)

                patch += hex(sub_state_patch)[2:].zfill(16)

            self.hex_patches_free[addr_patch >> 2] = False
            self.hex_patches[addr_patch >> 2] = patch

            patch_csv = f"{zfint(addr_patch)},{zfint(addr_src)},{zfint(addr_dest)},{patch}"
            self.hex_patches_csv[addr_patch >> 2] = patch_csv

    def get_patches(self, patch_policy):
        '''
        Generate patches for every transition needed one.

        Non-linear policy:
            Rules:
                1 - For jal, branch : patches are stored at @jal, @jump
                2 - For jalr : patchs are stored at @destination
                3 - In case of conflict, redirection is performed
            Algorithm:
            - Patches are firstly generated for branch and jal
            - Then Patches are generated for JALR destination (if not conflict)
            - Finally, redirection is set for all conflicts cases

        Parameters
        ----------
        patches_policy : str
            name for the patching policy, currently supported:
                NO: Non-linear (patch generated every time a successor is not at PC+4
        '''
        if patch_policy not in PATCH_POLICIES:
            print(
                f"The '{patch_policy}' is not a valid patch policy. It should be in '{PATCH_POLICIES}'.")

        # Non linear policy
        if patch_policy == 'NL':
            self.patches_dec = ""
            self.patches_hex = ""
            edges = ""

            # dict of jalr when patches are in conflicts
            self.patches_to_be_redirected = {}

            self.hex_patches = ['0' * 80] * len(self.instrs.keys())
            self.hex_patches_csv = ['00000,00000,00000,' + '0' * 80] * len(self.instrs.keys())
            self.hex_patches_free = [True] * len(self.instrs.keys())

            # FIRST ITERATION (Generate patches for all branch and jal)
            for addr in self.instrs:
                if addr > ADDR_ENC_BEGIN and addr != list(self.instrs.keys())[-1]:
                    for s in self.instrs[addr].successors:

                        # Generate edge file, which list all non-linear transitions
                        edges += f"{addr},{s}\n"

                        # Non-linear policy (patch generated every time a successor is not at PC+4)
                        if s != addr + 4:
                            # branch taken need 3 cycles so two instructions are loaded from
                            # memory after a branch (thus addr + 12)
                            if self.instrs[addr].type == 'B':
                                self.add_patch_if_free(addr, addr + 8, s)

                            elif self.instrs[addr].inst == 'jal':
                                self.add_patch_if_free(addr, addr + 4, s)

            # SECOND ITERATION (Generate patches for jalr)
            for addr in self.instrs:
                if addr > ADDR_ENC_BEGIN and addr != list(self.instrs.keys())[-1]:
                    if self.instrs[addr].inst == 'jalr':

                        # Detect if one successor of jalr is a branch or jal
                        # which has already a patch at his address
                        redirection = False
                        for s in self.instrs[addr].successors:
                            if not self.hex_patches_free[s >> 2]:
                                redirection = True
                                break

                        if redirection:
                            self.patches_to_be_redirected[addr] = self.instrs[addr].successors
                            print(f"### INFOS, redirection for jalr ({addr})")
                            if self.instrs[addr].successors_n > NB_ADDR_REDIRECTED_MAX:
                                print(f"/!\\ NOT SUPPORTED, jalr ({addr}) has " +
                                      f"{self.instrs[addr].successors_n} successors " +
                                      f"(> {NB_ADDR_REDIRECTED_MAX} supported for the redirection)")

                        else:
                            for s in self.instrs[addr].successors:
                                self.add_patch_if_free(s, addr + 4, s)



            # ITERATION OVER REDIRECTIONS
            addr_free = ADDR_ENC_BEGIN
            for addr in self.patches_to_be_redirected:
                addr_redirected = [0] * NB_ADDR_REDIRECTED_MAX

                # For each patch to be redirected, a free address if found and filled with the patch
                for i, s in enumerate(self.patches_to_be_redirected[addr][:NB_ADDR_REDIRECTED_MAX]):
                    while True:
                        if self.hex_patches_free[addr_free >> 2]:
                            addr_redirected[i] = addr_free
                            self.add_patch_if_free(addr_free, addr + 4, s)
                            break

                        if addr_free == list(self.instrs.keys())[-1]:
                            raise ValueError(f"There is no free address in memory to host redirected patches")
                        addr_free += 4

                # To be sure that patches_to_be_redirected is not too short
                self.patches_to_be_redirected[addr].extend([0]*NB_ADDR_REDIRECTED_MAX)

                # Insert redirection at the address of the jalr
                redirection_field = ""
                for s in range(NB_ADDR_REDIRECTED_MAX):
                    # Remove '0b' and the two least significant bits
                    redirection_field += bin(self.patches_to_be_redirected[addr][s])[2:-2].zfill(WIDTH_ADDR)
                    redirection_field += bin(addr_redirected[s])[2:-2].zfill(WIDTH_ADDR)
                self.hex_patches[addr >> 2] = hex(int(REDIRECTION_TAG + redirection_field, 2))[2:]
                self.hex_patches_csv[addr >> 2] = f"{zfint(addr)},REDIRECTION,{REDIRECTION_TAG}{redirection_field}"
                self.hex_patches_free[addr >> 2] = False

            with open(EDGES_PATH, 'w', encoding="utf-8") as file:
                file.write(edges)

            with open(PATCHES_HEX_CSV_PATH, 'w', encoding="utf-8") as file:
                file.write('\n'.join(self.hex_patches_csv))

            with open(PATCHES_HEX_PATH, 'w', encoding="utf-8") as file:
                file.write('\n'.join(self.hex_patches))

    def plot_graph(self):
        '''
        Plot a graph of all instructions.
        Nodes are instructions and edges are transitions.
        '''
        self.G = nx.empty_graph()
        # G = nx.DiGraph()  # to display arrow
        for addr in self.instrs:
            self.G.add_node(addr)

        for addr in self.instrs:
            for s in self.instrs[addr].successors:
                self.G.add_edge(addr, s)
        nx.draw_circular(
            self.G,
            node_color='#5F259F',
            node_size=10)  # , with_labels=True)
        plt.show()

    def plot_subgraph(self, node0, order_min, order_max, save=False):
        '''
        Plot a graph of instructions close to a given instruction.
        Nodes are instructions and edges are transitions.
        '''
        # self.subG = nx.empty_graph()
        self.subG = nx.DiGraph()  # to display arrow
        self.subGnodeOrder = {}

        self.subG.add_node(node0)
        self.already_visited = []
        distance = 1
        self.extract_nodes_rec(node0, node0, distance, order_min, order_max, 0)

        # pos=nx.fruchterman_reingold_layout(self.subG)
        pos = nx.random_layout(self.subG)
        # pos=nx.circular_layout(self.subG)
        # pos=nx.spectral_layout(self.subG)
        # pos=nx.spring_layout(self.subG)

        color = ['red' if node == node0 else '#5F259F' for node in self.subG]
        nodes_of_orders = {}

        nodes_of_orders = {key: [] for key in range(order_min, order_max + 1)}

        if True:
            # set X value (depending of the order)
            for pp in pos:
                pos[pp][0] = self.subGnodeOrder[pp]

            # set Y value (dispatch the nodes)
            for pp in pos:
                nodes_of_orders[self.subGnodeOrder[pp]].append(pp)

            for order in nodes_of_orders:
                nodes_of_orders[order].sort()

                l = len(nodes_of_orders[order])
                for i, addr in enumerate(nodes_of_orders[order]):
                    pos[addr][1] = i - ((l - 1) / 2)

        plt.figure(figsize=(16, 9))

        nx.draw(self.subG, pos, node_color=color, node_size=100, arrowsize=18)
        for pp in pos:
            pos[pp][1] += 0.06
        if True:
            labels = {}
            labels_init = {n: n for n in self.subG}
            for addr in labels_init:
                labels[addr] = f"{self.instrs[addr].addr}: {self.instrs[addr].asm[:min(15, len(self.instrs[addr].asm))]}"
            nx.draw_networkx_labels(self.subG, pos, labels=labels)
        else:
            nx.draw_networkx_labels(self.subG, pos)
        if save:
            plt.savefig(
                f"/home/theophile/these/these_theophile_gousselot/meetings/images/plot/cfi/code_successors/plot_code_successors_dhrystone_node{node0}_order{order_min}_{order_max}.pdf")
        else:
            plt.show()

    def extract_nodes_rec(self, addr_src, addr, distance, order_min, order_max, order):
        '''
        Recursively extract nodes (= instructions) close to a given instruction.
        '''
        if (addr_src, addr) not in self.already_visited:
            self.already_visited.append((addr_src, addr))
            # print(self.already_visited)
            if order >= order_min and order <= order_max:
                if order != order_max:
                    for s in self.instrs[addr].successors:
                        self.subG.add_node(s)
                        self.subG.add_edge(addr, s)
                        self.subGnodeOrder[s] = order + 1
                        self.extract_nodes_rec(
                            addr, s, distance - 1, order_min, order_max, order + 1)

                if order != order_min:
                    for p in self.instrs[addr].predecessors:
                        self.subG.add_node(p)
                        self.subG.add_edge(p, addr)
                        self.subGnodeOrder[p] = order - 1
                        self.extract_nodes_rec(
                            addr, p, distance - 1, order_min, order_max, order - 1)


###### Usefull functions #####


def to_bytes(l):  # where l is a list or bytearray or bytes
    return bytes(bytearray(l))


def bytes_to_int(bytes):
    return sum([bi << (i * 8) for i, bi in enumerate(to_bytes(bytes))])


def int_to_bytes(integer, nbytes):
    return to_bytes([(integer >> (i * 8)) % 256 for i in range(nbytes)])


def reverse_int(instr):
    return (instr & 0xff) << 24 | (instr & 0xff00) << 8 | (
        instr & 0xff0000) >> 8 | (instr & 0xff000000) >> 24


def reverse_bytes(instr):
    bytearray_instr = bytearray(instr)
    bytearray_instr.reverse()
    return bytes(bytearray_instr)


def save_several_subgraph(code):
    order_min = -2
    order_max = 1
    save = True
#    code.plot_subgraph(1428, -4, 0, False)
    code.plot_subgraph(1560, order_min, order_max, save)
    code.plot_subgraph(1428, order_min, order_max, save)
    code.plot_subgraph(2496, order_min, order_max, save)
    code.plot_subgraph(5668, order_min, order_max, save)
    code.plot_subgraph(5552, order_min, order_max, save)
    code.plot_subgraph(200, order_min, order_max, save)
    code.plot_subgraph(5592, order_min, order_max, save)
    code.plot_subgraph(9620, order_min, order_max, save)
    code.plot_subgraph(8712, order_min, order_max, save)
    code.plot_subgraph(10648, order_min, order_max, save)
    code.plot_subgraph(12724, order_min, order_max, save)
    code.plot_subgraph(8544, order_min, order_max, save)
    code.plot_subgraph(8800, order_min, order_max, save)
    code.plot_subgraph(12252, order_min, order_max, save)


###### Main ######
if __name__ == "__main__":
    code = Code()
    code.read_itb()
    code.get_predecessors()
    code.get_ret_successors()
    code.get_predecessors()
    code.write_successors()
    code.read_states()
    code.get_patches('NL')
    # code.plot_subgraph(NODE0, DISTANCE_MAX)
    # save_several_subgraph(code)
