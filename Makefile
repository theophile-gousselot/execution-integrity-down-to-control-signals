##################################################
## __     __         _       _     _            ##
## \ \   / /_ _ _ __(_) __ _| |__ | | ___  ___  ##
##  \ \ / / _` | '__| |/ _` | '_ \| |/ _ \/ __| ##
##   \ V / (_| | |  | | (_| | |_) | |  __/\__ \ ##
##    \_/ \__,_|_|  |_|\__,_|_.__/|_|\___||___/ ##
##                                              ##
##################################################

#==== DEFAULT USER MACROS ===#
VCD 				:= 0
VERIF				:= 1
TRACE_PC_INSTR		:= 0
MAX_SIM_TIME		:= 10000000



#==== PROGRAMS ====#


#==== RISCV ====#
RISCV				:= /opt/corev
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
SRC_PROGRAM_DIR		:= $(SRC_DIR)/PROGRAMS

SRC_RTL				:= $(shell cat ./SRC/RTL/rtl.flist)
SRC_RTL_ENCRYPTED	:= $(shell cat ./SRC/RTL/rtl_encrypted.flist)
SRC_TB_FILE			:= $(SV_BENCH_DIR)/core_v_fpga_top_veri_tb.cpp

#==== CV32E40P ====#
CV_CORE_PKG 		:= $(SV_RTL_DIR)/iea_cv32e40p_fpga_dev
CV_CORE_BRANCH 		:= iea_cv32e40p_fpga_dev
CV_CORE_REPO   		:= git@gitlab.emse.fr:theophile.gousselot/cv32e40p_cfi.git

TB_CPP_NAME			:= core_v_fpga_top_veri


#==== OBJECT PATHS ====#
OBJ_DIR                 := ./OBJ
OBJ_PROGRAMS_DIR        := $(OBJ_DIR)/PROGRAMS
OBJ_OVERVIEW_LOG_DIR    := $(OBJ_DIR)/LOG
OBJ_VERI_DIR  := $(OBJ_DIR)/VERILATOR_OBJ_DIR
OBJ_FAST_VERILATOR_DIR  := $(OBJ_VERI_DIR)/$(TB_CPP_NAME)
VERILATOR_EXE 			:= $(OBJ_VERILATOR_DIR)/V$(TB_CPP_NAME)
FAST_VERILATOR_EXE 		:= $(OBJ_FAST_VERILATOR_DIR)/V$(TB_CPP_NAME)
OBJ_TOOLS_DIR           := $(OBJ_DIR)/PROGRAM_TOOLS
OBJ_BSP_DIR             := $(OBJ_TOOLS_DIR)/BSP

OBJ_OVERVIEW_LOG 		:= $(OBJ_OVERVIEW_LOG_DIR)/overview.log




#==== RAISE ERRORS ====#


########################################
##  _____                    _        ##
## |_   _|_ _ _ __ __ _  ___| |_ ___  ##
##   | |/ _` | '__/ _` |/ _ \ __/ __| ##
##   | | (_| | | | (_| |  __/ |_\__ \ ##
##   |_|\__,_|_|  \__, |\___|\__|___/ ##
##                |___/               ##
########################################

$(info MAX_SIM_TIME   = $(MAX_SIM_TIME))

.PHONY: dummy
dummy:
ifeq (,$(wildcard OBJ/LOG/overview.log))
	mkdir -p OBJ/LOG
	@echo "|   PROGRAM_NAME   | ENCRYPT |   MODE   |    TEST   | REASON END. |  SIM_TIME  | FIRST ERR. |       TIMESTAMP         " > OBJ/LOG/overview.log
endif

-include dummy

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

OBJ/PROGRAMS/%/SIM/VCD/program_encrypted.vcd : \
		$(OBJ_VERI_DIR)/$(TB_CPP_NAME)_encrypted_vcd/V$(TB_CPP_NAME) \
		OBJ/PROGRAMS/%/PROGRAM_COMPILED/.mem_encrypted.timestamp \
		OBJ/PROGRAMS/%/PROGRAM_COMPILED/program_encrypted_patches.hex \
		OBJ/PROGRAMS/%/SIM/REF/ref_decode_pc_instr_patch.csv
	@echo "\n===> $@"
	mkdir -p $(dir $@)
	$(OBJ_VERI_DIR)/$(TB_CPP_NAME)_encrypted_vcd/V$(TB_CPP_NAME) $* --verif


