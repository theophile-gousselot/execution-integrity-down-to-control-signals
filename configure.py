#!/bin/python3

PROGRAMS=["crc32", "cubic", "dhrystone", "edn", "fibonacci", "huffbench", "matmult-int", "md5sum", "minver", "mont64", "nbody", "nettle-aes", "nettle-sha256", "nsichneu", "picojpeg", "primecount", "qrduino", "sglib-combined", "slre", "st", "statemate", "tarfind", "ud", "verifypin_0", "wikisort"]

def write_targets():
    string = ""
    for p in PROGRAMS:
        string += f"OBJ/PROGRAMS/{p}/SIM/VCD/program.vcd :\n"
        string += f"	make OBJ/PROGRAMS/{p}/SIM/VCD/program.vcd \n\n"
        string += f"OBJ/PROGRAMS/{p}/SIM/VCD/program_encrypted.vcd :\n"
        string += f"	make OBJ/PROGRAMS/{p}/SIM/VCD/program_encrypted.vcd \n\n"
        string += f"OBJ/PROGRAMS/{p}/SIM/LOG/program_save_ref.log :\n"
        string += f"	make OBJ/PROGRAMS/{p}/SIM/LOG/program_save_ref.log \n\n"
        string += f"OBJ/PROGRAMS/{p}/SIM/REF/ref_decode_pc_instr_patch.csv :\n"
        string += f"	make OBJ/PROGRAMS/{p}/SIM/REF/ref_decode_pc_instr_patch.csv \n\n"
        string += f"OBJ/PROGRAMS/{p}/SIM/LOG/program_verif.log :\n"
        string += f"	make OBJ/PROGRAMS/{p}/SIM/LOG/program_verif.log \n\n"
        string += f"OBJ/PROGRAMS/{p}/SIM/LOG/program_encrypted_verif.log :\n"
        string += f"	make OBJ/PROGRAMS/{p}/SIM/LOG/program_encrypted_verif.log \n\n"
        string += f"OBJ/PROGRAMS/{p}/SIM/REF/program_trace_signals.csv :\n"
        string += f"	make OBJ/PROGRAMS/{p}/SIM/REF/program_trace_signals.csv \n\n"
        string += f"OBJ/PROGRAMS/{p}/PROGRAM_COMPILED/.mem.timestamp :\n"
        string += f"	make OBJ/PROGRAMS/{p}/PROGRAM_COMPILED/.mem.timestamp \n\n"
        string += f"OBJ/PROGRAMS/{p}/PROGRAM_COMPILED/.mem_encrypted.timestamp :\n"
        string += f"	make OBJ/PROGRAMS/{p}/PROGRAM_COMPILED/.mem_encrypted.timestamp \n\n"
        string += f"OBJ/PROGRAMS/{p}/PROGRAM_COMPILED/program_encrypted_patches.hex:\n"
        string += f"	make OBJ/PROGRAMS/{p}/PROGRAM_COMPILED/program_encrypted_patches.hex\n\n"
        string += f"OBJ/PROGRAMS/{p}/PROGRAM_COMPILED/program_jalr_successors.csv :\n"
        string += f"	make OBJ/PROGRAMS/{p}/PROGRAM_COMPILED/program_jalr_successors.csv \n\n"
        string += f"OBJ/PROGRAMS/{p}/PROGRAM_COMPILED/program.readelf:\n"
        string += f"	make OBJ/PROGRAMS/{p}/PROGRAM_COMPILED/program.readelf\n\n"
        string += f"OBJ/PROGRAMS/{p}/PROGRAM_COMPILED/program.objdump:\n"
        string += f"	make OBJ/PROGRAMS/{p}/PROGRAM_COMPILED/program.objdump\n\n"
        string += f"OBJ/PROGRAMS/{p}/PROGRAM_COMPILED/program.itb:\n"
        string += f"	make OBJ/PROGRAMS/{p}/PROGRAM_COMPILED/program.itb\n\n"
        string += f"OBJ/PROGRAMS/{p}/PROGRAM_COMPILED/program.hex:\n"
        string += f"	make OBJ/PROGRAMS/{p}/PROGRAM_COMPILED/program.hex\n\n"
        string += f"OBJ/PROGRAMS/{p}/PROGRAM_COMPILED/program_encrypted.hex:\n"
        string += f"	make OBJ/PROGRAMS/{p}/PROGRAM_COMPILED/program_encrypted.hex\n\n"
        string += f"OBJ/PROGRAMS/{p}/PROGRAM_COMPILED/program_encrypted.elf:\n"
        string += f"	make OBJ/PROGRAMS/{p}/PROGRAM_COMPILED/program_encrypted.elf\n\n"
        string += f"OBJ/PROGRAMS/{p}/PROGRAM_COMPILED/program.elf:\n"
        string += f"	make OBJ/PROGRAMS/{p}/PROGRAM_COMPILED/program.elf\n\n"

    with open("explicit_target_names.mk", "w") as f:
        f.write(string)


write_targets()
