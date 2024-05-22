CS_VECTOR_ARCH = {'id': ['alu_operator', 'alu_en'], 'ex': ['alu_operator', 'alu_en']}


SIGNAL_DESCRIPTION = {}
SIGNAL_DESCRIPTION['alu_bmask_a_mux_sel']          = {'width': 1, 'position_dec_tab': 119}
SIGNAL_DESCRIPTION['alu_bmask_b_mux_sel']          = {'width': 1, 'position_dec_tab': 118}
SIGNAL_DESCRIPTION['alu_en']                       = {'width': 1, 'position_dec_tab': 117, 'reset_val': 0b0, 'id_invalid_ex_ready': 0b1}
SIGNAL_DESCRIPTION['alu_op_a_mux_sel']             = {'width': 3, 'position_dec_tab': 114}
SIGNAL_DESCRIPTION['alu_op_b_mux_sel']             = {'width': 3, 'position_dec_tab': 111}
SIGNAL_DESCRIPTION['alu_op_c_mux_sel']             = {'width': 2, 'position_dec_tab': 109}
SIGNAL_DESCRIPTION['alu_operator']                 = {'width': 7, 'position_dec_tab': 102,  'reset_val': 0b11, 'id_invalid_ex_ready': 0b11, 'ex_en':'alu_en'}
SIGNAL_DESCRIPTION['alu_vec_mode']                 = {'width': 2, 'position_dec_tab': 100}
SIGNAL_DESCRIPTION['apu_en']                       = {'width': 1, 'position_dec_tab': 99}
SIGNAL_DESCRIPTION['apu_lat']                      = {'width': 2, 'position_dec_tab': 97}
SIGNAL_DESCRIPTION['apu_op']                       = {'width': 6, 'position_dec_tab': 91}
SIGNAL_DESCRIPTION['atop_id']                      = {'width': 6, 'position_dec_tab': 85}
SIGNAL_DESCRIPTION['bmask_a_mux']                  = {'width': 1, 'position_dec_tab': 84}
SIGNAL_DESCRIPTION['bmask_b_mux']                  = {'width': 2, 'position_dec_tab': 82}
SIGNAL_DESCRIPTION['csr_access']                   = {'width': 1, 'position_dec_tab': 81}
SIGNAL_DESCRIPTION['csr_op']                       = {'width': 2, 'position_dec_tab': 79}
SIGNAL_DESCRIPTION['csr_status']                   = {'width': 1, 'position_dec_tab': 78}
SIGNAL_DESCRIPTION['ctrl_transfer_insn_in_dec']    = {'width': 2, 'position_dec_tab': 76}
SIGNAL_DESCRIPTION['ctrl_transfer_insn_in_id']     = {'width': 2, 'position_dec_tab': 74}
SIGNAL_DESCRIPTION['ctrl_transfer_target_mux_sel'] = {'width': 2, 'position_dec_tab': 72}
SIGNAL_DESCRIPTION['data_load_event_id']           = {'width': 1, 'position_dec_tab': 71}
SIGNAL_DESCRIPTION['data_reg_offset_id']           = {'width': 2, 'position_dec_tab': 69}
SIGNAL_DESCRIPTION['data_req_id']                  = {'width': 1, 'position_dec_tab': 68}
SIGNAL_DESCRIPTION['data_sign_ext_id']             = {'width': 2, 'position_dec_tab': 66}
SIGNAL_DESCRIPTION['data_type_id']                 = {'width': 2, 'position_dec_tab': 64}
SIGNAL_DESCRIPTION['data_we_id']                   = {'width': 1, 'position_dec_tab': 63}
SIGNAL_DESCRIPTION['dret_dec']                     = {'width': 1, 'position_dec_tab': 62}
SIGNAL_DESCRIPTION['dret_insn_dec']                = {'width': 1, 'position_dec_tab': 61}
SIGNAL_DESCRIPTION['ebrk_insn_dec']                = {'width': 1, 'position_dec_tab': 60}
SIGNAL_DESCRIPTION['ecall_insn_dec']               = {'width': 1, 'position_dec_tab': 59}
SIGNAL_DESCRIPTION['fencei_insn_dec']              = {'width': 1, 'position_dec_tab': 58}
SIGNAL_DESCRIPTION['fp_rnd_mode']                  = {'width': 3, 'position_dec_tab': 55}
SIGNAL_DESCRIPTION['fpu_dst_fmt']                  = {'width': 3, 'position_dec_tab': 52}
SIGNAL_DESCRIPTION['fpu_int_fmt']                  = {'width': 2, 'position_dec_tab': 50}
SIGNAL_DESCRIPTION['fpu_src_fmt']                  = {'width': 3, 'position_dec_tab': 47}
SIGNAL_DESCRIPTION['hwlp_cnt_mux_sel']             = {'width': 1, 'position_dec_tab': 46}
SIGNAL_DESCRIPTION['hwlp_start_mux_sel']           = {'width': 1, 'position_dec_tab': 45}
SIGNAL_DESCRIPTION['hwlp_target_mux_sel']          = {'width': 1, 'position_dec_tab': 44}
SIGNAL_DESCRIPTION['hwlp_we_int']                  = {'width': 3, 'position_dec_tab': 41}
SIGNAL_DESCRIPTION['illegal_insn_dec']             = {'width': 1, 'position_dec_tab': 40}
SIGNAL_DESCRIPTION['imm_a_mux_sel']                = {'width': 1, 'position_dec_tab': 39}
SIGNAL_DESCRIPTION['imm_b_mux_sel']                = {'width': 4, 'position_dec_tab': 35}
SIGNAL_DESCRIPTION['is_clpx']                      = {'width': 1, 'position_dec_tab': 34}
SIGNAL_DESCRIPTION['is_subrot']                    = {'width': 1, 'position_dec_tab': 33}
SIGNAL_DESCRIPTION['mret_dec']                     = {'width': 1, 'position_dec_tab': 32}
SIGNAL_DESCRIPTION['mret_insn_dec']                = {'width': 1, 'position_dec_tab': 31}
SIGNAL_DESCRIPTION['mult_dot_en']                  = {'width': 1, 'position_dec_tab': 30}
SIGNAL_DESCRIPTION['mult_dot_signed']              = {'width': 2, 'position_dec_tab': 28}
SIGNAL_DESCRIPTION['mult_imm_mux']                 = {'width': 1, 'position_dec_tab': 27}
SIGNAL_DESCRIPTION['mult_int_en']                  = {'width': 1, 'position_dec_tab': 26}
SIGNAL_DESCRIPTION['mult_operator']                = {'width': 3, 'position_dec_tab': 23}
SIGNAL_DESCRIPTION['mult_sel_subword']             = {'width': 1, 'position_dec_tab': 22}
SIGNAL_DESCRIPTION['mult_signed_mode']             = {'width': 2, 'position_dec_tab': 20}
SIGNAL_DESCRIPTION['prepost_useincr']              = {'width': 1, 'position_dec_tab': 19}
SIGNAL_DESCRIPTION['rega_used_dec']                = {'width': 1, 'position_dec_tab': 18}
SIGNAL_DESCRIPTION['regb_used_dec']                = {'width': 1, 'position_dec_tab': 17}
SIGNAL_DESCRIPTION['regc_mux']                     = {'width': 2, 'position_dec_tab': 15}
SIGNAL_DESCRIPTION['regc_used_dec']                = {'width': 1, 'position_dec_tab': 14}
SIGNAL_DESCRIPTION['regfile_alu_waddr_mux_sel']    = {'width': 1, 'position_dec_tab': 13}
SIGNAL_DESCRIPTION['regfile_alu_we_dec_id']        = {'width': 1, 'position_dec_tab': 12}
SIGNAL_DESCRIPTION['regfile_alu_we_id']            = {'width': 1, 'position_dec_tab': 11}
SIGNAL_DESCRIPTION['regfile_fp_a']                 = {'width': 1, 'position_dec_tab': 10}
SIGNAL_DESCRIPTION['regfile_fp_b']                 = {'width': 1, 'position_dec_tab': 9}
SIGNAL_DESCRIPTION['regfile_fp_c']                 = {'width': 1, 'position_dec_tab': 8}
SIGNAL_DESCRIPTION['regfile_fp_d']                 = {'width': 1, 'position_dec_tab': 7}
SIGNAL_DESCRIPTION['regfile_we_id']                = {'width': 1, 'position_dec_tab': 6}
SIGNAL_DESCRIPTION['scalar_replication']           = {'width': 1, 'position_dec_tab': 5}
SIGNAL_DESCRIPTION['scalar_replication_c']         = {'width': 1, 'position_dec_tab': 4}
SIGNAL_DESCRIPTION['uret_dec']                     = {'width': 1, 'position_dec_tab': 3}
SIGNAL_DESCRIPTION['uret_insn_dec']                = {'width': 1, 'position_dec_tab': 2}
SIGNAL_DESCRIPTION['wfi_insn_dec']                 = {'width': 1, 'position_dec_tab': 1}
SIGNAL_DESCRIPTION['null']                         = {'width': 1, 'position_dec_tab': 0}



