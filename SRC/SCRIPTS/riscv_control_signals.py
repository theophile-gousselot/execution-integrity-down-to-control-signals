CS_VECTOR_ARCH_LIB = [{}]
CS_VECTOR_ARCH_LIB.append({'wb': ['regfile_we']})
CS_VECTOR_ARCH_LIB.append({'id': ['mult_en', 'mult_operator', 'mult_signed_mode'], 'ex': ['mult_en', 'mult_operator', 'mult_signed_mode'], 'wb': ['regfile_we']})
CS_VECTOR_ARCH_LIB.append({'id': ['alu_operator', 'alu_en', 'alu_op_a_mux_sel', 'alu_op_b_mux_sel', 'alu_op_c_mux_sel', 'regfile_we'], 'ex': ['alu_operator', 'alu_en', 'regfile_we'], 'wb': ['regfile_we']})
CS_VECTOR_ARCH_LIB.append({'id': ['rega_used_dec', 'regb_used_dec', 'regc_mux', 'regc_used_dec', 'regfile_alu_we_dec', 'regfile_alu_we'], 'ex': ['regfile_we', 'regfile_alu_we'], 'wb': ['regfile_we']})
CS_VECTOR_ARCH_LIB.append({'id': ['data_type', 'data_req', 'ctrl_transfer_target_mux_sel', 'ctrl_transfer_insn_in_dec', 'ctrl_transfer_insn_in_id', 'csr_status', 'csr_access', 'alu_bmask_b_mux_sel', 'alu_op_a_mux_sel', 'regfile_we'], 'ex': ['data_type', 'data_req', 'csr_access', 'alu_operator', 'alu_en', 'regfile_we'], 'wb': ['regfile_we']})
CS_VECTOR_ARCH_LIB.append({'id': ['regfile_alu_we'], 'ex': ['regfile_alu_we'], 'wb': ['regfile_we']})
CS_VECTOR_ARCH_LIB.append({'id': ['imm_a_mux_sel', 'imm_b_mux_sel', 'data_type', 'data_sign_ext', 'data_we', 'data_req', 'regfile_we'], 'ex': ['data_type', 'data_sign_ext', 'data_we', 'data_req', 'alu_en', 'regfile_we'], 'wb': ['regfile_we', 'data_type', 'data_sign_ext', 'data_we']})
CS_VECTOR_ARCH_LIB.append({'id': ['data_we'], 'ex': ['data_we'], 'wb': ['data_we']})
CS_VECTOR_ARCH_LIB.append({'id': ['alu_operator', 'alu_en'], 'wb': ['regfile_we']})
#ok: CS_VECTOR_ARCH_LIB.append({'id': ['alu_operator', 'alu_en', 'regfile_we'], 'ex': ['alu_operator', 'regfile_we'], 'wb': ['regfile_we']})
#CS_VECTOR_ARCH_LIB.append({'id': ['data_type', 'data_sign_ext', 'data_req', 'ctrl_transfer_target_mux_sel', 'ctrl_transfer_insn_in_dec', 'ctrl_transfer_insn_in_id', 'csr_status', 'csr_access', 'alu_bmask_b_mux_sel', 'alu_op_a_mux_sel', 'regfile_we'], 'ex': ['data_req', 'csr_access', 'alu_operator', 'alu_en', 'regfile_we'], 'wb': ['regfile_we']})



# todo: function to count cs valid (add usefull/notusefull in cs dicts), count width, count cs per stage, etc...



#problem with this one: CS_VECTOR_ARCH_LIB.append({'id': ['alu_operator', 'alu_en', 'alu_op_a_mux_sel', 'regfile_we'], 'ex': ['alu_operator', 'alu_en', 'regfile_we', 'regfile_alu_we'], 'wb': ['regfile_we']})

