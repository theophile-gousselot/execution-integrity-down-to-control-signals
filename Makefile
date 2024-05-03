##################################################
## __     __         _       _     _            ##
## \ \   / /_ _ _ __(_) __ _| |__ | | ___  ___  ##
##  \ \ / / _` | '__| |/ _` | '_ \| |/ _ \/ __| ##
##   \ V / (_| | |  | | (_| | |_) | |  __/\__ \ ##
##    \_/ \__,_|_|  |_|\__,_|_.__/|_|\___||___/ ##
##                                              ##
##################################################

#==== DEFAULT USER MACROS ===#
MAX_SIM_TIME		:= 30000000


#==== RISCV ====#
RISCV			:= /opt/corev
RISCV_PREFIX      	:= riscv32-corev-elf-
RISCV_EXE_PREFIX  	:= $(RISCV)/bin/$(RISCV_PREFIX)
RISCV_CC          	:= gcc
CFLAGS 				:= -Os -g -static -mabi=ilp32 -march=rv32im -Wall -pedantic



#==== ENCRYPTION ===#
PB_ROUNDS			:= 6
PB_ROUNDS_PY_FLAG	:= --pb_rounds=$(PB_ROUNDS)



#==== SOURCE PATHS ====#
SRC_DIR				:= ./SRC
SCRIPT_DIR	 		:= $(SRC_DIR)/SCRIPTS
SV_RTL_DIR	 		:= $(SRC_DIR)/RTL
SV_BENCH_DIR		:= $(SRC_DIR)/BENCH
SRC_BSP_DIR	 		:= $(SRC_DIR)/PROGRAM_TOOLS/BSP
BSP_RESULT_FILES	:= $(patsubst %,$(SRC_BSP_DIR)/%,crt0.o handlers.o syscalls.o vectors.o libcv-verif.a)

SRC_RTL				:= $(shell cat ./SRC/RTL/rtl.flist)
SRC_RTL_ENCRYPTED	:= $(shell cat ./SRC/RTL/rtl_encrypted.flist)
SRC_TB_FILE			:= $(SV_BENCH_DIR)/core_v_verif_fpga_tb.cpp

TB_CPP_NAME			:= core_v_verif_fpga

#==== CV32E40P ====#
CV_CORE_PKG 		:= $(SV_RTL_DIR)/iea_cv32e40p_fpga_dev
CV_CORE_BRANCH 		:= iea_cv32e40p_fpga_dev
CV_CORE_REPO   		:= git@gitlab.emse.fr:theophile.gousselot/cv32e40p_cfi.git



#==== OBJECT PATHS ====#
OBJ_DIR                 := ./OBJ
OBJ_VERI_DIR 			:= $(OBJ_DIR)/VERILATOR_OBJ_DIR
OBJ_TOOLS_DIR           := $(OBJ_DIR)/PROGRAM_TOOLS
OBJ_BSP_DIR             := $(OBJ_TOOLS_DIR)/BSP




###################################################
##  _____                 _   _                  ##
## |  ___|   _ _ __   ___| |_(_) ___  _ __  ___  ##
## | |_ | | | | '_ \ / __| __| |/ _ \| '_ \/ __| ##
## |  _|| |_| | | | | (__| |_| | (_) | | | \__ \ ##
## |_|   \__,_|_| |_|\___|\__|_|\___/|_| |_|___/ ##
##                                               ##
###################################################

cf_val = $(shell echo "$(1)" | sed 's=^.*_cf\([0-9]\).*$$=\1=' || true)
cf = $(shell echo "$(1)" | sed -n 's=^.*_cf\([0-9]\).*$$=_cf\1=p' || true)