DEASSERT_WE_AFFECTED_SIGNALS = ['alu_en', ' apu_en', ' mult_int_en', ' mult_dot_en', ' regfile_mem_we', ' regfile_alu_we', ' data_req', ' hwlp_we', ' csr_op', ' ctrl_transfer_insn']

#if not 'data_req_id'  thus:  data_load_event_ex_o <= 1'b0;

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



def extract(integer, position, width):
    return ((integer >> position) & ((1 << width) - 1))

def gen_signal_set():
    signal_set = []
    for stage in CS_VECTOR_ARCH.values():
        for name in stage:
            if name not in signal_set:
                signal_set.append(name)
    signal_set.reverse()
    return signal_set


def gen_cs_vector_description(signal_set):
    cs_vector_description = {}
    position = 0
    for cs_name in signal_set:
        cs_vector_description[cs_name]=SIGNAL_DESCRIPTION[cs_name]
        cs_vector_description[cs_name]['position']= position
        position += cs_vector_description[cs_name]['width']
    return cs_vector_description

CS_VECTOR_DESCRIPTION =  gen_cs_vector_description(gen_signal_set())

def gen_deassert_we_mask():
    mask = 0
    for cs in CS_VECTOR_DESCRIPTION:
        if cs not in DEASSERT_WE_AFFECTED_SIGNALS:
            mask |= ((1 << CS_VECTOR_DESCRIPTION[cs]['width']) - 1) << CS_VECTOR_DESCRIPTION[cs]['position']
    return mask

