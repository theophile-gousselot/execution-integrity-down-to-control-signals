IMMA_Z = 0b0
IMMA_ZERO = 0b1

IMMB_I = 0b0000
IMMB_S = 0b0001
IMMB_U = 0b0010
IMMB_PCINCR = 0b0011
IMMB_S2 = 0b0100
IMMB_BI = 0b1011
IMMB_S3 = 0b0101
IMMB_VS = 0b0110
IMMB_VU = 0b0111
IMMB_SHUF = 0b1000
IMMB_CLIP = 0b1001


def instr2fct7_3_opcode(instr):
    return (((instr >> 25) << 8) | (((instr >> 12) & 0b111) << 5) | ((instr >> 2) & 0b11111))

def sel(instr, i, j):
    msb, lsb = max(i, j), min(i, j)
    return ((instr >> lsb) & ((1 << (msb - lsb + 1)) -1 ))

def sign_ext(bit, width):
    if bit == 0:
        return 0
    elif bit == 1:
        return ((1 << width) - 1)
    else:
        raise ValueError(f'Error, bit should be a bit ! Not {bit}.')




imm_i_type = lambda instr : sign_ext(sel(instr, 31, 31), 20) << 12 | sel(instr, 31, 20)
imm_iz_type = lambda instr : sel(instr, 31, 20)
imm_s_type = lambda instr : sign_ext(sel(instr, 31, 31), 20) << 12  | sel(instr, 31, 25) << 5 | sel(instr, 11, 7)
imm_sb_type = lambda instr : sign_ext(sel(instr, 31, 31), 19) << 13  | sel(instr, 31, 31) << 12  | sel(instr, 7, 7) << 11  | sel(instr, 30, 25) << 5  | sel(instr, 11, 8) << 1
imm_u_type = lambda instr : sel(instr, 31, 12) << 12
imm_z_type = lambda instr : sel(instr, 19, 15)
imm_s2_type = lambda instr : sel(instr, 24, 20)
imm_bi_type = lambda instr : sign_ext(sel(instr, 24, 24), 27) << 5 | sel(instr, 24, 20)
imm_s3_type = lambda instr : sel(instr, 29, 25)
imm_vs_type = lambda instr : sign_ext(sel(instr, 24, 24), 26) << 6 | sel(instr, 24, 20) << 1  | sel(instr, 25, 25)
imm_vu_type = lambda instr : sel(instr, 24, 20) << 1  | sel(instr, 25, 25)
imm_shuffleb_type = lambda instr : sel(instr, 28, 27) << 24  | sel(instr, 24, 23) << 16 | sel(instr, 22, 21) << 8 | sel(instr, 20, 20) << 1 | sel(instr, 25, 25)
imm_shuffle_type = lambda instr : imm_shuffleb_type


def imm_a(instr, extract_cs_from_decoder_lut):
    imm_a_mux_sel = extract_cs_from_decoder_lut(instr2fct7_3_opcode(instr), 'imm_a_mux_sel')
    if imm_a_mux_sel == IMMA_ZERO:
        imm_a = 0
    elif imm_a_mux_sel == IMMA_Z:
        imm_a = imm_z_type(instr)
    else:
        raise ValueError(f'Error, imm_a_mux_sel should be a bit ! Not {imm_a_mux_sel}.')
    return imm_a

def imm_b(instr, extract_cs_from_decoder_lut):
    imm_b_mux_sel = extract_cs_from_decoder_lut(instr2fct7_3_opcode(instr), 'imm_b_mux_sel')

    if imm_b_mux_sel == IMMB_I:
        imm_b = imm_i_type(instr)
    elif imm_b_mux_sel == IMMB_S:
        imm_b = imm_s_type(instr)
    elif imm_b_mux_sel == IMMB_U:
        imm_b = imm_u_type(instr)
    elif imm_b_mux_sel == IMMB_PCINCR:
        imm_b = 0x4
    elif imm_b_mux_sel == IMMB_S2:
        imm_b = imm_s2_type(instr)
    elif imm_b_mux_sel == IMMB_BI:
        imm_b = imm_bi_type(instr)
    elif imm_b_mux_sel == IMMB_S3:
        imm_b = imm_s3_type(instr)
    elif imm_b_mux_sel == IMMB_VS:
        imm_b = imm_vs_type(instr)
    elif imm_b_mux_sel == IMMB_VU:
        imm_b = imm_vu_type(instr)
    elif imm_b_mux_sel == IMMB_SHUF:
        imm_b = imm_shuffle_type(instr)
    #elif imm_b_mux_sel == IMMB_CLIP: # ignore that case (not used)
    #    imm_b = imm_clip_type >> 1
    else:
        imm_b = imm_i_type(instr)

    return imm_b