#==== SAVE REF ====#
.PRECIOUS: OBJ/PROGRAMS/%/SIM/LOG/program_save_ref.log
OBJ/PROGRAMS/%/SIM/LOG/program_save_ref.log : OBJ/PROGRAMS/%/SIM/REF/ref_decode_pc_instr_patch.csv


.PRECIOUS: OBJ/PROGRAMS/%/SIM/REF/ref_decode_pc_instr_patch.csv
OBJ/PROGRAMS/%/SIM/REF/ref_decode_pc_instr_patch.csv : \
		$(OBJ_VERI_DIR)/$(TB_CPP_NAME)/V$(TB_CPP_NAME) \
		OBJ/PROGRAMS/%/PROGRAM_COMPILED/.mem.timestamp
	@echo "\n===> $@"
	mkdir -p $(dir $@)
	$(OBJ_VERI_DIR)/$(TB_CPP_NAME)/V$(TB_CPP_NAME) $* --save_ref


#==== VERIFICATION ====#
OBJ/PROGRAMS/%/SIM/LOG/program_verif.log :  \
		$(OBJ_VERI_DIR)/$(TB_CPP_NAME)/V$(TB_CPP_NAME) \
		OBJ/PROGRAMS/%/PROGRAM_COMPILED/.mem.timestamp \
		OBJ/PROGRAMS/%/SIM/REF/ref_decode_pc_instr_patch.csv
	@echo "\n===> $@"
	mkdir -p $(dir $@)
	$(OBJ_VERI_DIR)/$(TB_CPP_NAME)/V$(TB_CPP_NAME) $* --verif

OBJ/PROGRAMS/%/SIM/LOG/program_encrypted_verif.log :  \
		$(OBJ_VERI_DIR)/$(TB_CPP_NAME)_encrypted/V$(TB_CPP_NAME) \
		OBJ/PROGRAMS/%/PROGRAM_COMPILED/.mem_encrypted.timestamp \
		OBJ/PROGRAMS/%/PROGRAM_COMPILED/program_encrypted_patches.hex \
		OBJ/PROGRAMS/%/SIM/REF/ref_decode_pc_instr_patch.csv
	@echo "\n===> $@"
	mkdir -p $(dir $@)
	$(OBJ_VERI_DIR)/$(TB_CPP_NAME)_encrypted/V$(TB_CPP_NAME) $* --verif


#==== TRACE SIGNALS ====#
# "$(OBJ_VERI_DIR)/$(TB_CPP_NAME)/V$(TB_CPP_NAME) \" must be added to the dependency list,
# however it induces to compute again jalr_successor beacause of RTL edits, even if the
# edits concern only encryption part.
.PRECIOUS: OBJ/PROGRAMS/%/SIM/REF/program_trace_signals.csv
OBJ/PROGRAMS/%/SIM/REF/program_trace_signals.csv : \
		OBJ/PROGRAMS/%/PROGRAM_COMPILED/.mem.timestamp
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
$(OBJ_VERI_DIR)/$(TB_CPP_NAME)_encrypted_vcd/V$(TB_CPP_NAME) : $(CV_CORE_PKG) $(SRC_RTL_ENCRYPTED) $(SRC_TB_FILE)
	@echo "\n===> $@"
	mkdir -p $(dir $@)
	verilator \
		--trace --trace-depth 5 -CFLAGS "-D VCD" \
		+define+ENCRYPT -CFLAGS "-D ENCRYPT" \
		-CFLAGS "-D MAX_SIM_TIME=$(MAX_SIM_TIME)" \
	   	--Mdir $(OBJ_VERI_DIR)/$(TB_CPP_NAME)_encrypted_vcd \
	   	--cc -sv --exe \
	   	--top-module $(TB_CPP_NAME) ../../$(SRC_TB_FILE) \
	   	-f SRC/RTL/rtl_encrypted.flist
	make \
		-C $(OBJ_VERI_DIR)/$(TB_CPP_NAME)_encrypted_vcd \
		-f V$(TB_CPP_NAME).mk \
		V$(TB_CPP_NAME)


#==== BUILD CPP MODEL with ENCRYPTED PROGRAM ===#
$(OBJ_VERI_DIR)/$(TB_CPP_NAME)_encrypted/V$(TB_CPP_NAME) : $(CV_CORE_PKG) $(SRC_RTL_ENCRYPTED) $(SRC_TB_FILE)
	@echo "\n===> $@"
	mkdir -p $(dir $@)
	verilator \
		+define+ENCRYPT -CFLAGS "-D ENCRYPT" \
		-CFLAGS "-D MAX_SIM_TIME=$(MAX_SIM_TIME)" \
	   	--Mdir $(OBJ_VERI_DIR)/$(TB_CPP_NAME)_encrypted \
	   	--cc -sv --exe \
	   	--top-module $(TB_CPP_NAME) ../../$(SRC_TB_FILE) \
	   	-f SRC/RTL/rtl_encrypted.flist
	make \
		-C $(OBJ_VERI_DIR)/$(TB_CPP_NAME)_encrypted \
		-f V$(TB_CPP_NAME).mk \
		V$(TB_CPP_NAME)