def gen_cs_vector_reset():
    cs_vector_reset = 0
    for cs in CS_VECTOR_DESCRIPTION:
        cs_vector_reset |= CS_VECTOR_DESCRIPTION[cs]['reset_val'] << (CS_VECTOR_DESCRIPTION[cs]['position'])
    return(cs_vector_reset)


def count_cs_vector_width():
    cs_vector_width = 0
    for cs in CS_VECTOR_DESCRIPTION:
        cs_vector_width += CS_VECTOR_DESCRIPTION[cs]['width']
    return(cs_vector_width)


def gen_cs_vector_id_invalid_ex_ready():
    cs_vector_id_invalid_ex_ready = 0
    mask_cs_vector_id_invalid_ex_ready = 0
    for cs in CS_VECTOR_DESCRIPTION:
        if 'id_invalid_ex_ready' in CS_VECTOR_DESCRIPTION[cs].keys():
            cs_vector_id_invalid_ex_ready |= CS_VECTOR_DESCRIPTION[cs]['id_invalid_ex_ready'] << CS_VECTOR_DESCRIPTION[cs]['position']
        else:
            mask_cs_vector_id_invalid_ex_ready |= ((1 << CS_VECTOR_DESCRIPTION[cs]['width']) - 1) << CS_VECTOR_DESCRIPTION[cs]['position']
    return(cs_vector_id_invalid_ex_ready, mask_cs_vector_id_invalid_ex_ready)