SIGNAL_DESCRIPTION = {}
SIGNAL_DESCRIPTION['alu_bmask_a_mux_sel']          = {'used': False, 'width': 1, 'position_dec_tab': 119, 'stages': ['id'], 'reset_val': 0b1} # useful only if PULP_XPULP
SIGNAL_DESCRIPTION['alu_bmask_b_mux_sel']          = {'used': False, 'width': 1, 'position_dec_tab': 118, 'stages': ['id'], 'reset_val': 0b1} # useful only if PULP_XPULP
SIGNAL_DESCRIPTION['alu_en']                       = {'used': True, 'width': 1, 'position_dec_tab': 117, 'stages': ['id', 'ex'], 'reset_val': 0b0, 'id_invalid_ex_ready': 0b1}
SIGNAL_DESCRIPTION['alu_op_a_mux_sel']             = {'used': True, 'width': 3, 'position_dec_tab': 114, 'stages': ['id'], 'reset_val': 0b0}
SIGNAL_DESCRIPTION['alu_op_b_mux_sel']             = {'used': True, 'width': 3, 'position_dec_tab': 111, 'stages': ['id'], 'reset_val': 0b0}
SIGNAL_DESCRIPTION['alu_op_c_mux_sel']             = {'used': True, 'width': 2, 'position_dec_tab': 109, 'stages': ['id'], 'reset_val': 0b0}
SIGNAL_DESCRIPTION['alu_operator']                 = {'used': True, 'width': 7, 'position_dec_tab': 102, 'stages': ['id', 'ex'], 'reset_val': 0b11, 'id_invalid_ex_ready': 0b11, 'ex_en':'alu_en'}
SIGNAL_DESCRIPTION['alu_vec_mode']                 = {'used': False, 'width': 2, 'position_dec_tab': 100} # useful only if FPU
SIGNAL_DESCRIPTION['apu_en']                       = {'used': False, 'width': 1, 'position_dec_tab': 99} # useful only if FPU
SIGNAL_DESCRIPTION['apu_lat']                      = {'used': False, 'width': 2, 'position_dec_tab': 97} # useful only if FPU
SIGNAL_DESCRIPTION['apu_op']                       = {'used': False, 'width': 6, 'position_dec_tab': 91} # useful only if FPU
SIGNAL_DESCRIPTION['atop']                         = {'used': False, 'width': 6, 'position_dec_tab': 85} # useful only if A (ATOMIC)
SIGNAL_DESCRIPTION['bmask_a_mux']                  = {'used': False, 'width': 1, 'position_dec_tab': 84} # useful only if PULP_XPULP
SIGNAL_DESCRIPTION['bmask_b_mux']                  = {'used': False, 'width': 2, 'position_dec_tab': 82} # useful only if PULP_XPULP
SIGNAL_DESCRIPTION['csr_access']                   = {'used': True, 'width': 1, 'position_dec_tab': 81, 'stages': ['id', 'ex'], 'reset_val': 0b0}
SIGNAL_DESCRIPTION['csr_op']                       = {'used': False, 'width': 2, 'position_dec_tab': 79, 'stages': ['id', 'ex'], 'reset_val': 0b0, 'id_invalid_ex_ready': 0b0} #problem csr_status_i=1 => flush_ex => halt_id => id_valid = 0 => id_invalid_ex_ready (but in soft modelization id_invalid do not depend on other thing that load_stall...)
SIGNAL_DESCRIPTION['csr_status']                   = {'used': True, 'width': 1, 'position_dec_tab': 78, 'stages': ['id'], 'reset_val': 0b0}
SIGNAL_DESCRIPTION['ctrl_transfer_insn_in_dec']    = {'used': True, 'width': 2, 'position_dec_tab': 76, 'stages': ['id']}
SIGNAL_DESCRIPTION['ctrl_transfer_insn_in_id']     = {'used': True, 'width': 2, 'position_dec_tab': 74, 'stages': ['id']}
SIGNAL_DESCRIPTION['ctrl_transfer_target_mux_sel'] = {'used': True, 'width': 2, 'position_dec_tab': 72, 'stages': ['id'], 'reset_val': 0b01}
SIGNAL_DESCRIPTION['data_load_event']           = {'used': False, 'width': 1, 'position_dec_tab': 71} # useful only if PULP_CLUSTER
SIGNAL_DESCRIPTION['data_reg_offset']           = {'used': False, 'width': 2, 'position_dec_tab': 69} # cte to 0
SIGNAL_DESCRIPTION['data_req']                  = {'used': True, 'width': 1, 'position_dec_tab': 68, 'stages': ['id', 'ex'], 'reset_val': 0b0, 'id_invalid_ex_ready': 0b0}
SIGNAL_DESCRIPTION['data_sign_ext']             = {'used': True, 'width': 2, 'position_dec_tab': 66, 'stages': ['id', 'ex', 'wb'], 'reset_val': 0b0, 'ex_en': 'data_req', 'id_invalid_ex_ready': 0b0} # pb when used in execute
SIGNAL_DESCRIPTION['data_type']                 = {'used': True, 'width': 2, 'position_dec_tab': 64, 'stages': ['id', 'ex', 'wb'], 'reset_val': 0b0, 'ex_en': 'data_req', 'id_invalid_ex_ready': 0b0} # pb when used in execute# must be valid to WB
SIGNAL_DESCRIPTION['data_we']                   = {'used': True, 'width': 1, 'position_dec_tab': 63, 'stages': ['id', 'ex', 'wb'], 'reset_val': 0b0, 'ex_en': 'data_req', 'wb_en': 'data_req', 'id_invalid_ex_ready': 0b0}
SIGNAL_DESCRIPTION['dret_dec']                     = {'used': False, 'width': 1, 'position_dec_tab': 62, 'stages': ['id']} # useful only if debug mode
SIGNAL_DESCRIPTION['dret_insn_dec']                = {'used': False, 'width': 1, 'position_dec_tab': 61, 'stages': ['id']} # useful only if debug mode
SIGNAL_DESCRIPTION['ebrk_insn_dec']                = {'used': False, 'width': 1, 'position_dec_tab': 60, 'stages': ['id']} # useful only if debug mode
SIGNAL_DESCRIPTION['ecall_insn_dec']               = {'used': False, 'width': 1, 'position_dec_tab': 59, 'stages': ['id']} # useful only if debug mode
SIGNAL_DESCRIPTION['fencei_insn_dec']              = {'used': False, 'width': 1, 'position_dec_tab': 58, 'stages': ['id']} # useful only if debug mode
SIGNAL_DESCRIPTION['fp_rnd_mode']                  = {'used': False, 'width': 3, 'position_dec_tab': 55, 'stages': ['id']} # useful only if FPU 
SIGNAL_DESCRIPTION['fpu_dst_fmt']                  = {'used': False, 'width': 3, 'position_dec_tab': 52, 'stages': ['id']} # useful only if FPU 
SIGNAL_DESCRIPTION['fpu_int_fmt']                  = {'used': False, 'width': 2, 'position_dec_tab': 50, 'stages': ['id']} # useful only if FPU 
SIGNAL_DESCRIPTION['fpu_src_fmt']                  = {'used': False, 'width': 3, 'position_dec_tab': 47, 'stages': ['id']} # useful only if FPU 
SIGNAL_DESCRIPTION['hwlp_cnt_mux_sel']             = {'used': False, 'width': 1, 'position_dec_tab': 46, 'stages': ['id']} # useful only if HWLP 
SIGNAL_DESCRIPTION['hwlp_start_mux_sel']           = {'used': False, 'width': 1, 'position_dec_tab': 45, 'stages': ['id']} # useful only if HWLP 
SIGNAL_DESCRIPTION['hwlp_target_mux_sel']          = {'used': False, 'width': 1, 'position_dec_tab': 44, 'stages': ['id']} # useful only if HWLP 
SIGNAL_DESCRIPTION['hwlp_we_int']                  = {'used': False, 'width': 3, 'position_dec_tab': 41, 'stages': ['id']} # useful only if HWLP 
SIGNAL_DESCRIPTION['illegal_insn_dec']             = {'used': False, 'width': 1, 'position_dec_tab': 40} # not useful to include illegal insn as it must be always bi high, except under attack
SIGNAL_DESCRIPTION['imm_a_mux_sel']                = {'used': True, 'width': 1, 'position_dec_tab': 39, 'stages': ['id'], 'reset_val': 0b1}
SIGNAL_DESCRIPTION['imm_b_mux_sel']                = {'used': True, 'width': 4, 'position_dec_tab': 35, 'stages': ['id'], 'reset_val': 0b0}
SIGNAL_DESCRIPTION['is_clpx']                      = {'used': False, 'width': 1, 'position_dec_tab': 34} # cte to 0
SIGNAL_DESCRIPTION['is_subrot']                    = {'used': False, 'width': 1, 'position_dec_tab': 33} # cte to 0
SIGNAL_DESCRIPTION['mret_dec']                     = {'used': False, 'width': 1, 'position_dec_tab': 32} # useful only if debug mode
SIGNAL_DESCRIPTION['mret_insn_dec']                = {'used': False, 'width': 1, 'position_dec_tab': 31} # useful only if debug mode
SIGNAL_DESCRIPTION['mult_dot_en']                  = {'used': False, 'width': 1, 'position_dec_tab': 30} # useful only if PULP_XPULP
SIGNAL_DESCRIPTION['mult_dot_signed']              = {'used': False, 'width': 2, 'position_dec_tab': 28} # useful only if PULP_XPULP
SIGNAL_DESCRIPTION['mult_imm_mux']                 = {'used': False, 'width': 1, 'position_dec_tab': 27, 'stages': ['id'], 'reset_val': 0b0} # useful only if PULP_XPULP
SIGNAL_DESCRIPTION['mult_en']                  = {'used': True, 'width': 1, 'position_dec_tab': 26, 'stages': ['id', 'ex'], 'reset_val': 0b0, 'id_invalid_ex_ready': 0b0}
SIGNAL_DESCRIPTION['mult_operator']                = {'used': True, 'width': 3, 'position_dec_tab': 23, 'stages': ['id', 'ex'], 'reset_val': 0b10, 'id_invalid_ex_ready': 0b10, 'ex_en':'mult_en'}
SIGNAL_DESCRIPTION['mult_sel_subword']             = {'used': False, 'width': 1, 'position_dec_tab': 22} # useful only if PULP_XPULP
SIGNAL_DESCRIPTION['mult_signed_mode']             = {'used': True, 'width': 2, 'position_dec_tab': 20, 'stages': ['id', 'ex'], 'reset_val': 0b0, 'id_invalid_ex_ready': 0b0, 'ex_en':'mult_en'}
SIGNAL_DESCRIPTION['prepost_useincr']              = {'used': False, 'width': 1, 'position_dec_tab': 19} # useful only if PULP_XPULP
SIGNAL_DESCRIPTION['rega_used_dec']                = {'used': True, 'width': 1, 'position_dec_tab': 18, 'stages': ['id'], 'reset_val': 0b0}
SIGNAL_DESCRIPTION['regb_used_dec']                = {'used': True, 'width': 1, 'position_dec_tab': 17, 'stages': ['id'], 'reset_val': 0b0}
SIGNAL_DESCRIPTION['regc_mux']                     = {'used': True, 'width': 2, 'position_dec_tab': 15, 'stages': ['id'], 'reset_val': 0b11}
SIGNAL_DESCRIPTION['regc_used_dec']                = {'used': True, 'width': 1, 'position_dec_tab': 14, 'stages': ['id'], 'reset_val': 0b0}
SIGNAL_DESCRIPTION['regfile_alu_waddr_mux_sel']    = {'used': False, 'width': 1, 'position_dec_tab': 13, 'stages': ['id'], 'reset_val': 0b1} # cte to 1 # useful only if PULP_XPULP
SIGNAL_DESCRIPTION['regfile_alu_we_dec']        = {'used': True, 'width': 1, 'position_dec_tab': 12, 'stages': ['id'], 'reset_val': 0b0} # (same as regfile_alu_we, but propagated only to controller) alu we to detect load_stall
SIGNAL_DESCRIPTION['regfile_alu_we']            = {'used': True, 'width': 1, 'position_dec_tab': 11, 'stages': ['id', 'ex'], 'reset_val': 0b0, 'id_invalid_ex_ready': 0b0} # regfile_alu_we 
SIGNAL_DESCRIPTION['regfile_fp_a']                 = {'used': False, 'width': 1, 'position_dec_tab': 10} # useful only if FPU
SIGNAL_DESCRIPTION['regfile_fp_b']                 = {'used': False, 'width': 1, 'position_dec_tab': 9} # useful only if FPU
SIGNAL_DESCRIPTION['regfile_fp_c']                 = {'used': False, 'width': 1, 'position_dec_tab': 8} # useful only if FPU
SIGNAL_DESCRIPTION['regfile_fp_d']                 = {'used': False, 'width': 1, 'position_dec_tab': 7} # useful only if FPU
SIGNAL_DESCRIPTION['regfile_we']                   = {'used': True, 'width': 1, 'position_dec_tab': 6, 'stages': ['id', 'ex', 'wb'], 'reset_val': 0b0, 'id_invalid_ex_ready': 0b0, 'ex_invalid_wb_ready': 0b0} # regfile_mem_we -> we_a
SIGNAL_DESCRIPTION['scalar_replication']           = {'used': False, 'width': 1, 'position_dec_tab': 5} # useful only if FPU
SIGNAL_DESCRIPTION['scalar_replication_c']         = {'used': False, 'width': 1, 'position_dec_tab': 4} # useful only if FPU
SIGNAL_DESCRIPTION['uret_dec']                     = {'used': False, 'width': 1, 'position_dec_tab': 3} # useful only if uret
SIGNAL_DESCRIPTION['uret_insn_dec']                = {'used': False, 'width': 1, 'position_dec_tab': 2} # useful only if uret
SIGNAL_DESCRIPTION['wfi_insn_dec']                 = {'used': False, 'width': 1, 'position_dec_tab': 1} # wfi
SIGNAL_DESCRIPTION['null']                         = {'used': False, 'width': 1, 'position_dec_tab': 0}


