
## Getting Started

1. Simulate execution of `fibonacci`, without encryption and save PC/instr in Fetch at every cycle.
``` bash
 make OBJ/PROGRAMS/fibonacci/SIM/LOG/program_save_ref.log
```

2. Simulate execution of `fibonacci`, without encryption, **compare PC/instr in Fetch at every cycle with previously saved reference**, generate reference if not exist.
``` bash
 make OBJ/PROGRAMS/fibonacci/SIM/LOG/program_verif.log
```

3. Simulate execution of `fibonacci`, without encryption, **compare PC/instr in Fetch at every cycle with previously saved reference** and generate waveform.
``` bash
 make OBJ/PROGRAMS/fibonacci/SIM/VCD/program.vcd
```
  
4. Simulate execution of `fibonacci`, **with encryption**, compare PC/instr in Fetch at every cycle with previously saved reference, generate reference if not exist.
``` bash
 make OBJ/PROGRAMS/fibonacci/SIM/LOG/program_encrypted_verif.log
```

5. Execute previous command for all programs with a for loop.
``` bash
for program in SRC/PROGRAMS/* ; do make OBJ/PROGRAMS/$(basename $(program))/SIM/LOG/program_encrypted_verif.log; done
for cf in 1 2 3 6; do for a in SRC/PROGRAMS/* ; do make OBJ/PROGRAMS/$(basename $a)/SIM/LOG/program_encrypted_cf${cf}_verif.log; done; done
```

6. Every time a simulation is performed, a log file is generated :
    - `OBJ/PROGRAMS/<program_name>/SIM/LOG/<program_name>_save_ref.log`
    - `OBJ/PROGRAMS/<program_name>/SIM/LOG/<program_name>_verif.log`
    - `OBJ/PROGRAMS/<program_name>/SIM/LOG/<program_name>_encrypted_verif.log`

7. Explicit target names can be generated.
``` bash
python3 ./configure.py
make -f explicit_target_names.mk <tab>
```

8. Every time a simulation is performed, a line is added in `OBJ/LOG/overview.log`, after step **5**, `overview.log` looks like this:

