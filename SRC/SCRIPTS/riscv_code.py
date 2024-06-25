import os
import sys

from riscv_instruction import Instruction, LOAD_INSTR, INSTR_TYPE
from riscv_control_signals import Control_signals




PATCH_POLICIES = ['NL']  # Patch when No Linear

##### CONTANTS & SIGNAL WIDTH #####
ASCON_STATE_WIDTH = 320
ADDR_ENC_BEGIN = 124
WIDTH_ADDR = 14
NB_ADDR_REDIRECTED_MAX = 11
REDIRECTION_TAG_SIZE = int((ASCON_STATE_WIDTH - WIDTH_ADDR * NB_ADDR_REDIRECTED_MAX * 2))
REDIRECTION_TAG = '1' * REDIRECTION_TAG_SIZE

def h(interger):
    return (hex(interger)[2:])

def zfint(i,bits):
    """ Convert a int into a str filled with 0 to reach 5 caracters. """
    return hex(i)[2:].zfill(bits)

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

    def __init__(self, src_path, obj_path, cs_vector_arch_id):
        self.instrs = {}
        self.cs_mode = cs_vector_arch_id != 0
        self.CS_FLAG = f"_cs{cs_vector_arch_id}" if self.cs_mode else ""
        if self.cs_mode:
            self.cs = Control_signals(cs_vector_arch_id)

        ###### Paths ######
        PROGRAM = "program"
        self.ITB_PATH = f"{obj_path}/{PROGRAM}.itb"
        self.STATES_DEC_CSV_PATH = f"{obj_path}/{PROGRAM}_encrypted{self.CS_FLAG}_states_dec.csv"
        self.EDGES_PATH = f"{obj_path}/{PROGRAM}_edges.csv"
        self.PATCHES_HEX_PATH = f"{obj_path}/{PROGRAM}_encrypted{self.CS_FLAG}_patches.mem"
        self.PATCHES_HEX_CSV_PATH = f"{obj_path}/{PROGRAM}_encrypted{self.CS_FLAG}_patches_hex.csv"
        self.SUCCESSORS_PATH = f"{obj_path}/{PROGRAM}.successors"
        self.JALR_SUCCESSORS_PATH = f"{obj_path}//{PROGRAM}_jalr_successors.csv"
        self.FILE_GET_JALR_SUCC_PATH = "a script"


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
        with open(self.ITB_PATH, 'r', encoding="utf-8") as file:
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

    def check_load_stall(self, instr, next_instr):
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

        if not os.path.exists(self.JALR_SUCCESSORS_PATH):
            raise ValueError(f"{self.JALR_SUCCESSORS_PATH} does not exist," +
                             f"please execute {self.FILE_GET_JALR_SUCC_PATH} before.")

        with open(self.JALR_SUCCESSORS_PATH, "r", encoding="utf-8") as f:
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

        with open(self.SUCCESSORS_PATH, 'w', encoding="utf-8") as file:
            file.write(patches)

    def read_states(self):
        '''
        Read state file (generated by riscv-elf-encryption). For each instruction the state used
        to encrypted  it is added as a attribute of the Instruction class.
        '''
        with open(self.STATES_DEC_CSV_PATH, 'r', encoding="utf-8") as file:
            states = file.read()

        states_list = list(states.split("\n"))

        for state_l in states_list:
            if len(state_l) > 0:
                if self.cs_mode:
                    addr_hex, addr_dec, instr, cs_vector, cs_vector_str , is_multicycle, state = list(state_l.split(",", 6))
                    self.instrs[int(addr_dec)].state = list( map(int, list(state.split(",", 4))))
                    self.instrs[int(addr_dec)].is_multicycle = is_multicycle == "1"
                    self.instrs[int(addr_dec)].cs_vector = int(cs_vector)
                    self.instrs[int(addr_dec)].cs_vector_dict = dict(zip([stage for stage in ['if', 'id', 'ex', 'wb'] if stage in list(self.cs.CS_VECTOR_ARCH.keys()) + ['if']], list(map(int, list(cs_vector_str.split('-'))))))
                else:
                    addr_hex, addr_dec, instr, state = list(state_l.split(",", 3))
                    self.instrs[int(addr_dec)].state = list(map(int, list(state.split(",", 4))))

    def add_patch_if_free(self, addr_patch, addr_src, addr_dest, disc_type='none'):
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
            if disc_type == 'b':
                addr_disc = addr_src - 8
            elif disc_type in ['jal', 'jalr']:
                addr_disc = addr_src - 4
            else:
                raise ValueError(f"Invalid disc type")


            patch = ''
            correction_str = ''
            for i in range(5):
                state1, state2 = self.instrs[addr_src].state[i], self.instrs[addr_dest].state[i]
                sub_state_patch = state1 ^ state2

                ##### PATCH FOR CYCLE AT INSTRUCTION DISCONTINUITY EXECUTION #####
                if self.cs_mode and i == 0:


                    # When a branch is in EXECUTE, even if instr in DECODE is not a multicycle instruction, 
                    # the signal we_deassert will be raised! Therefore, if the instr in DECODE was multicycle
                    # CS was already masked: nothing to do. However, if not, as mask is applied by xoring 
                    # cs_vector bits to mask to itself (as it is already in the patch through cs2cipher.
                    if disc_type == 'b': #addr_patch -> addr_src-8
                        br_corr_deassert = {}
                        br_corr_deassert['id'] = self.instrs[addr_patch+8].cs_vector_dict['id'] & (self.cs.CS_VECTOR_ALL_ONE ^ self.cs.DEASSERT_WE_MASK)
                        if 'ex' in self.cs.CS_VECTOR_ARCH.keys():
                            br_corr_deassert['ex'] = self.instrs[addr_patch+8].cs_vector_dict['ex'] ^ self.cs.CS_VECTOR_RESET
                            #br_corr_deassert['ex'] = self.instrs[addr_patch+8].cs_vector_dict['ex'] & (self.cs.CS_VECTOR_ALL_ONE ^ self.cs.DEASSERT_WE_MASK)
                        if 'wb' in self.cs.CS_VECTOR_ARCH.keys():
                            #br_corr_deassert['wb'] = self.instrs[addr_patch+8].cs_vector_dict['wb'] & self.instrs[addr_patch+8].cs_vector_dict['ex']
                            br_corr_deassert['wb'] = self.instrs[addr_patch+8].cs_vector_dict['wb'] ^ self.instrs[addr_disc].cs_vector_dict['if']
                            #br_corr_deassert['wb'] = self.instrs[addr_dest].cs_vector_dict['wb'] ^ self.instrs[addr_disc].cs_vector_dict['if']
                        brplus4_mask = self.cs.cs_vector_dict_to_xored_int(br_corr_deassert)

                        sub_state_patch ^= brplus4_mask
                        correction_str = f",{h(brplus4_mask)} ({h(br_corr_deassert['ex'])} {h(br_corr_deassert['id'])}  mask={h(self.cs.CS_VECTOR_ALL_ONE ^ self.cs.DEASSERT_WE_MASK)})"

                    # Destination of a jump is decrypted after the state get from jal decryption xor with patch, and CS from 
                    # jal in the execute (not jal-4) AND in the decode (deasserted). Therefore, the execute cs_vector
                    # must be replaced in the patch from the cs_vector of the instruction at JAL-4 to JAL cs_vector
                    if disc_type in ['jal', 'jalr']:
                        jal_ex_correction = {}
                        jal_ex_correction['id'] = 0
                        if 'ex' in self.cs.CS_VECTOR_ARCH.keys():
                            jal_ex_correction['ex'] = self.instrs[addr_src].cs_vector_dict['ex'] ^ self.instrs[addr_disc].cs_vector_dict['if'] #jal-4 ^ jal
                        if 'wb' in self.cs.CS_VECTOR_ARCH.keys():
                            jal_ex_correction['wb'] = self.instrs[addr_src].cs_vector_dict['wb'] ^ self.instrs[addr_src].cs_vector_dict['ex'] #jal-4 ^ jal
                        sub_state_patch ^= self.cs.cs_vector_dict_to_xored_int(jal_ex_correction)
                        correction_str = f",{h(jal_ex_correction['ex']):>4}({zfint(self.instrs[addr_src].cs_vector_dict['ex'],2)}^{zfint(self.instrs[addr_disc].cs_vector_dict['if'],2)})"

                patch += hex(sub_state_patch)[2:].zfill(16)

            #print(f"{hex(addr_patch)}({hex(self.instrs[addr_patch].cs_vector & 0x7f)}): {hex(addr_dest-4)}({hex(self.instrs[addr_dest-4].cs_vector & 0xff)}  {hex(((self.instrs[addr_patch].cs_vector & 0x7f) ^ self.instrs[addr_dest-4].cs_vector) & 0xff)[2:].zfill(2)}")


            ##### PATCH FOR CYCLES AFTER THE ONE OF INSTRUCTION DISCONTINUITY EXECUTION #####
            if self.cs_mode and ('wb' in self.cs.CS_VECTOR_ARCH.keys() or 'ex' in self.cs.CS_VECTOR_ARCH.keys()):
                if addr_dest+4 not in self.instrs.keys():
                    cs_corr = "0" * self.cs.PATCH_CS_HEX_WIDTH
                    correction_str += f"no dest+4"
                elif disc_type in ['jal', 'jalr'] or self.instrs[addr_patch].type == 'B': # Instruction in EX is disc deasserted not dest-4
                    if 'wb' in self.cs.CS_VECTOR_ARCH.keys():
                        #TODO: case (addr_dest+4) WB )= lw ??
                        cs_corr_cycplus1_dict = {'wb': self.instrs[addr_dest+4].cs_vector_dict['wb'], 'ex': (self.cs.CS_VECTOR_RESET) ^ (self.instrs[addr_dest+4].cs_vector_dict['ex'])} # ex only because extra patch for cs in on ex only #TODO: 'wb': self.instrs[addr_dest+4].cs_vector_dict['wb'] ^ ... (cs_disc)
                        #cs_corr_cycplus1_dict = {'wb': self.instrs[addr_dest+4].cs_vector_dict['wb'], 'ex': ((self.instrs[addr_disc].cs_vector_dict['if'] & self.cs.DEASSERT_WE_MASK) ^ (self.instrs[addr_dest+4].cs_vector_dict['ex']))} # ex only because extra patch for cs in on ex only #TODO: 'wb': self.instrs[addr_dest+4].cs_vector_dict['wb'] ^ ... (cs_disc)
                        if self.check_load_stall(self.instrs[addr_dest], self.instrs[addr_dest+4]):
                            cs_corr_cycplus2_dict = {'wb': 0}
                        else:
                            cs_corr_cycplus2_dict = {'wb': self.instrs[addr_dest+8].cs_vector_dict['wb'] ^ self.instrs[addr_disc].cs_vector_dict['if']} # todo for branch dest+12 must be corrected teh same way ? (branch is still in the WB)
                            #cs_corr_cycplus2_dict = {'wb': self.instrs[addr_dest+8].cs_vector_dict['wb'] ^ ((self.instrs[addr_disc].cs_vector_dict['if'] & self.cs.DEASSERT_WE_MASK) ^ (self.instrs[addr_dest+4].cs_vector_dict['ex']))}
                        cs_corr_int = (self.cs.cs_vector_dict_to_xored_int(cs_corr_cycplus2_dict) << (self.cs.WIDTH['wb'] + self.cs.WIDTH['ex'])) | self.cs.cs_vector_dict_to_xored_int(cs_corr_cycplus1_dict)
                    else: #only ex
                        cs_corr_cycplus1_dict = {'ex': (self.cs.CS_VECTOR_RESET) ^ (self.instrs[addr_dest+4].cs_vector_dict['ex'])}
                        #cs_corr_cycplus1_dict = {'ex': ((self.instrs[addr_disc].cs_vector_dict['if'] & self.cs.DEASSERT_WE_MASK) ^ (self.instrs[addr_dest+4].cs_vector_dict['ex']))}
                        cs_corr_int = self.cs.cs_vector_dict_to_xored_int(cs_corr_cycplus1_dict)
                    cs_corr = hex(cs_corr_int)[2:].zfill(self.cs.PATCH_CS_HEX_WIDTH)
                    correction_str += f",{cs_corr}"#,cycplus1:{hex(self.cs.cs_vector_dict_to_xored_int(cs_corr_cycplus1_dict))},cycplus2:{hex(self.cs.cs_vector_dict_to_xored_int(cs_corr_cycplus2_dict))}" (load_stall:{self.check_load_stall(self.instrs[addr_dest], self.instrs[addr_dest+4])}, {hex(self.instrs[addr_dest+8].cs_vector_dict['wb'])},{hex((self.instrs[addr_disc].cs_vector_dict['if'] & self.cs.DEASSERT_WE_MASK))}!={hex(self.instrs[addr_disc].cs_vector_dict['if'])}!={hex(self.instrs[addr_dest+4].cs_vector_dict['ex'])}"#({hex(self.cs.cs_vector_dict_to_xored_int({'wb': self.instrs[addr_disc].cs_vector_dict['if']}))}{zfint(self.instrs[addr_disc].cs_vector_dict['if'] & self.cs.DEASSERT_WE_MASK, 2)}^{zfint(self.instrs[addr_dest+4].cs_vector_dict['ex'],2)})"
                else:
                    cs_corr = "0" * self.cs.PATCH_CS_HEX_WIDTH
                patch = cs_corr + patch

            self.hex_patches_free[addr_patch >> 2] = False
            self.hex_patches[addr_patch >> 2] = patch

            patch_csv = f"{disc_type:<4},{zfint(addr_patch,5)},{zfint(addr_disc,5)},{zfint(addr_src,5)},{zfint(addr_dest,5)},{patch}{correction_str}"
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

            PATCH_WIDTH = 80 + self.cs.PATCH_CS_HEX_WIDTH if self.cs_mode else 80
            self.hex_patches = ['0' * PATCH_WIDTH] * len(self.instrs.keys())
            self.hex_patches_csv = ['    ,00000,00000,00000,00000,' + '0' * PATCH_WIDTH] * len(self.instrs.keys())
            self.hex_patches_free = [True] * len(self.instrs.keys())

            # FIRST ITERATION (Generate patches for all branch and jal)
            for addr in self.instrs:
                if addr > ADDR_ENC_BEGIN and addr != list(self.instrs.keys())[-1]:
                    for s in self.instrs[addr].successors:

                        # Generate edge file, which list all non-linear transitions
                        edges += f"{addr},{s}\n"

                        # Non-linear policy (patch generated every time a successor is not at PC+4)
                        if s != addr + 4:
                            # branch taken need 3 cycles so one instruction is loaded and decrypted from
                            # memory after a branch (thus addr + 8) 
                            if self.instrs[addr].type == 'B':
                                self.add_patch_if_free(addr, addr + 8, s, disc_type='b')

                            elif self.instrs[addr].inst == 'jal':
                                self.add_patch_if_free(addr, addr + 4, s, disc_type='jal')

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
                                self.add_patch_if_free(s, addr + 4, s, disc_type='jalr')



            # ITERATION OVER REDIRECTIONS
            addr_free = ADDR_ENC_BEGIN
            for addr in self.patches_to_be_redirected:
                addr_redirected = [0] * NB_ADDR_REDIRECTED_MAX

                # For each patch to be redirected, a free address if found and filled with the patch
                for i, s in enumerate(self.patches_to_be_redirected[addr][:NB_ADDR_REDIRECTED_MAX]):
                    while True:
                        if self.hex_patches_free[addr_free >> 2]:
                            addr_redirected[i] = addr_free
                            self.add_patch_if_free(addr_free, addr + 4, s, disc_type='jalr')
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
                if self.cs_mode:
                    self.hex_patches[addr >> 2] = "0" * self.cs.PATCH_CS_HEX_WIDTH + hex(int(REDIRECTION_TAG + redirection_field, 2))[2:]
                else:
                    self.hex_patches[addr >> 2] = hex(int(REDIRECTION_TAG + redirection_field, 2))[2:]
                self.hex_patches_csv[addr >> 2] = f"jalr,{zfint(addr,5)},{zfint(addr,5)},REDIRECTION,{self.hex_patches[addr >> 2]}"
                self.hex_patches_free[addr >> 2] = False

            with open(self.EDGES_PATH, 'w', encoding="utf-8") as file:
                file.write(edges)

            with open(self.PATCHES_HEX_CSV_PATH, 'w', encoding="utf-8") as file:
                file.write('\n'.join(self.hex_patches_csv))

            with open(self.PATCHES_HEX_PATH, 'w', encoding="utf-8") as file:
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