SIGNAL_BUILD_AFTER_DECODER = ['branch_in_ex']



DEASSERT_WE_AFFECTED_SIGNALS = ['alu_en', 'apu_en', 'mult_en', 'mult_dot_en', 'regfile_we', 'regfile_alu_we', 'data_req', 'hwlp_we', 'csr_op', 'ctrl_transfer_insn_in_id']

#if not 'data_req_id'  thus:  data_load_event_ex_o <= 1'b0;


EN_AFFECTED_SIGNALS = {
    'alu_en': ['alu_operator', 'alu_operand_a', 'alu_operand_b', 'alu_operand_c',
               'bmask_a', 'bmask_b', 'imm_vec_ext', 'alu_vec_mode',
               'is_clpx', 'alu_clpx_shift', 'is_subrot'],
    'mult_en': ['mult_operator', 'mult_sel_subword', 'mult_signed_mode',
                    'alu_operand_a', 'alu_operand_b', 'alu_operand_c', 'mult_imm'],
    'mult_dot_en': ['mult_operator', 'mult_dot_signed', 'alu_operand_a', 'alu_operand_b',
                    'alu_operand_c', 'is_clpx', 'clpx_shift_ex_o', 'clpx_img_ex_o'],
    'apu_en': ['apu_op', 'apu_lat', 'apu_operands', 'apu_flags', 'apu_waddr'],
    'regfile_we': ['regfile_waddr'],
    'regfile_alu_we': ['regfile_alu_waddr'],
    'data_req': ['data_we', 'data_type', 'data_sign_ext',
                    'data_reg_offset', 'data_load_event', 'atop']}