|   PROGRAM_NAME   | ENCRYPT |   MODE   |    TEST   | REASON END. |  SIM_TIME  | FIRST ERR. |       TIMESTAMP
|:----------------:|:-------:|:--------:|:---------:|:-----------:|:----------:|:----------:|:----------------------:|
|       crc32      |         |SAVE/TRACE|           |  VALID EXEC |    1149080 |            | Tue Mar 26 16:41:13 2024
|       crc32      |         | SAVE_REF |           |  VALID EXEC |    1149080 |            | Tue Mar 26 16:41:29 2024
|       crc32      | ENCRYPT |   VERIF  |  SUCCESS  |  VALID EXEC |    1149080 |            | Tue Mar 26 16:41:32 2024
|       cubic      |         |SAVE/TRACE|           |  VALID EXEC |    1380282 |            | Tue Mar 26 16:41:34 2024
|       cubic      |         | SAVE_REF |           |  VALID EXEC |    1380282 |            | Tue Mar 26 16:41:55 2024
|       cubic      | ENCRYPT |   VERIF  |  SUCCESS  |  VALID EXEC |    1380282 |            | Tue Mar 26 16:41:58 2024
|     dhrystone    |         |SAVE/TRACE|           |  VALID EXEC |     611550 |            | Tue Mar 26 16:41:59 2024
|     dhrystone    |         | SAVE_REF |           |  VALID EXEC |     611550 |            | Tue Mar 26 16:42:08 2024
|     dhrystone    | ENCRYPT |   VERIF  |  SUCCESS  |  VALID EXEC |     611550 |            | Tue Mar 26 16:42:09 2024
|        edn       |         |SAVE/TRACE|           |  VALID EXEC |     642402 |            | Tue Mar 26 16:42:10 2024
|        edn       |         | SAVE_REF |           |  VALID EXEC |     642402 |            | Tue Mar 26 16:42:19 2024
|        edn       | ENCRYPT |   VERIF  |  SUCCESS  |  VALID EXEC |     642402 |            | Tue Mar 26 16:42:21 2024
|     fibonacci    |         |SAVE/TRACE|           |  VALID EXEC |     187694 |            | Tue Mar 26 16:42:21 2024
|     fibonacci    |         | SAVE_REF |           |  VALID EXEC |     187694 |            | Tue Mar 26 16:42:25 2024
|     fibonacci    | ENCRYPT |   VERIF  |  SUCCESS  |  VALID EXEC |     187694 |            | Tue Mar 26 16:42:25 2024
|     huffbench    |         |SAVE/TRACE|           |  VALID EXEC |     904196 |            | Tue Mar 26 16:42:26 2024
|     huffbench    |         | SAVE_REF |           |  VALID EXEC |     904196 |            | Tue Mar 26 16:42:39 2024
|     huffbench    | ENCRYPT |   VERIF  |  SUCCESS  |  VALID EXEC |     904196 |            | Tue Mar 26 16:42:41 2024
|    matmult-int   |         |SAVE/TRACE|           |  VALID EXEC |     839262 |            | Tue Mar 26 16:42:42 2024
|    matmult-int   |         | SAVE_REF |           |  VALID EXEC |     839262 |            | Tue Mar 26 16:42:54 2024
|    matmult-int   | ENCRYPT |   VERIF  |  SUCCESS  |  VALID EXEC |     839262 |            | Tue Mar 26 16:42:56 2024
|      md5sum      |         |SAVE/TRACE|           |  VALID EXEC |     681136 |            | Tue Mar 26 16:42:57 2024
|      md5sum      |         | SAVE_REF |           |  VALID EXEC |     681136 |            | Tue Mar 26 16:43:06 2024
|      md5sum      | ENCRYPT |   VERIF  |  SUCCESS  |  VALID EXEC |     681136 |            | Tue Mar 26 16:43:08 2024
|      minver      |         |SAVE/TRACE|           |  VALID EXEC |     785076 |            | Tue Mar 26 16:43:09 2024
|      minver      |         | SAVE_REF |           |  VALID EXEC |     785076 |            | Tue Mar 26 16:43:21 2024
|      minver      | ENCRYPT |   VERIF  |  SUCCESS  |  VALID EXEC |     785076 |            | Tue Mar 26 16:43:23 2024
|      mont64      |         |SAVE/TRACE|           |  VALID EXEC |     515094 |            | Tue Mar 26 16:43:24 2024
|      mont64      |         | SAVE_REF |           |  VALID EXEC |     515094 |            | Tue Mar 26 16:43:31 2024
|      mont64      | ENCRYPT |   VERIF  |  SUCCESS  |  VALID EXEC |     515094 |            | Tue Mar 26 16:43:33 2024
|       nbody      |         |SAVE/TRACE|           |  VALID EXEC |    4387282 |            | Tue Mar 26 16:43:38 2024
|       nbody      |         | SAVE_REF |           |  VALID EXEC |    4387282 |            | Tue Mar 26 16:44:35 2024
|       nbody      | ENCRYPT |   VERIF  |  SUCCESS  |  VALID EXEC |    4387282 |            | Tue Mar 26 16:44:46 2024
|    nettle-aes    |         |SAVE/TRACE|           |  VALID EXEC |     540220 |            | Tue Mar 26 16:44:47 2024
|    nettle-aes    |         | SAVE_REF |           |  VALID EXEC |     540220 |            | Tue Mar 26 16:44:54 2024
|    nettle-aes    | ENCRYPT |   VERIF  |  SUCCESS  |  VALID EXEC |     540220 |            | Tue Mar 26 16:44:55 2024
|   nettle-sha256  |         |SAVE/TRACE|           |  VALID EXEC |     277932 |            | Tue Mar 26 16:44:56 2024
|   nettle-sha256  |         | SAVE_REF |           |  VALID EXEC |     277932 |            | Tue Mar 26 16:45:01 2024
|   nettle-sha256  | ENCRYPT |   VERIF  |  SUCCESS  |  VALID EXEC |     277932 |            | Tue Mar 26 16:45:01 2024
|     nsichneu     |         |SAVE/TRACE|           |  VALID EXEC |     306970 |            | Tue Mar 26 16:45:03 2024
|     nsichneu     |         | SAVE_REF |           |  VALID EXEC |     306970 |            | Tue Mar 26 16:45:08 2024
|     nsichneu     | ENCRYPT |   VERIF  |  SUCCESS  |  VALID EXEC |     306970 |            | Tue Mar 26 16:45:08 2024
|     picojpeg     |         |SAVE/TRACE|           |  VALID EXEC |    1927668 |            | Tue Mar 26 16:45:11 2024
|     picojpeg     |         | SAVE_REF |           |  VALID EXEC |    1927668 |            | Tue Mar 26 16:45:37 2024
|     picojpeg     | ENCRYPT |   VERIF  |  FAILURE  |  REF ERROR  |      75190 |      75169 | Tue Mar 26 16:45:38 2024
|    primecount    |         |SAVE/TRACE|           |  VALID EXEC |     896720 |            | Tue Mar 26 16:45:39 2024
|    primecount    |         | SAVE_REF |           |  VALID EXEC |     896720 |            | Tue Mar 26 16:45:51 2024
|    primecount    | ENCRYPT |   VERIF  |  SUCCESS  |  VALID EXEC |     896720 |            | Tue Mar 26 16:45:54 2024
|      qrduino     |         |SAVE/TRACE|           |  VALID EXEC |    1672566 |            | Tue Mar 26 16:45:56 2024
|      qrduino     |         | SAVE_REF |           |  VALID EXEC |    1672566 |            | Tue Mar 26 16:46:19 2024
|      qrduino     | ENCRYPT |   VERIF  |  FAILURE  |  REF ERROR  |     109746 |     109725 | Tue Mar 26 16:46:20 2024
|  sglib-combined  |         |SAVE/TRACE|           |  VALID EXEC |     688540 |            | Tue Mar 26 16:46:21 2024
|  sglib-combined  |         | SAVE_REF |           |  VALID EXEC |     688540 |            | Tue Mar 26 16:46:31 2024
|  sglib-combined  | ENCRYPT |   VERIF  |  SUCCESS  |  VALID EXEC |     688540 |            | Tue Mar 26 16:46:33 2024
|       slre       |         |SAVE/TRACE|           |  VALID EXEC |     306600 |            | Tue Mar 26 16:46:34 2024
|       slre       |         | SAVE_REF |           |  VALID EXEC |     306600 |            | Tue Mar 26 16:46:39 2024
|       slre       | ENCRYPT |   VERIF  |  SUCCESS  |  VALID EXEC |     306600 |            | Tue Mar 26 16:46:39 2024
|        st        |         |SAVE/TRACE|           |  VALID EXEC |    1126622 |            | Tue Mar 26 16:46:41 2024
|        st        |         | SAVE_REF |           |  VALID EXEC |    1126622 |            | Tue Mar 26 16:46:57 2024
|        st        | ENCRYPT |   VERIF  |  SUCCESS  |  VALID EXEC |    1126622 |            | Tue Mar 26 16:46:59 2024
|     statemate    |         |SAVE/TRACE|           |  VALID EXEC |     240826 |            | Tue Mar 26 16:47:00 2024
|     statemate    |         | SAVE_REF |           |  VALID EXEC |     240826 |            | Tue Mar 26 16:47:04 2024
|     statemate    | ENCRYPT |   VERIF  |  SUCCESS  |  VALID EXEC |     240826 |            | Tue Mar 26 16:47:04 2024
|      tarfind     |         |SAVE/TRACE|           |  VALID EXEC |     717312 |            | Tue Mar 26 16:47:06 2024
|      tarfind     |         | SAVE_REF |           |  VALID EXEC |     717312 |            | Tue Mar 26 16:47:18 2024
|      tarfind     | ENCRYPT |   VERIF  |  SUCCESS  |  VALID EXEC |     717312 |            | Tue Mar 26 16:47:20 2024
|        ud        |         |SAVE/TRACE|           |  VALID EXEC |     588562 |            | Tue Mar 26 16:47:21 2024
|        ud        |         | SAVE_REF |           |  VALID EXEC |     588562 |            | Tue Mar 26 16:47:30 2024
|        ud        | ENCRYPT |   VERIF  |  SUCCESS  |  VALID EXEC |     588562 |            | Tue Mar 26 16:47:32 2024
|    verifypin_0   |         |SAVE/TRACE|           |  VALID EXEC |      18938 |            | Tue Mar 26 16:47:32 2024
|    verifypin_0   |         | SAVE_REF |           |  VALID EXEC |      18938 |            | Tue Mar 26 16:47:34 2024
|    verifypin_0   | ENCRYPT |   VERIF  |  SUCCESS  |  VALID EXEC |      18938 |            | Tue Mar 26 16:47:34 2024
|     wikisort     |         |SAVE/TRACE|           |  VALID EXEC |    3579694 |            | Tue Mar 26 16:47:38 2024
|     wikisort     |         | SAVE_REF |           |  VALID EXEC |    3579694 |            | Tue Mar 26 16:48:27 2024
|     wikisort     | ENCRYPT |   VERIF  |  SUCCESS  |  VALID EXEC |    3579694 |            | Tue Mar 26 16:48:35 2024




## ToExplain:
- jalr_successors.csv
- new cv32e40p branch: adding comments to ignore specifically Verilator Warnings