def cs_vector_dict_to_xored_int(cs_vector_dict):
    cs_vector_reduced = 0
    for stage in ['wb','ex','id']:
        if stage in cs_vector_dict.keys() and stage in CS_VECTOR_ARCH:
            for cs in CS_VECTOR_ARCH[stage]:
                cs_vector_reduced <<= CS_VECTOR_DESCRIPTION[cs]['width']
                cs_vector_reduced |= (cs_vector_dict[stage] >> CS_VECTOR_DESCRIPTION[cs]['position']) & ((1 << CS_VECTOR_DESCRIPTION[cs]['width']) - 1)
    return(cs_vector_reduced)



def cs_vector_xored_dict_to_xored_int(cs_vector_xored_dict):
    cs_vector_xored_int = 0
    for stage in ['wb', 'ex', 'id']:
        if stage in cs_vector_xored_dict.keys():
            width = 0
            for cs in CS_VECTOR_ARCH[stage]:
                width += SIGNAL_DESCRIPTION[cs]['width']
            cs_vector_xored_int <<= width
            cs_vector_xored_int |= cs_vector_xored_dict[stage]
    return(cs_vector_xored_int)



def cs_vector_xored_int_to_dict(cs_vector_xored_int):
    cs_vector_dict = {}
    for stage in ['id', 'ex', 'wb']:
        if stage in CS_VECTOR_ARCH.keys():
            cs_vector_dict[stage] = 0
            for cs in CS_VECTOR_ARCH[stage]:
                cs_vector_dict[stage] <<= CS_VECTOR_DESCRIPTION[cs]['width']
                cs_vector_dict[stage] |= cs_vector_xored_int & ((1 << CS_VECTOR_DESCRIPTION[cs]['width']) - 1)
            cs_vector_xored_int >>= width
    return (cs_vector_xored_dict)



def make_mask_ex_en(cs_vector_id):
    mask = 0
    for cs in CS_VECTOR_DESCRIPTION:
        if not 'ex_en' in CS_VECTOR_DESCRIPTION[cs]:
            mask |= ((1 << CS_VECTOR_DESCRIPTION[cs]['width']) - 1) << CS_VECTOR_DESCRIPTION[cs]['position']
        else:
            en_ex = (cs_vector_id >> CS_VECTOR_DESCRIPTION[CS_VECTOR_DESCRIPTION[cs]['ex_en']]['position']) & 1
            if en_ex == 1:
                mask |= ((1 << CS_VECTOR_DESCRIPTION[cs]['width']) - 1) << CS_VECTOR_DESCRIPTION[cs]['position']
    return mask



def decode_tab_to_cs_vector(cs_decode_table):
    cs_vector = 0
    for cs_name in CS_VECTOR_DESCRIPTION.keys():
        cs_vector |= extract(cs_decode_table, CS_VECTOR_DESCRIPTION[cs_name]['position_dec_tab'], CS_VECTOR_DESCRIPTION[cs_name]['width']) << CS_VECTOR_DESCRIPTION[cs_name]['position']
    return cs_vector




def read_decoding_table(cs_path):
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
        cs_decoder.append({'cs_vector': (int(cs_file_line[2], 16) << (56+8)) | ( int(cs_file_line[2], 16) << 8) | int(cs_file_line[2], 16),
            'is_multicycle': int(cs_file_line[5]), 'ctrl_transfer': int(cs_file_line[6])})
    return (cs_decoder)


