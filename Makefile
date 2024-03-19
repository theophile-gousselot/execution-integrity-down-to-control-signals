##################################################
## __     __         _       _     _            ##
## \ \   / /_ _ _ __(_) __ _| |__ | | ___  ___  ##
##  \ \ / / _` | '__| |/ _` | '_ \| |/ _ \/ __| ##
##   \ V / (_| | |  | | (_| | |_) | |  __/\__ \ ##
##    \_/ \__,_|_|  |_|\__,_|_.__/|_|\___||___/ ##
##                                              ##
##################################################

#==== DEFAULT USER MACROS ===#
ENCRYPT				:= 0
VCD 				:= 0
VERIF				:= 1
TRACE_PC_INSTR		:= 0
MAX_SIM_TIME		:= 10000000



#==== PROGRAMS ====#
PROGRAM				:= verifypin_0
ifneq (${ENCRYPT}, 0)
ENC_EXT				:= _c
VERILATOR_FLAG 		:= +define+ENCRYPT -CFLAGS "-D ENCRYPT" $(VERILATOR_FLAG)
endif

VERILATOR_FLAG 		:= -CFLAGS "-D MAX_SIM_TIME=$(MAX_SIM_TIME)" $(VERILATOR_FLAG)
ifneq (${VCD}, 0)
VCD_EXT				:= _vcd
VERILATOR_FLAG 		:= --trace --trace-depth 5 -CFLAGS "-D VCD" $(VERILATOR_FLAG)
endif


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
PROGRAM_FILES		:= $(filter %.c %.S,$(wildcard  $(SRC_PROGRAM_DIR)/$(PROGRAM)/*))

SRC_RTL				:= $(shell cat ./SRC/RTL/rtl.flist)
SRC_BENCH			:= $(SV_BENCH_DIR)/core_v_fpga_top_veri_tb.cpp

#==== CV32E40P ====#
CV_CORE_PKG 		:= $(SV_RTL_DIR)/iea_cv32e40p_fpga_dev
CV_CORE_BRANCH 		:= iea_cv32e40p_fpga_dev
CV_CORE_REPO   		:= git@gitlab.emse.fr:theophile.gousselot/cv32e40p_cfi.git

TOP_MODULE			:= core_v_fpga_top_veri


#==== OBJECT PATHS ====#
OBJ_DIR                 := ./OBJ
OBJ_PROGRAMS_DIR        := $(OBJ_DIR)/PROGRAMS
OBJ_PROGRAM_DIR         := $(OBJ_PROGRAMS_DIR)/$(PROGRAM)
OBJ_SIM_DIR             := $(OBJ_PROGRAM_DIR)/SIM
OBJ_LOG_DIR             := $(OBJ_SIM_DIR)/LOG
OBJ_REF_DIR             := $(OBJ_SIM_DIR)/REF
OBJ_VCD_DIR             := $(OBJ_SIM_DIR)/VCD
OBJ_COMPILED_DIR        := $(OBJ_PROGRAM_DIR)/PROGRAM_COMPILED
OBJ_PROGRAM_PREFIX      := $(OBJ_COMPILED_DIR)/$(PROGRAM)
OBJ_OVERVIEW_LOG_DIR    := $(OBJ_DIR)/LOG
OBJ_MAIN_VERILATOR_DIR  := $(OBJ_DIR)/VERILATOR_OBJ_DIR
OBJ_VERILATOR_DIR       := $(OBJ_MAIN_VERILATOR_DIR)/$(TOP_MODULE)$(ENC_EXT)$(VCD_EXT)
VERILATOR_EXE 			:= $(OBJ_VERILATOR_DIR)/V$(TOP_MODULE)
OBJ_TOOLS_DIR           := $(OBJ_DIR)/PROGRAM_TOOLS
OBJ_BSP_DIR             := $(OBJ_TOOLS_DIR)/BSP

OBJ_OVERVIEW_LOG 		:= $(OBJ_OVERVIEW_LOG_DIR)/overview.log

ifneq (${ENCRYPT}, 0)
SIM_DEPENDENCIES 	:= $(OBJ_PROGRAM_PREFIX)_c_patches.hex
endif



#==== MEMORY FILES ====#
MEM := \
	$(OBJ_PROGRAM_PREFIX)_mem0.mem \
	$(OBJ_PROGRAM_PREFIX)_mem1.mem \
	$(OBJ_PROGRAM_PREFIX)_mem2.mem \
	$(OBJ_PROGRAM_PREFIX)_mem3.mem

ifneq (${ENCRYPT}, 0)
MEM := \
	$(OBJ_PROGRAM_PREFIX)_mem0_c.mem \
	$(OBJ_PROGRAM_PREFIX)_mem1_c.mem \
	$(OBJ_PROGRAM_PREFIX)_mem2_c.mem \
	$(OBJ_PROGRAM_PREFIX)_mem3_c.mem \
	$(OBJ_PROGRAM_PREFIX)_patches.mem 
MEM_PATCHES := \
	$(OBJ_PROGRAM_PREFIX)_patches.mem
endif



#==== RAISE ERRORS ====#
ifndef PROGRAM_FILES
$(error $(PROGRAM), no such file or directory in $(SRC_PROGRAM_DIR)/$(PROGRAM))
endif


########################################
##  _____                    _        ##
## |_   _|_ _ _ __ __ _  ___| |_ ___  ##
##   | |/ _` | '__/ _` |/ _ \ __/ __| ##
##   | | (_| | | | (_| |  __/ |_\__ \ ##
##   |_|\__,_|_|  \__, |\___|\__|___/ ##
##                |___/               ##
########################################

$(info PROGRAM        = $(PROGRAM))
$(info ENCRYPT        = $(ENCRYPT))
$(info MAX_SIM_TIME   = $(MAX_SIM_TIME))


##                 _ _       _             
## __   _____ _ __(_) | __ _| |_ ___  _ __ 
## \ \ / / _ \ '__| | |/ _` | __/ _ \| '__|
##  \ V /  __/ |  | | | (_| | || (_) | |   
##   \_/ \___|_|  |_|_|\__,_|\__\___/|_|   
##                                         


$(OBJ_LOG_DIR)/$(PROGRAM)_save_ref.log : $(OBJ_OVERVIEW_LOG) $(VERILATOR_EXE) $(OBJ_COMPILED_DIR)/.mem$(ENC_EXT).timestamp $(SIM_DEPENDENCIES)
	@echo  "\n\n########## SIMULATE  ##########"
	mkdir -p $(OBJ_DIR) $(OBJ_OVERVIEW_LOG_DIR) $(OBJ_VCD_DIR) $(OBJ_LOG_DIR) $(OBJ_REF_DIR)
	$(VERILATOR_EXE) $(PROGRAM) --save_ref

$(OBJ_LOG_DIR)/$(PROGRAM)$(ENC_EXT)_verif.log : $(OBJ_OVERVIEW_LOG) $(VERILATOR_EXE) $(OBJ_COMPILED_DIR)/.mem$(ENC_EXT).timestamp $(SIM_DEPENDENCIES)
	@echo  "\n\n########## SIMULATE  ##########"
	mkdir -p $(OBJ_DIR) $(OBJ_OVERVIEW_LOG_DIR) $(OBJ_VCD_DIR) $(OBJ_LOG_DIR) $(OBJ_REF_DIR)
	$(VERILATOR_EXE) $(PROGRAM) --verif


$(VERILATOR_EXE) : $(CV_CORE_PKG) $(SRC_RTL) $(SRC_BENCH)
	@echo  "\n\n########## COMPILE RTL/BENCH and BUILD VERILATOR EXECUTABLE ##########"
	mkdir -p $(OBJ_DIR) $(OBJ_MAIN_VERILATOR_DIR)
	verilator $(VERILATOR_FLAG) --Mdir $(OBJ_VERILATOR_DIR) --cc -sv --exe --top-module $(TOP_MODULE) ../../$(SRC_BENCH) -f SRC/RTL/rtl.flist
	make -C $(OBJ_VERILATOR_DIR) -f V$(TOP_MODULE).mk V$(TOP_MODULE)

$(OBJ_OVERVIEW_LOG) :
	mkdir -p $(OBJ_DIR) $(OBJ_OVERVIEW_LOG_DIR)
	@echo "|   PROGRAM_NAME   | ENCRYPT |   MODE   |    TEST   | REASON END. |  SIM_TIME  | FIRST ERR. |       TIMESTAMP         " > $(OBJ_OVERVIEW_LOG)



##  _                   _                        
## | |__   __ _ _ __ __| |_      ____ _ _ __ ___ 
## | '_ \ / _` | '__/ _` \ \ /\ / / _` | '__/ _ \
## | | | | (_| | | | (_| |\ V  V / (_| | | |  __/
## |_| |_|\__,_|_|  \__,_| \_/\_/ \__,_|_|  \___|
##                                               

#==== GIT CLONE CV32E40P ====#
$(CV_CORE_PKG) :
	@echo  "\n\n########## CLONE CV32E40P CORE ##########"
	git clone -b $(CV_CORE_BRANCH) $(CV_CORE_REPO) $(CV_CORE_PKG); \
	cd $(CV_CORE_PKG); git checkout $(CV_CORE_BRANCH)



##                            _ _       _   _                    __ _               
##   ___ ___  _ __ ___  _ __ (_) | __ _| |_(_) ___  _ __        / _| | _____      __
##  / __/ _ \| '_ ` _ \| '_ \| | |/ _` | __| |/ _ \| '_ \ _____| |_| |/ _ \ \ /\ / /
## | (_| (_) | | | | | | |_) | | | (_| | |_| | (_) | | | |_____|  _| | (_) \ V  V / 
##  \___\___/|_| |_| |_| .__/|_|_|\__,_|\__|_|\___/|_| |_|     |_| |_|\___/ \_/\_/  
##                     |_|                                                          
                                           
#==== CONVERT HEX INTO MEM FILES ====#
$(OBJ_COMPILED_DIR)/.mem$(ENC_EXT).timestamp : $(OBJ_PROGRAM_PREFIX)$(ENC_EXT).hex $(OBJ_PROGRAM_PREFIX).itb $(OBJ_PROGRAM_PREFIX).readelf $(OBJ_PROGRAM_PREFIX).objdump
	@echo  "\n\n########## GENERATING MEMORY FILE ##########"
	$(SCRIPT_DIR)/hex2mem.py $<
	touch $@

#==== GENERATE PATCH MEM FILE ====#
$(OBJ_PROGRAM_PREFIX)_c_patches.hex : $(OBJ_PROGRAM_PREFIX).itb $(OBJ_PROGRAM_PREFIX)$(ENC_EXT).elf
	@echo "\n\n########## GENERATING PATCH MEMORY FILE ##########"
	$(SCRIPT_DIR)/riscv-elf-generate-patches.py $(PROGRAM) $(SRC_PROGRAM_DIR) $(OBJ_COMPILED_DIR)


#==== ENCRYPT MEMORY ====#
$(OBJ_PROGRAM_PREFIX)_c.elf: $(OBJ_PROGRAM_PREFIX).elf
	@echo "\n\n########## ENCRYPTING MEMORY FILE ##########"
	cp $< $@
	$(SCRIPT_DIR)/riscv-elf-encryption.py $@ $(PB_ROUNDS_PY_FLAG)


#==== GENERATE HEX FILE ====#
$(OBJ_PROGRAM_PREFIX).hex: $(OBJ_PROGRAM_PREFIX).elf
	@echo "\n\n########## GENERATING HEX FILE ##########"
	$(RISCV_EXE_PREFIX)objcopy -O verilog \
		$< \
		$@


#==== GENERATE ENCRYPTED HEX FILE ====#
$(OBJ_PROGRAM_PREFIX)_c.hex: $(OBJ_PROGRAM_PREFIX)_c.elf
	@echo  "\n\n########## GENERATING ENCRYPTED HEX FILE ##########"
	$(RISCV_EXE_PREFIX)objcopy -O verilog \
		$< \
		$@


#==== GENERATE READELF FILE ====#
$(OBJ_PROGRAM_PREFIX).readelf : $(OBJ_PROGRAM_PREFIX).elf
	@echo "\n\n########## GENERATING READELF FILE ##########"
	$(RISCV_EXE_PREFIX)readelf -a $< > $(OBJ_PROGRAM_PREFIX).readelf


#==== GENERATE OBJDUMP FILE ====#
$(OBJ_PROGRAM_PREFIX).objdump : $(OBJ_PROGRAM_PREFIX).elf
	@echo  "\n\n########## GENERATING OBJDUMP FILE ##########"
	$(RISCV_EXE_PREFIX)objdump \
		-d \
		-M no-aliases \
		-M numeric \
		-S \
		$(OBJ_PROGRAM_PREFIX).elf > $(OBJ_PROGRAM_PREFIX).objdump



#==== GENERATE ITB FILE FROM HEX FILE ====#
$(OBJ_PROGRAM_PREFIX).itb : $(OBJ_PROGRAM_PREFIX).hex
	@echo  "\n\n########## GENERATING ITB FILE ##########"
	$(RISCV_EXE_PREFIX)objdump \
		-d \
		-S \
		-M no-aliases \
		-M numeric \
		-l \
		$(OBJ_PROGRAM_PREFIX).elf | $(SCRIPT_DIR)/objdump2itb - > $(OBJ_PROGRAM_PREFIX).itb


#==== COMPILE PROGRAM ====#
.PRECIOUS : %.elf
$(OBJ_PROGRAM_PREFIX).elf: $(PROGRAM_FILES) $(OBJ_BSP_DIR)/.bsp.timestamp
	@echo  "\n\n########## COMPILING $@ ##########"
	mkdir -p $(OBJ_COMPILED_DIR)
	$(RISCV_EXE_PREFIX)$(RISCV_CC) \
		$(CFLAGS) \
		-I $(OBJ_BSP_DIR) \
		-o $@ \
		-nostartfiles \
		$(PROGRAM_FILES) \
		-T $(SRC_BSP_DIR)/link.ld \
		-L $(OBJ_BSP_DIR) \
		-lcv-verif


#==== COMPILE BSP ====#
$(OBJ_BSP_DIR)/.bsp.timestamp :
	@echo  "\n\n########## COMPILING THE BSP ##########"
	make -C $(SRC_BSP_DIR) \
		VPATH=$(SRC_BSP_DIR) \
		RISCV=$(RISCV) \
		RISCV_PREFIX=$(RISCV_PREFIX) \
		RISCV_EXE_PREFIX=$(RISCV_EXE_PREFIX) \
		RISCV_CC=$(RISCV_CC) \
		all
	mkdir -p $(OBJ_DIR) $(OBJ_PROGRAMS_DIR) $(OBJ_PROGRAM_DIR) $(OBJ_BSP_DIR)
	mv $(BSP_RESULT_FILES) $(OBJ_BSP_DIR)
	touch $@

                              


##       _                  
##   ___| | ___  __ _ _ __  
##  / __| |/ _ \/ _` | '_ \ 
## | (__| |  __/ (_| | | | |
##  \___|_|\___|\__,_|_| |_|
##                         

#==== CLEAN ===#
.PHONY : clean
clean_vcd :
	find . -name "*.vcd" -exec rm {} \;

.PHONY : clean
clean_large_vcd :
	find . -size +200M -name "*.vcd" -exec rm {} \;

.PHONY : clean
clean :
	rm -rf $(OBJ_DIR)
