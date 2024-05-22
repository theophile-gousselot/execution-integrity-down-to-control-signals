from riscv_control_signals import *


SIGNAL_SET = gen_signal_set()
CS_VECTOR_DESCRIPTION =  gen_cs_vector_description(SIGNAL_SET)

DEASSERT_WE_MASK = gen_deassert_we_mask()

CS_VECTOR_RESET = gen_cs_vector_reset()
CS_VECTOR_WIDTH = count_cs_vector_width()
CS_VECTOR_ALL_ONE = (1 << CS_VECTOR_WIDTH) - 1
CS_VECTOR_ID_INVALID_EX_READY, MASK_CS_VECTOR_ID_INVALID_EX_READY = gen_cs_vector_id_invalid_ex_ready()