cs_val = $(shell echo "$(1)" | sed -E -n 's=^.*_cs(([a-z]|-)*).*$$=_cs\1=p' || true)
#cs = $(shell echo "$(1)" | grep -q "_cs" && echo "_cs" || true)
cs_id_hw = $(shell echo "$(1)" | sed -E -n 's=^.*_cs.*-(id).*$$=+define+CS_\U\1 -CFLAGS  '\''-D CS_\U\1'\''=p')
cs_ex_hw = $(shell echo "$(1)" | sed -E -n 's=^.*_cs.*-(ex).*$$=+define+CS_\U\1 -CFLAGS  '\''-D CS_\U\1'\''=p')
cs_flags_hw = $(shell echo "$(1)" | grep -q "_cs" && echo "$(call cs_id_hw,$(1)) $(call cs_ex_hw,$(1))" || true)
cs_sw = $(shell echo "$(1)" | sed -E -n 's=^.*_cs(-id|)(-ex|).*$$=cs\1\2=p')
cs_flags_sw = $(shell echo "$(1)" | grep -q "_cs" && echo "--control_signals=$(call cs_sw,$(1))" || true)

vcd = $(shell echo "$(1)" | grep -q "_vcd\|\.vcd" && echo "_vcd" || true)
vcd_flags = $(shell echo "$(1)" | grep -q "_vcd" && echo "--trace --trace-depth 8 -CFLAGS '-D VCD'" || true)

encrypted = $(shell echo "$(1)" | grep -q "_encrypted" && echo "_encrypted" || true)
encrypted_flags = $(shell echo "$(1)" | grep -q "_encrypted" && echo "+define+ENCRYPT -CFLAGS '-D ENCRYPT' -GHW_PERMUTATION_N=$(shell expr 6 / $(call cf_val,$@) ) -CFLAGS '-D CLK_FACTOR=$(call cf_val,$@)'" || true)





########################################
##  _____                    _        ##
## |_   _|_ _ _ __ __ _  ___| |_ ___  ##
##   | |/ _` | '__/ _` |/ _ \ __/ __| ##
##   | | (_| | | | (_| |  __/ |_\__ \ ##
##   |_|\__,_|_|  \__, |\___|\__|___/ ##
##                |___/               ##
########################################

##                 _ _       _                                           _
## __   _____ _ __(_| | __ _| |_ ___  _ __ _     _____  _____  ___ _   _| |_ ___
## \ \ / / _ | '__| | |/ _` | __/ _ \| '__(_)   / _ \ \/ / _ \/ __| | | | __/ _ \
##  \ V |  __| |  | | | (_| | || (_) | |   _   |  __/>  |  __| (__| |_| | ||  __/
##   \_/ \___|_|  |_|_|\__,_|\__\___/|_|  (_)   \___/_/\_\___|\___|\__,_|\__\___|
##


#==== VCD ====#
OBJ/PROGRAMS/%/SIM/VCD/program.vcd : \
		$(OBJ_VERI_DIR)/$(TB_CPP_NAME)_vcd/V$(TB_CPP_NAME) \
		OBJ/PROGRAMS/%/PROGRAM_COMPILED/.mem.timestamp \
		OBJ/PROGRAMS/%/SIM/REF/ref_decode_pc_instr_patch.csv
	@echo "\n===> $@"
	mkdir -p $(dir $@)
	$(OBJ_VERI_DIR)/$(TB_CPP_NAME)_vcd/V$(TB_CPP_NAME) $* --verif

OBJ/PROGRAMS/%/SIM/LOG/program_encrypted_cf1_verif.log \
OBJ/PROGRAMS/%/SIM/LOG/program_encrypted_cf2_verif.log \
OBJ/PROGRAMS/%/SIM/LOG/program_encrypted_cf3_verif.log \
OBJ/PROGRAMS/%/SIM/LOG/program_encrypted_cf6_verif.log \
OBJ/PROGRAMS/%/SIM/LOG/program_encrypted_cf1_cs-id_verif.log \
OBJ/PROGRAMS/%/SIM/LOG/program_encrypted_cf2_cs-id_verif.log \
OBJ/PROGRAMS/%/SIM/LOG/program_encrypted_cf3_cs-id_verif.log \
OBJ/PROGRAMS/%/SIM/LOG/program_encrypted_cf6_cs-id_verif.log \
OBJ/PROGRAMS/%/SIM/LOG/program_encrypted_cf1_cs-id-ex_verif.log \
OBJ/PROGRAMS/%/SIM/LOG/program_encrypted_cf2_cs-id-ex_verif.log \
OBJ/PROGRAMS/%/SIM/LOG/program_encrypted_cf3_cs-id-ex_verif.log \
OBJ/PROGRAMS/%/SIM/LOG/program_encrypted_cf6_cs-id-ex_verif.log \
OBJ/PROGRAMS/%/SIM/VCD/program_encrypted_cf1.vcd \
OBJ/PROGRAMS/%/SIM/VCD/program_encrypted_cf2.vcd \
OBJ/PROGRAMS/%/SIM/VCD/program_encrypted_cf3.vcd \
OBJ/PROGRAMS/%/SIM/VCD/program_encrypted_cf6.vcd \
OBJ/PROGRAMS/%/SIM/VCD/program_encrypted_cf1_cs-id.vcd \
OBJ/PROGRAMS/%/SIM/VCD/program_encrypted_cf2_cs-id.vcd \
OBJ/PROGRAMS/%/SIM/VCD/program_encrypted_cf3_cs-id.vcd \
OBJ/PROGRAMS/%/SIM/VCD/program_encrypted_cf6_cs-id.vcd \
OBJ/PROGRAMS/%/SIM/VCD/program_encrypted_cf1_cs-id-ex.vcd \
OBJ/PROGRAMS/%/SIM/VCD/program_encrypted_cf2_cs-id-ex.vcd \
OBJ/PROGRAMS/%/SIM/VCD/program_encrypted_cf3_cs-id-ex.vcd \
OBJ/PROGRAMS/%/SIM/VCD/program_encrypted_cf6_cs-id-ex.vcd : \
		OBJ/PROGRAMS/%/SIM/REF/ref_decode_pc_instr_patch.csv
	make OBJ/PROGRAMS/$*/PROGRAM_COMPILED/.mem_encrypted$(call cs_val,$@).timestamp
	make OBJ/PROGRAMS/$*/PROGRAM_COMPILED/program_encrypted$(call cs_val,$@)_patches.mem
	make $(OBJ_VERI_DIR)/$(TB_CPP_NAME)_encrypted$(call vcd,$@)$(call cf,$@)$(call cs_val,$@)/V$(TB_CPP_NAME)
	@echo "\n===> $@"
	mkdir -p $(dir $@)
	$(OBJ_VERI_DIR)/$(TB_CPP_NAME)_encrypted$(call vcd,$@)$(call cf,$@)$(call cs_val,$@)/V$(TB_CPP_NAME) $* --verif


#==== SAVE REF ====#
.PRECIOUS: OBJ/PROGRAMS/%/SIM/LOG/program_save_ref.log
OBJ/PROGRAMS/%/SIM/LOG/program_save_ref.log :
	make OBJ/PROGRAMS/$*/SIM/REF/ref_decode_pc_instr_patch.csv


.PRECIOUS: OBJ/PROGRAMS/%/SIM/REF/ref_decode_pc_instr_patch.csv
OBJ/PROGRAMS/%/SIM/REF/ref_decode_pc_instr_patch.csv : \
		$(OBJ_VERI_DIR)/$(TB_CPP_NAME)/V$(TB_CPP_NAME) \
		OBJ/PROGRAMS/%/PROGRAM_COMPILED/.mem.timestamp
	@echo "\n===> $@"
	mkdir -p $(dir $@)
	$(OBJ_VERI_DIR)/$(TB_CPP_NAME)/V$(TB_CPP_NAME) $* --save_ref


.PRECIOUS: OBJ/PROGRAMS/%/SIM/REF/ref_cs.csv
OBJ/PROGRAMS/%/SIM/REF/ref_cs.csv : \
		$(OBJ_VERI_DIR)/$(TB_CPP_NAME)/V$(TB_CPP_NAME) \
		OBJ/PROGRAMS/%/PROGRAM_COMPILED/.mem.timestamp
	@echo "\n===> $@"
	mkdir -p $(dir $@)
	$(OBJ_VERI_DIR)/$(TB_CPP_NAME)/V$(TB_CPP_NAME) $* --save_ref --cs_ref


#==== VERIFICATION ====#
OBJ/PROGRAMS/%/SIM/LOG/program_verif.log :  \
		$(OBJ_VERI_DIR)/$(TB_CPP_NAME)/V$(TB_CPP_NAME) \
		OBJ/PROGRAMS/%/PROGRAM_COMPILED/.mem.timestamp \
		OBJ/PROGRAMS/%/SIM/REF/ref_decode_pc_instr_patch.csv
	@echo "\n===> $@"
	mkdir -p $(dir $@)
	$(OBJ_VERI_DIR)/$(TB_CPP_NAME)/V$(TB_CPP_NAME) $* --verif



#==== TRACE SIGNALS ====#
# "$(OBJ_VERI_DIR)/$(TB_CPP_NAME)/V$(TB_CPP_NAME) \" must be added to the dependency list,
# however it induces to compute again jalr_successor beacause of RTL edits, even if the
# edits concern only encryption part.
.PRECIOUS: OBJ/PROGRAMS/%/SIM/REF/program_trace_signals.csv
OBJ/PROGRAMS/%/SIM/REF/program_trace_signals.csv : \
		OBJ/PROGRAMS/%/PROGRAM_COMPILED/.mem.timestamp
	make $(OBJ_VERI_DIR)/$(TB_CPP_NAME)/V$(TB_CPP_NAME)
	@echo "\n===> $@"
	mkdir -p $(dir $@)
	$(OBJ_VERI_DIR)/$(TB_CPP_NAME)/V$(TB_CPP_NAME) $* --trace_signals --save_ref



##                  _ _       _                  _           _ _     _
##  __   _____ _ __(_| | __ _| |_ ___  _ __ _   | |__  _   _(_| | __| |
##  \ \ / / _ | '__| | |/ _` | __/ _ \| '__(_)  | '_ \| | | | | |/ _` |
##   \ V |  __| |  | | | (_| | || (_) | |   _   | |_) | |_| | | | (_| |
##    \_/ \___|_|  |_|_|\__,_|\__\___/|_|  (_)  |_.__/ \__,_|_|_|\__,_|
## 


#==== BUILD CPP MODEL with ENCRYPTED PROGRAM and WAVEFORM GENERATION ===#
OBJ/VERILATOR_OBJ_DIR/core_v_verif_fpga/Vcore_v_verif_fpga \
OBJ/VERILATOR_OBJ_DIR/core_v_verif_fpga_vcd/Vcore_v_verif_fpga \
OBJ/VERILATOR_OBJ_DIR/core_v_verif_fpga_encrypted_cf1/Vcore_v_verif_fpga \
OBJ/VERILATOR_OBJ_DIR/core_v_verif_fpga_encrypted_cf2/Vcore_v_verif_fpga \
OBJ/VERILATOR_OBJ_DIR/core_v_verif_fpga_encrypted_cf3/Vcore_v_verif_fpga \
OBJ/VERILATOR_OBJ_DIR/core_v_verif_fpga_encrypted_cf6/Vcore_v_verif_fpga \
OBJ/VERILATOR_OBJ_DIR/core_v_verif_fpga_encrypted_cf1_cs-id/Vcore_v_verif_fpga \
OBJ/VERILATOR_OBJ_DIR/core_v_verif_fpga_encrypted_cf2_cs-id/Vcore_v_verif_fpga \
OBJ/VERILATOR_OBJ_DIR/core_v_verif_fpga_encrypted_cf3_cs-id/Vcore_v_verif_fpga \
OBJ/VERILATOR_OBJ_DIR/core_v_verif_fpga_encrypted_cf6_cs-id/Vcore_v_verif_fpga \
OBJ/VERILATOR_OBJ_DIR/core_v_verif_fpga_encrypted_cf1_cs-id-ex/Vcore_v_verif_fpga \
OBJ/VERILATOR_OBJ_DIR/core_v_verif_fpga_encrypted_cf2_cs-id-ex/Vcore_v_verif_fpga \
OBJ/VERILATOR_OBJ_DIR/core_v_verif_fpga_encrypted_cf3_cs-id-ex/Vcore_v_verif_fpga \
OBJ/VERILATOR_OBJ_DIR/core_v_verif_fpga_encrypted_cf6_cs-id-ex/Vcore_v_verif_fpga \
OBJ/VERILATOR_OBJ_DIR/core_v_verif_fpga_encrypted_vcd_cf1/Vcore_v_verif_fpga \
OBJ/VERILATOR_OBJ_DIR/core_v_verif_fpga_encrypted_vcd_cf2/Vcore_v_verif_fpga \
OBJ/VERILATOR_OBJ_DIR/core_v_verif_fpga_encrypted_vcd_cf3/Vcore_v_verif_fpga \
OBJ/VERILATOR_OBJ_DIR/core_v_verif_fpga_encrypted_vcd_cf6/Vcore_v_verif_fpga \
OBJ/VERILATOR_OBJ_DIR/core_v_verif_fpga_encrypted_vcd_cf1_cs-id/Vcore_v_verif_fpga \
OBJ/VERILATOR_OBJ_DIR/core_v_verif_fpga_encrypted_vcd_cf2_cs-id/Vcore_v_verif_fpga \
OBJ/VERILATOR_OBJ_DIR/core_v_verif_fpga_encrypted_vcd_cf3_cs-id/Vcore_v_verif_fpga \
OBJ/VERILATOR_OBJ_DIR/core_v_verif_fpga_encrypted_vcd_cf6_cs-id/Vcore_v_verif_fpga  \
OBJ/VERILATOR_OBJ_DIR/core_v_verif_fpga_encrypted_vcd_cf1_cs-id-ex/Vcore_v_verif_fpga \
OBJ/VERILATOR_OBJ_DIR/core_v_verif_fpga_encrypted_vcd_cf2_cs-id-ex/Vcore_v_verif_fpga \
OBJ/VERILATOR_OBJ_DIR/core_v_verif_fpga_encrypted_vcd_cf3_cs-id-ex/Vcore_v_verif_fpga \
OBJ/VERILATOR_OBJ_DIR/core_v_verif_fpga_encrypted_vcd_cf6_cs-id-ex/Vcore_v_verif_fpga : \
		$(CV_CORE_PKG) $(SRC_RTL_ENCRYPTED) $(SRC_TB_FILE)
	@echo "\n===> $@"
	mkdir -p $(dir $@)
	verilator \
		$(call vcd_flags,$@) \
		$(call encrypted_flags,$@) \
		$(call cs_flags_hw,$@) \
		-CFLAGS "-D MAX_SIM_TIME=$(MAX_SIM_TIME)" \
	   	--Mdir $(OBJ_VERI_DIR)/$(TB_CPP_NAME)$(call encrypted,$@)$(call vcd,$@)$(call cf,$@)$(call cs_val,$@) \
	   	--cc -sv --exe \
	   	--top-module $(TB_CPP_NAME) ../../$(SRC_TB_FILE) \
	   	-f SRC/RTL/rtl_encrypted.flist
	make \
		-C $(OBJ_VERI_DIR)/$(TB_CPP_NAME)$(call encrypted,$@)$(call vcd,$@)$(call cf,$@)$(call cs_val,$@) \
		-f V$(TB_CPP_NAME).mk \
		V$(TB_CPP_NAME)



##        _                _
## __   _(_)_   ____ _  __| | ___
## \ \ / / \ \ / / _` |/ _` |/ _ \
##  \ V /| |\ V / (_| | (_| | (_) |
##   \_/ |_| \_/ \__,_|\__,_|\___/
##



OBJ/VIVADO_OBJ_DIR/core_v_verif_fpga_%/.simulate_behav_log.timestamp : OBJ/VIVADO_OBJ_DIR/core_v_verif_fpga_%
	@echo "\n===> $@"
	vivado -mode batch OBJ/VIVADO_OBJ_DIR/core_v_verif_fpga_$*/core_v_verif_fpga_$*.xpr -source ./SRC/SCRIPTS/set_questa_dir_for_5simulations.tcl
	SRC/SCRIPTS/launch_questa_simulation.sh OBJ/VIVADO_OBJ_DIR/core_v_verif_fpga_$*/core_v_verif_fpga_$*.sim/sim_1/behav/questa -c
	touch $@

OBJ/VIVADO_OBJ_DIR/core_v_verif_fpga_%/.simulate_log.timestamp : OBJ/VIVADO_OBJ_DIR/core_v_verif_fpga_%
	@echo "\n===> $@"
	vivado -mode batch OBJ/VIVADO_OBJ_DIR/core_v_verif_fpga_$*/core_v_verif_fpga_$*.xpr -source ./SRC/SCRIPTS/set_questa_dir_for_5simulations.tcl
	SRC/SCRIPTS/launch_questa_simulation.sh OBJ/VIVADO_OBJ_DIR/core_v_verif_fpga_$*/core_v_verif_fpga_$*.sim/sim_1/behav/questa -c
	SRC/SCRIPTS/launch_questa_simulation.sh OBJ/VIVADO_OBJ_DIR/core_v_verif_fpga_$*/core_v_verif_fpga_$*.sim/sim_1/synth/func/questa -c
	SRC/SCRIPTS/launch_questa_simulation.sh OBJ/VIVADO_OBJ_DIR/core_v_verif_fpga_$*/core_v_verif_fpga_$*.sim/sim_1/synth/timing/questa -c
	SRC/SCRIPTS/launch_questa_simulation.sh OBJ/VIVADO_OBJ_DIR/core_v_verif_fpga_$*/core_v_verif_fpga_$*.sim/sim_1/impl/func/questa -c
	SRC/SCRIPTS/launch_questa_simulation.sh OBJ/VIVADO_OBJ_DIR/core_v_verif_fpga_$*/core_v_verif_fpga_$*.sim/sim_1/impl/timing/questa -c
	touch $@


OBJ/VIVADO_OBJ_DIR/core_v_verif_fpga_%_encrypted_cf1/.simulate_behav_log.timestamp \
OBJ/VIVADO_OBJ_DIR/core_v_verif_fpga_%_encrypted_cf2/.simulate_behav_log.timestamp \
OBJ/VIVADO_OBJ_DIR/core_v_verif_fpga_%_encrypted_cf3/.simulate_behav_log.timestamp \
OBJ/VIVADO_OBJ_DIR/core_v_verif_fpga_%_encrypted_cf6/.simulate_behav_log.timestamp :
	make OBJ/VIVADO_OBJ_DIR/core_v_verif_fpga_$*_encrypted$(call cf,$@)
	@echo "\n===> $@"
	vivado -mode batch OBJ/VIVADO_OBJ_DIR/core_v_verif_fpga_$*_encrypted$(call cf,$@)/core_v_verif_fpga_$*_encrypted$(call cf,$@).xpr -source ./SRC/SCRIPTS/set_questa_dir_for_5simulations.tcl
	SRC/SCRIPTS/launch_questa_simulation.sh OBJ/VIVADO_OBJ_DIR/core_v_verif_fpga_$*_encrypted$(call cf,$@)/core_v_verif_fpga_$*_encrypted$(call cf,$@).sim/sim_1/behav/questa -c
	touch $@


OBJ/VIVADO_OBJ_DIR/core_v_verif_fpga_%_encrypted_cf1/.simulate_log.timestamp \
OBJ/VIVADO_OBJ_DIR/core_v_verif_fpga_%_encrypted_cf2/.simulate_log.timestamp \
OBJ/VIVADO_OBJ_DIR/core_v_verif_fpga_%_encrypted_cf3/.simulate_log.timestamp \
OBJ/VIVADO_OBJ_DIR/core_v_verif_fpga_%_encrypted_cf6/.simulate_log.timestamp :
	make OBJ/VIVADO_OBJ_DIR/core_v_verif_fpga_$*_encrypted$(call cf,$@)
	@echo "\n===> $@"
	vivado -mode batch OBJ/VIVADO_OBJ_DIR/core_v_verif_fpga_$*_encrypted$(call cf,$@)/core_v_verif_fpga_$*_encrypted$(call cf,$@).xpr -source ./SRC/SCRIPTS/set_questa_dir_for_5simulations.tcl
	SRC/SCRIPTS/launch_questa_simulation.sh OBJ/VIVADO_OBJ_DIR/core_v_verif_fpga_$*_encrypted$(call cf,$@)/core_v_verif_fpga_$*_encrypted$(call cf,$@).sim/sim_1/behav/questa -c
	SRC/SCRIPTS/launch_questa_simulation.sh OBJ/VIVADO_OBJ_DIR/core_v_verif_fpga_$*_encrypted$(call cf,$@)/core_v_verif_fpga_$*_encrypted$(call cf,$@).sim/sim_1/synth/func/questa -c
	SRC/SCRIPTS/launch_questa_simulation.sh OBJ/VIVADO_OBJ_DIR/core_v_verif_fpga_$*_encrypted$(call cf,$@)/core_v_verif_fpga_$*_encrypted$(call cf,$@).sim/sim_1/synth/timing/questa -c
	SRC/SCRIPTS/launch_questa_simulation.sh OBJ/VIVADO_OBJ_DIR/core_v_verif_fpga_$*_encrypted$(call cf,$@)/core_v_verif_fpga_$*_encrypted$(call cf,$@).sim/sim_1/impl/func/questa -c
	SRC/SCRIPTS/launch_questa_simulation.sh OBJ/VIVADO_OBJ_DIR/core_v_verif_fpga_$*_encrypted$(call cf,$@)/core_v_verif_fpga_$*_encrypted$(call cf,$@).sim/sim_1/impl/timing/questa -c
	touch $@

OBJ/VIVADO_OBJ_DIR/core_v_verif_fpga_% : $(CV_CORE_PKG) $(SRC_RTL) $(SRC_TB_FILE) \
		SRC/SCRIPTS/create_projects.tcl \
		OBJ/PROGRAMS/%/PROGRAM_COMPILED/.mem.timestamp
	@echo "\n===> $@"
	vivado -mode batch -source SRC/SCRIPTS/create_projects.tcl -tclargs core_v_verif_fpga_$*

OBJ/VIVADO_OBJ_DIR/core_v_verif_fpga_%_encrypted_cf1 \
OBJ/VIVADO_OBJ_DIR/core_v_verif_fpga_%_encrypted_cf2 \
OBJ/VIVADO_OBJ_DIR/core_v_verif_fpga_%_encrypted_cf3 \
OBJ/VIVADO_OBJ_DIR/core_v_verif_fpga_%_encrypted_cf6 :  $(CV_CORE_PKG) $(SRC_RTL_ENCRYPTED) $(SRC_TB_FILE) \
		SRC/SCRIPTS/create_projects.tcl \
		OBJ/PROGRAMS/%/PROGRAM_COMPILED/.mem_encrypted.timestamp \
		OBJ/PROGRAMS/%/PROGRAM_COMPILED/program_encrypted_patches.mem
	@echo "\n===> $@"
	vivado -mode batch -source SRC/SCRIPTS/create_projects.tcl -tclargs core_v_verif_fpga_$*_encrypted$(call cf,$@)

##  _                   _                        
## | |__   __ _ _ __ __| |_      ____ _ _ __ ___ 
## | '_ \ / _` | '__/ _` \ \ /\ / / _` | '__/ _ \
## | | | | (_| | | | (_| |\ V  V / (_| | | |  __/
## |_| |_|\__,_|_|  \__,_| \_/\_/ \__,_|_|  \___|
##                                               

#==== GIT CLONE CV32E40P ====#
SRC/RTL/iea_cv32e40p_fpga_dev :
	@echo "\n===> $@"
	git clone -b $(CV_CORE_BRANCH) $(CV_CORE_REPO) $(CV_CORE_PKG); \
	cd $(CV_CORE_PKG); git checkout $(CV_CORE_BRANCH)



##                            _ _       _   _                    __ _               
##   ___ ___  _ __ ___  _ __ (_) | __ _| |_(_) ___  _ __        / _| | _____      __
##  / __/ _ \| '_ ` _ \| '_ \| | |/ _` | __| |/ _ \| '_ \ _____| |_| |/ _ \ \ /\ / /
## | (_| (_) | | | | | | |_) | | | (_| | |_| | (_) | | | |_____|  _| | (_) \ V  V / 
##  \___\___/|_| |_| |_| .__/|_|_|\__,_|\__|_|\___/|_| |_|     |_| |_|\___/ \_/\_/  
##                     |_|                                                          


#==== CONVERT HEX ENCRYPTED ====#
.PRECIOUS: OBJ/PROGRAMS/%/PROGRAM_COMPILED/.mem.timestamp 
.PRECIOUS: OBJ/PROGRAMS/%/PROGRAM_COMPILED/.mem_encrypted.timestamp 
.PRECIOUS: OBJ/PROGRAMS/%/PROGRAM_COMPILED/.mem_encrypted_cs-id.timestamp 
.PRECIOUS: OBJ/PROGRAMS/%/PROGRAM_COMPILED/.mem_encrypted_cs-id-ex.timestamp 
OBJ/PROGRAMS/%/PROGRAM_COMPILED/.mem.timestamp \
OBJ/PROGRAMS/%/PROGRAM_COMPILED/.mem_encrypted.timestamp \
OBJ/PROGRAMS/%/PROGRAM_COMPILED/.mem_encrypted_cs-id.timestamp \
OBJ/PROGRAMS/%/PROGRAM_COMPILED/.mem_encrypted_cs-id-ex.timestamp : \
		OBJ/PROGRAMS/%/PROGRAM_COMPILED/program.itb \
		OBJ/PROGRAMS/%/PROGRAM_COMPILED/program.readelf \
		OBJ/PROGRAMS/%/PROGRAM_COMPILED/program.objdump \
		$(SCRIPT_DIR)/hex2mem.py
	make OBJ/PROGRAMS/$*/PROGRAM_COMPILED/program$(call encrypted,$@)$(call cs_val,$@).hex 
	@echo "\n===> $@"
	$(SCRIPT_DIR)/hex2mem.py OBJ/PROGRAMS/$*/PROGRAM_COMPILED/program$(call encrypted,$@)$(call cs_val,$@).hex 
	touch $@


#==== GENERATE PATCH MEM FILE ====#
.PRECIOUS: OBJ/PROGRAMS/%/PROGRAM_COMPILED/program_encrypted_patches.mem
.PRECIOUS: OBJ/PROGRAMS/%/PROGRAM_COMPILED/program_encrypted_cs_patches.mem
OBJ/PROGRAMS/%/PROGRAM_COMPILED/program_encrypted_patches.mem \
OBJ/PROGRAMS/%/PROGRAM_COMPILED/program_encrypted_cs-id_patches.mem \
OBJ/PROGRAMS/%/PROGRAM_COMPILED/program_encrypted_cs-id-ex_patches.mem: \
		OBJ/PROGRAMS/%/PROGRAM_COMPILED/program.itb \
		OBJ/PROGRAMS/%/PROGRAM_COMPILED/program_jalr_successors.csv \
		$(SCRIPT_DIR)/riscv-elf-generate-patches.py
	make OBJ/PROGRAMS/$*/PROGRAM_COMPILED/.mem_encrypted$(call cs_val,$@).timestamp
	@echo "\n===> $@"
	$(SCRIPT_DIR)/riscv-elf-generate-patches.py OBJ/PROGRAMS/$*/SIM/REF OBJ/PROGRAMS/$*/PROGRAM_COMPILED $(call cs_flags_sw,$@)



#==== GENERATE ENCRYPTED HEX FILE ====#
.PRECIOUS: OBJ/PROGRAMS/%/PROGRAM_COMPILED/program.hex
.PRECIOUS: OBJ/PROGRAMS/%/PROGRAM_COMPILED/program_encrypted.hex
.PRECIOUS: OBJ/PROGRAMS/%/PROGRAM_COMPILED/program_encrypted_cs.hex
OBJ/PROGRAMS/%/PROGRAM_COMPILED/program.hex \
OBJ/PROGRAMS/%/PROGRAM_COMPILED/program_encrypted.hex \
OBJ/PROGRAMS/%/PROGRAM_COMPILED/program_encrypted_cs-id.hex \
OBJ/PROGRAMS/%/PROGRAM_COMPILED/program_encrypted_cs-id-ex.hex : \
		$(SCRIPT_DIR)/riscv-elf-encryption.py \
		$(SCRIPT_DIR)/ascon_fct.py
	make OBJ/PROGRAMS/$*/PROGRAM_COMPILED/program$(call encrypted,$@)$(call cs_val,$@).elf
	@echo "\n===> $@"
	$(RISCV_EXE_PREFIX)objcopy -O verilog OBJ/PROGRAMS/$*/PROGRAM_COMPILED/program$(call encrypted,$@)$(call cs_val,$@).elf $@
	


#==== ENCRYPT MEMORY ====#
.PRECIOUS: OBJ/PROGRAMS/%/PROGRAM_COMPILED/program_encrypted.elf
.PRECIOUS: OBJ/PROGRAMS/%/PROGRAM_COMPILED/program_encrypted_cs-id.elf
.PRECIOUS: OBJ/PROGRAMS/%/PROGRAM_COMPILED/program_encrypted_cs-id-ex.elf
OBJ/PROGRAMS/%/PROGRAM_COMPILED/program_encrypted.elf \
OBJ/PROGRAMS/%/PROGRAM_COMPILED/program_encrypted_cs-id.elf\
OBJ/PROGRAMS/%/PROGRAM_COMPILED/program_encrypted_cs-id-ex.elf: \
		OBJ/PROGRAMS/%/PROGRAM_COMPILED/program.elf \
		$(SCRIPT_DIR)/riscv-elf-encryption.py \
		$(SCRIPT_DIR)/ascon_fct.py
	@echo "\n===> $@"
	cp $< $@
	$(SCRIPT_DIR)/riscv-elf-encryption.py $@ $(PB_ROUNDS_PY_FLAG) $(call cs_flags_sw,$@)



#==== EXTRACT JALR SUCCESSORS ====#
.PRECIOUS: OBJ/PROGRAMS/%/PROGRAM_COMPILED/program_jalr_successors.csv
OBJ/PROGRAMS/%/PROGRAM_COMPILED/program_jalr_successors.csv : \
		OBJ/PROGRAMS/%/SIM/REF/program_trace_signals.csv \
		$(SCRIPT_DIR)/riscv-get-jalr-successors-from-extracted-signals.py
	@echo "\n===> $@"
	$(SCRIPT_DIR)/riscv-get-jalr-successors-from-extracted-signals.py $< $@
	

#==== GENERATE READELF FILE ====#
.PRECIOUS: OBJ/PROGRAMS/%/PROGRAM_COMPILED/program.readelf
OBJ/PROGRAMS/%/PROGRAM_COMPILED/program.readelf: OBJ/PROGRAMS/%/PROGRAM_COMPILED/program.elf
	@echo "\n===> $@"
	$(RISCV_EXE_PREFIX)readelf -a $< > $@


#==== GENERATE OBJDUMP FILE ====#
.PRECIOUS: OBJ/PROGRAMS/%/PROGRAM_COMPILED/program.objdump
OBJ/PROGRAMS/%/PROGRAM_COMPILED/program.objdump: OBJ/PROGRAMS/%/PROGRAM_COMPILED/program.elf
	@echo "\n===> $@"
	$(RISCV_EXE_PREFIX)objdump \
		-d \
		-M no-aliases \
		-M numeric \
		-S \
		$< > $@



#==== GENERATE ITB FILE FROM OBJDUMP FILE ====#
.PRECIOUS : OBJ/PROGRAMS/%/PROGRAM_COMPILED/program.itb
OBJ/PROGRAMS/%/PROGRAM_COMPILED/program.itb: OBJ/PROGRAMS/%/PROGRAM_COMPILED/program.objdump
	@echo "\n===> $@"
	$(SCRIPT_DIR)/objdump2itb $< > $@


#==== COMPILE PROGRAM ====#
.PRECIOUS : OBJ/PROGRAMS/%/PROGRAM_COMPILED/program.elf
OBJ/PROGRAMS/%/PROGRAM_COMPILED/program.elf: $(OBJ_BSP_DIR)/.bsp.timestamp
	@echo "\n===> $@"
	mkdir -p $(dir $@)
	$(RISCV_EXE_PREFIX)$(RISCV_CC) \
		$(CFLAGS) \
		-I $(OBJ_BSP_DIR) \
		-o $@ \
		-nostartfiles \
		$(filter %.c %.S,$(wildcard  SRC/PROGRAMS/$*/*)) \
		-T $(SRC_BSP_DIR)/link.ld \
		-L $(OBJ_BSP_DIR) \
		-lcv-verif


#==== COMPILE BSP ====#
OBJ/PROGRAM_TOOLS/BSP/.bsp.timestamp :
	@echo "\n===> $@"
	make -C $(SRC_BSP_DIR) \
		VPATH=$(SRC_BSP_DIR) \
		RISCV=$(RISCV) \
		RISCV_PREFIX=$(RISCV_PREFIX) \
		RISCV_EXE_PREFIX=$(RISCV_EXE_PREFIX) \
		RISCV_CC=$(RISCV_CC) \
		all
	mkdir -p $(dir $@)
	mv $(BSP_RESULT_FILES) $(OBJ_BSP_DIR)
	touch $@

                              


##       _                  
##   ___| | ___  __ _ _ __  
##  / __| |/ _ \/ _` | '_ \ 
## | (__| |  __/ (_| | | | |
##  \___|_|\___|\__,_|_| |_|
##                         

#==== CLEAN ===#
.PHONY : clean_vcd
clean_vcd :
	find . -name "*.vcd" -exec rm {} \;

.PHONY : clean_large_vcd
clean_large_vcd :
	find . -size +200M -name "*.vcd" -exec rm {} \;

.PHONY : clean
clean :
	rm explicit_target_names.mk
	rm -rf $(OBJ_DIR)