class Control_signals:
    def __init__(self, cs_vector_arch_id):
        self.cs_vector_arch_id = cs_vector_arch_id
        self.SIGNAL_DESCRIPTION = SIGNAL_DESCRIPTION
        self.CS_VECTOR_ARCH = CS_VECTOR_ARCH_LIB[cs_vector_arch_id]
        self.SIGNAL_SET = self.gen_signal_set()
        self.CS_VECTOR_DESCRIPTION = self.gen_cs_vector_description(self.SIGNAL_SET)
        self.DEASSERT_WE_MASK = self.gen_deassert_we_mask()
        self.CS_VECTOR_RESET = self.gen_cs_vector_reset()
        self.CS_VECTOR_WIDTH = self.count_cs_vector_width()
        self.CS_VECTOR_ALL_ONE = (1 << self.CS_VECTOR_WIDTH) - 1
        self.CS_VECTOR_ID_INVALID_EX_READY, self.MASK_CS_VECTOR_ID_INVALID_EX_READY = self.gen_mask_cs_vector_stage_invalid_next_stage_ready('id_invalid_ex_ready')
        self.CS_VECTOR_EX_INVALID_WB_READY, self.MASK_CS_VECTOR_EX_INVALID_WB_READY = self.gen_mask_cs_vector_stage_invalid_next_stage_ready('ex_invalid_wb_ready')
        self.CS_VECTOR_DESCRIPTION = self.gen_cs_vector_description(self.SIGNAL_SET)
        self.WIDTH = self.count_all_stage_width()

        self.PATCH_CS_HEX_WIDTH = self.count_patch_cs_hex_width()

    def stats_on_cs(self):
        cs_used, cs_not_used = 0, 0
        cs_used_width, cs_not_used_width = 0, 0
        cs_used_id, cs_used_ex, cs_used_wb = 0, 0, 0
        cs_used_id_width, cs_used_ex_width, cs_used_wb_width = 0, 0, 0
        for cs in self.SIGNAL_DESCRIPTION.keys():
            if self.SIGNAL_DESCRIPTION[cs]['used']:
                cs_used += 1
                cs_used_width += self.SIGNAL_DESCRIPTION[cs]['width']
                if self.SIGNAL_DESCRIPTION[cs]['stages'] == ['id']:
                    cs_used_id += 1
                    cs_used_id_width += self.SIGNAL_DESCRIPTION[cs]['width']
                elif self.SIGNAL_DESCRIPTION[cs]['stages'] == ['id', 'ex']:
                    cs_used_ex += 1
                    cs_used_ex_width += self.SIGNAL_DESCRIPTION[cs]['width']
                elif self.SIGNAL_DESCRIPTION[cs]['stages'] == ['id', 'ex', 'wb']:
                    cs_used_wb += 1
                    cs_used_wb_width += self.SIGNAL_DESCRIPTION[cs]['width']
                else:
                    raise ValueError(f'Invalid stages for {cs}.')

            else:
                cs_not_used += 1
                cs_not_used_width += self.SIGNAL_DESCRIPTION[cs]['width']
        print(f"Number of CS:          {cs_used + cs_not_used:>4}")
        print(f"Width of CS:           {cs_used_width + cs_not_used_width:>4} bits")
        print(f"Number of CS used:     {cs_used:>4}")
        print(f"Width of CS used:      {cs_used_width:>4} bits")
        print(f"Number of CS not used: {cs_not_used:>4}")
        print(f"Width of CS not used:  {cs_not_used_width:>4} bits")
        print(f"#### ABOUT USED SIGNALS ####")
        print(f"Number of CS in ID only:    { cs_used_id:>4}")
        print(f"Width of CS in ID only:     { cs_used_id_width:>4} bits")
        print(f"Number of CS in ID/EX only: { cs_used_ex:>4}")
        print(f"Width of CS in ID/EX only:  { cs_used_ex_width:>4} bits")
        print(f"Number of CS in ID/EX/WB:   { cs_used_wb:>4}")
        print(f"Width of CS in ID/EX/WB:    { cs_used_wb_width:>4} bits")

    def count_patch_cs_hex_width(self):
        width = 0
        if 'wb' in self.CS_VECTOR_ARCH.keys():
            width += 2*self.WIDTH['wb'] 
        if 'ex' in self.CS_VECTOR_ARCH.keys():
            width += self.WIDTH['ex'] 
        width_hex = ((width - 1)//4) + 1
        return(width_hex)

    def count_all_stage_width(self):
        width_dict = {}
        for stage in ['id', 'ex', 'wb']:
            width_dict[stage] = self.count_stage_width(stage)
        return width_dict

    def extract(self, integer, position, width):
        return ((integer >> position) & ((1 << width) - 1))

    def gen_signal_set(self):
        signal_set = []
        for stage in self.CS_VECTOR_ARCH.keys():
            for cs in self.CS_VECTOR_ARCH[stage]:
                # check signal reach this stage in microarchitecture (e.g., alu_operator is usefull in execute
                # stage, thus it is accessible in decode and excute but not in write-back
                if stage not in self.SIGNAL_DESCRIPTION[cs]['stages']: 
                    raise ValueError(f'Invalid CS_VECTOR_ARCH, {cs} is not available in stage {stage}. Please edit CS_VECTOR_ARCH_LIB.')

                if cs not in signal_set:
                    signal_set.append(cs)

        for cs in ['alu_en', 'mult_en', 'data_req']:
            if cs not in signal_set:
                signal_set.append(cs)
        signal_set.reverse()
        return signal_set


    def gen_cs_vector_description(self, signal_set):
        cs_vector_description = {}
        position = 0
        for cs_name in signal_set:
            cs_vector_description[cs_name]=self.SIGNAL_DESCRIPTION[cs_name]
            cs_vector_description[cs_name]['position']= position
            position += cs_vector_description[cs_name]['width']
        return cs_vector_description


    def gen_deassert_we_mask(self):
        mask = 0
        for cs in self.CS_VECTOR_DESCRIPTION:
            if cs not in DEASSERT_WE_AFFECTED_SIGNALS:
                mask |= ((1 << self.CS_VECTOR_DESCRIPTION[cs]['width']) - 1) << self.CS_VECTOR_DESCRIPTION[cs]['position']
        return mask

    def gen_cs_vector_reset(self):
        cs_vector_reset = 0
        for cs in self.CS_VECTOR_DESCRIPTION:
            if 'reset_val' in self.CS_VECTOR_DESCRIPTION[cs].keys():
                reset_val = self.CS_VECTOR_DESCRIPTION[cs]['reset_val'] 
            else:
                reset_val = 0
            cs_vector_reset |= reset_val << (self.CS_VECTOR_DESCRIPTION[cs]['position'])
        return(cs_vector_reset)


    def count_cs_vector_width(self):
        cs_vector_width = 0
        for cs in self.CS_VECTOR_DESCRIPTION:
            cs_vector_width += self.CS_VECTOR_DESCRIPTION[cs]['width']
        return(cs_vector_width)


    def gen_mask_cs_vector_stage_invalid_next_stage_ready(self, stage_invalid_next_stage_ready):
        cs_vector_id_invalid_ex_ready = 0
        mask_cs_vector_id_invalid_ex_ready = 0
        for cs in self.CS_VECTOR_DESCRIPTION:
            if stage_invalid_next_stage_ready in self.CS_VECTOR_DESCRIPTION[cs].keys():
                cs_vector_id_invalid_ex_ready |= self.CS_VECTOR_DESCRIPTION[cs][stage_invalid_next_stage_ready] << self.CS_VECTOR_DESCRIPTION[cs]['position']
            else:
                mask_cs_vector_id_invalid_ex_ready |= ((1 << self.CS_VECTOR_DESCRIPTION[cs]['width']) - 1) << self.CS_VECTOR_DESCRIPTION[cs]['position']
        return(cs_vector_id_invalid_ex_ready, mask_cs_vector_id_invalid_ex_ready)


    def count_stage_width(self, stage):
        width = 0
        if stage not in self.CS_VECTOR_ARCH.keys():
            width = 0
        else:
            for cs in self.CS_VECTOR_ARCH[stage]:
                width += self.SIGNAL_DESCRIPTION[cs]['width']
        return (width)



    def extract_cs(self, cs_vector, cs):
        return ((cs_vector >> self.CS_VECTOR_DESCRIPTION[cs]['position']) & self.CS_VECTOR_DESCRIPTION[cs]['width'])

    def cs_vector_dict_to_xored_int(self, cs_vector_dict):
        cs_vector_reduced = 0
        for stage in ['wb','ex','id']:
            if stage in cs_vector_dict.keys() and stage in self.CS_VECTOR_ARCH:
                for cs in self.CS_VECTOR_ARCH[stage]:
                    cs_vector_reduced <<= self.CS_VECTOR_DESCRIPTION[cs]['width']
                    cs_vector_reduced |= (cs_vector_dict[stage] >> self.CS_VECTOR_DESCRIPTION[cs]['position']) & ((1 << self.CS_VECTOR_DESCRIPTION[cs]['width']) - 1)
        return(cs_vector_reduced)



    def cs_vector_xored_dict_to_xored_int(self, cs_vector_xored_dict):
        cs_vector_xored_int = 0
        for stage in ['wb', 'ex', 'id']:
            if stage in cs_vector_xored_dict.keys():
                width = 0
                for cs in self.CS_VECTOR_ARCH[stage]:
                    width += self.SIGNAL_DESCRIPTION[cs]['width']
                cs_vector_xored_int <<= width
                cs_vector_xored_int |= cs_vector_xored_dict[stage]
        return(cs_vector_xored_int)



    def cs_vector_xored_int_to_dict(self, cs_vector_xored_int):
        cs_vector_dict = {}
        for stage in ['id', 'ex', 'wb']:
            if stage in self.CS_VECTOR_ARCH.keys():
                cs_vector_dict[stage] = 0
                for cs in self.CS_VECTOR_ARCH[stage]:
                    cs_vector_dict[stage] <<= self.CS_VECTOR_DESCRIPTION[cs]['width']
                    cs_vector_dict[stage] |= cs_vector_xored_int & ((1 << self.CS_VECTOR_DESCRIPTION[cs]['width']) - 1)
                cs_vector_xored_int >>= width
        return (cs_vector_xored_dict)



    def make_mask_ex_en(self, cs_vector_id):
        mask = 0
        mask_for_id = 0
        mask_for_reset = 0
        for cs in self.CS_VECTOR_DESCRIPTION:
            if not 'ex_en' in self.CS_VECTOR_DESCRIPTION[cs]:
                mask |= ((1 << self.CS_VECTOR_DESCRIPTION[cs]['width']) - 1) << self.CS_VECTOR_DESCRIPTION[cs]['position']
                mask_for_id |= ((1 << self.CS_VECTOR_DESCRIPTION[cs]['width']) - 1) << self.CS_VECTOR_DESCRIPTION[cs]['position']
            else:
                en_ex = (cs_vector_id >> self.CS_VECTOR_DESCRIPTION[self.CS_VECTOR_DESCRIPTION[cs]['ex_en']]['position']) & 1
                if en_ex == 1:
                    mask |= ((1 << self.CS_VECTOR_DESCRIPTION[cs]['width']) - 1) << self.CS_VECTOR_DESCRIPTION[cs]['position']
                    mask_for_id |= ((1 << self.CS_VECTOR_DESCRIPTION[cs]['width']) - 1) << self.CS_VECTOR_DESCRIPTION[cs]['position']
                else:
                    mask_for_reset |= ((1 << self.CS_VECTOR_DESCRIPTION[cs]['width']) - 1) << self.CS_VECTOR_DESCRIPTION[cs]['position']
        return (mask_for_id, mask_for_reset)
        #return mask


    def make_mask_wb_en(self, cs_vector_ex):
        mask = 0
        mask_for_ex = 0
        mask_for_reset = 0
        for cs in self.CS_VECTOR_DESCRIPTION:
            if not 'wb_en' in self.CS_VECTOR_DESCRIPTION[cs]:
                mask_for_ex |= ((1 << self.CS_VECTOR_DESCRIPTION[cs]['width']) - 1) << self.CS_VECTOR_DESCRIPTION[cs]['position']
            else:
                en_wb = (cs_vector_ex >> self.CS_VECTOR_DESCRIPTION[self.CS_VECTOR_DESCRIPTION[cs]['wb_en']]['position']) & 1
                if en_wb == 1:
                    mask_for_ex |= ((1 << self.CS_VECTOR_DESCRIPTION[cs]['width']) - 1) << self.CS_VECTOR_DESCRIPTION[cs]['position']
                else:
                    mask_for_reset |= ((1 << self.CS_VECTOR_DESCRIPTION[cs]['width']) - 1) << self.CS_VECTOR_DESCRIPTION[cs]['position']
        return (mask_for_ex, mask_for_reset)
        #return mask



    def decode_tab_to_cs_vector(self, cs_decode_table):
        cs_vector = 0
        for cs_name in self.CS_VECTOR_DESCRIPTION.keys():
            cs_vector |= self.extract(cs_decode_table, self.CS_VECTOR_DESCRIPTION[cs_name]['position_dec_tab'], self.CS_VECTOR_DESCRIPTION[cs_name]['width']) << self.CS_VECTOR_DESCRIPTION[cs_name]['position']
        return cs_vector




    def read_decoding_table(self, cs_path):
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
        with open(cs_path, "r") as file:
            cs_file = file.read()
        cs_file_list = list(filter(('').__ne__, list(cs_file.split('\n'))))

        cs_decoder = []
        for fct7_3_opcode in range(len(cs_file_list)):
            cs_file_line = list(cs_file_list[fct7_3_opcode].split(','))
            if int(cs_file_line[1], 16) != fct7_3_opcode:
                raise ValueError(f'Error, {cs_path} is bad-formated.')
            cs_decoder.append({'cs_vector': (int(cs_file_line[2], 16) << (56+8)) | ( int(cs_file_line[3], 16) << 8) | int(cs_file_line[4], 16),
                'is_multicycle': int(cs_file_line[5]), 'is_div': int(cs_file_line[6]), 'ctrl_transfer': int(cs_file_line[7])})
        return (cs_decoder)