#==== BUILD CPP MODEL with WAVEFORM GENERATION ===#
$(OBJ_VERI_DIR)/$(TB_CPP_NAME)_vcd/V$(TB_CPP_NAME) : $(CV_CORE_PKG) $(SRC_RTL) $(SRC_TB_FILE)
	@echo "\n===> $@"
	mkdir -p $(dir $@)
	verilator \
		--trace --trace-depth 5 -CFLAGS "-D VCD" \
		-CFLAGS "-D MAX_SIM_TIME=$(MAX_SIM_TIME)" \
	   	--Mdir $(OBJ_VERI_DIR)/$(TB_CPP_NAME)_vcd \
	   	--cc -sv --exe \
	   	--top-module $(TB_CPP_NAME) \
		../../$(SRC_TB_FILE) \
	   	-f SRC/RTL/rtl.flist
	make \
		-C $(OBJ_VERI_DIR)/$(TB_CPP_NAME)_vcd \
		-f V$(TB_CPP_NAME).mk \
		V$(TB_CPP_NAME)


#==== BUILD CPP MODEL ===#
$(OBJ_VERI_DIR)/$(TB_CPP_NAME)/V$(TB_CPP_NAME) : $(CV_CORE_PKG) $(SRC_RTL) $(SRC_TB_FILE)
	@echo "\n===> $@"
	mkdir -p $(dir $@)
	verilator \
		-CFLAGS "-D MAX_SIM_TIME=$(MAX_SIM_TIME)" \
	   	--Mdir $(OBJ_VERI_DIR)/$(TB_CPP_NAME) \
	   	--cc -sv --exe \
	   	--top-module $(TB_CPP_NAME) \
		../../$(SRC_TB_FILE) \
	   	-f SRC/RTL/rtl.flist
	make \
		-C $(OBJ_VERI_DIR)/$(TB_CPP_NAME) \
		-f V$(TB_CPP_NAME).mk \
		V$(TB_CPP_NAME)




##  _                   _                        
## | |__   __ _ _ __ __| |_      ____ _ _ __ ___ 
## | '_ \ / _` | '__/ _` \ \ /\ / / _` | '__/ _ \
## | | | | (_| | | | (_| |\ V  V / (_| | | |  __/
## |_| |_|\__,_|_|  \__,_| \_/\_/ \__,_|_|  \___|
##                                               

#==== GIT CLONE CV32E40P ====#
$(CV_CORE_PKG) :
	@echo "\n===> $@"
	git clone -b $(CV_CORE_BRANCH) $(CV_CORE_REPO) $(CV_CORE_PKG); \
	cd $(CV_CORE_PKG); git checkout $(CV_CORE_BRANCH)



##                            _ _       _   _                    __ _               
##   ___ ___  _ __ ___  _ __ (_) | __ _| |_(_) ___  _ __        / _| | _____      __
##  / __/ _ \| '_ ` _ \| '_ \| | |/ _` | __| |/ _ \| '_ \ _____| |_| |/ _ \ \ /\ / /
## | (_| (_) | | | | | | |_) | | | (_| | |_| | (_) | | | |_____|  _| | (_) \ V  V / 
##  \___\___/|_| |_| |_| .__/|_|_|\__,_|\__|_|\___/|_| |_|     |_| |_|\___/ \_/\_/  
##                     |_|                                                          


#==== CONVERT HEX INTO MEM FILES ====#
.PRECIOUS: OBJ/PROGRAMS/%/PROGRAM_COMPILED/.mem.timestamp 
OBJ/PROGRAMS/%/PROGRAM_COMPILED/.mem.timestamp : \
		OBJ/PROGRAMS/%/PROGRAM_COMPILED/program.hex \
		OBJ/PROGRAMS/%/PROGRAM_COMPILED/program.itb  \
		OBJ/PROGRAMS/%/PROGRAM_COMPILED/program.readelf \
		OBJ/PROGRAMS/%/PROGRAM_COMPILED/program.objdump
	@echo "\n===> $@"
	$(SCRIPT_DIR)/hex2mem.py $<
	touch $@
                                           
#==== CONVERT HEX ENCYPTED INTO MEM FILES ====#
.PRECIOUS: OBJ/PROGRAMS/%/PROGRAM_COMPILED/.mem_encrypted.timestamp 
OBJ/PROGRAMS/%/PROGRAM_COMPILED/.mem_encrypted.timestamp : \
		OBJ/PROGRAMS/%/PROGRAM_COMPILED/program_encrypted.hex \
		OBJ/PROGRAMS/%/PROGRAM_COMPILED/program.itb  \
		OBJ/PROGRAMS/%/PROGRAM_COMPILED/program.readelf \
		OBJ/PROGRAMS/%/PROGRAM_COMPILED/program.objdump
	@echo "\n===> $@"
	$(SCRIPT_DIR)/hex2mem.py $<
	touch $@

#==== GENERATE PATCH MEM FILE ====#
.PRECIOUS: OBJ/PROGRAMS/%/PROGRAM_COMPILED/program_encrypted_patches.hex
OBJ/PROGRAMS/%/PROGRAM_COMPILED/program_encrypted_patches.hex: \
		OBJ/PROGRAMS/%/PROGRAM_COMPILED/program.itb \
		OBJ/PROGRAMS/%/PROGRAM_COMPILED/program.elf \
		OBJ/PROGRAMS/%/PROGRAM_COMPILED/program_jalr_successors.csv 
	@echo "\n===> $@"
	$(SCRIPT_DIR)/riscv-elf-generate-patches.py OBJ/PROGRAMS/$*/SIM/REF OBJ/PROGRAMS/$*/PROGRAM_COMPILED 



.PRECIOUS: OBJ/PROGRAMS/%/PROGRAM_COMPILED/program_jalr_successors.csv
OBJ/PROGRAMS/%/PROGRAM_COMPILED/program_jalr_successors.csv : OBJ/PROGRAMS/%/SIM/REF/program_trace_signals.csv
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


#==== GENERATE HEX FILE ====#
.PRECIOUS: OBJ/PROGRAMS/%/PROGRAM_COMPILED/program.hex
OBJ/PROGRAMS/%/PROGRAM_COMPILED/program.hex: OBJ/PROGRAMS/%/PROGRAM_COMPILED/program.elf
	@echo "\n===> $@"
	$(RISCV_EXE_PREFIX)objcopy -O verilog \
		$< \
		$@


#==== GENERATE ENCRYPTED HEX FILE ====#
.PRECIOUS: OBJ/PROGRAMS/%/PROGRAM_COMPILED/program_encrypted.hex
OBJ/PROGRAMS/%/PROGRAM_COMPILED/program_encrypted.hex: OBJ/PROGRAMS/%/PROGRAM_COMPILED/program_encrypted.elf
	@echo "\n===> $@"
	$(RISCV_EXE_PREFIX)objcopy -O verilog \
		$< \
		$@
	
#==== ENCRYPT MEMORY ====#
.PRECIOUS: OBJ/PROGRAMS/%/PROGRAM_COMPILED/program_encrypted.elf
OBJ/PROGRAMS/%/PROGRAM_COMPILED/program_encrypted.elf: OBJ/PROGRAMS/%/PROGRAM_COMPILED/program.elf
	@echo "\n===> $@"
	cp $< $@
	$(SCRIPT_DIR)/riscv-elf-encryption.py $@ $(PB_ROUNDS_PY_FLAG)


#==== COMPILE PROGRAM ====#
.PRECIOUS : OBJ/PROGRAMS/%/PROGRAM_COMPILED/program.elf
OBJ/PROGRAMS/%/PROGRAM_COMPILED/program.elf: $(PROGRAM_FILES) $(OBJ_BSP_DIR)/.bsp.timestamp
	@echo "\n===> $@"
	mkdir -p $(dir $@)
	$(RISCV_EXE_PREFIX)$(RISCV_CC) \
		$(CFLAGS) \
		-I $(OBJ_BSP_DIR) \
		-o $@ \
		-nostartfiles \
		$(filter %.c %.S,$(wildcard  SRC/PROGRAMS/$*/*)) \
		$(PROGRAM_FILES) \
		-T $(SRC_BSP_DIR)/link.ld \
		-L $(OBJ_BSP_DIR) \
		-lcv-verif


#==== COMPILE BSP ====#
$(OBJ_BSP_DIR)/.bsp.timestamp :
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
	rm -rf $(OBJ_DIR)
