
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

5. Execute previous command for all programs with a for loop. You may run `watch -n1 tail -n 40 OBJ/LOG/overview.log` in another terminal to follow campaign execution.
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


|   PROGRAM_NAME   | ENCRYPT |C_F|   MODE   |    TEST   | REASON END. |  SIM_TIME  | FIRST ERR. |       TIMESTAMP         
|:----------------:|:-------:|:--------:|:---------:|:-----------:|:----------:|:----------:|:----------------------:|
|       crc32      |         |   |SAVE/TRACE|           |  VALID EXEC |    1149080 |            | Thu Mar 28 09:41:03 2024
|       crc32      | ENCRYPT | 1 |   VERIF  |  SUCCESS  |  VALID EXEC |    1149080 |            | Thu Mar 28 09:44:59 2024
|       cubic      |         |   |SAVE/TRACE|           |  VALID EXEC |    1380282 |            | Thu Mar 28 09:45:02 2024
|       cubic      | ENCRYPT | 1 |   VERIF  |  SUCCESS  |  VALID EXEC |    1380282 |            | Thu Mar 28 09:45:25 2024
|     dhrystone    |         |   |SAVE/TRACE|           |  VALID EXEC |     611550 |            | Thu Mar 28 09:45:26 2024
|     dhrystone    | ENCRYPT | 1 |   VERIF  |  SUCCESS  |  VALID EXEC |     611550 |            | Thu Mar 28 09:45:36 2024
|        edn       |         |   |SAVE/TRACE|           |  VALID EXEC |     642402 |            | Thu Mar 28 09:45:37 2024
|        edn       | ENCRYPT | 1 |   VERIF  |  SUCCESS  |  VALID EXEC |     642402 |            | Thu Mar 28 09:45:47 2024
|     fibonacci    | ENCRYPT | 1 |   VERIF  |  SUCCESS  |  VALID EXEC |     187694 |            | Thu Mar 28 09:45:48 2024
|     huffbench    |         |   |SAVE/TRACE|           |  VALID EXEC |     904196 |            | Thu Mar 28 09:45:49 2024
|     huffbench    | ENCRYPT | 1 |   VERIF  |  SUCCESS  |  VALID EXEC |     904196 |            | Thu Mar 28 09:46:03 2024
|    matmult-int   |         |   |SAVE/TRACE|           |  VALID EXEC |     839262 |            | Thu Mar 28 09:46:04 2024
|    matmult-int   | ENCRYPT | 1 |   VERIF  |  SUCCESS  |  VALID EXEC |     839262 |            | Thu Mar 28 09:46:17 2024
|      md5sum      |         |   |SAVE/TRACE|           |  VALID EXEC |     681136 |            | Thu Mar 28 09:46:19 2024
|      md5sum      | ENCRYPT | 1 |   VERIF  |  SUCCESS  |  VALID EXEC |     681136 |            | Thu Mar 28 09:46:29 2024
|      minver      |         |   |SAVE/TRACE|           |  VALID EXEC |     785076 |            | Thu Mar 28 09:46:31 2024
|      minver      | ENCRYPT | 1 |   VERIF  |  SUCCESS  |  VALID EXEC |     785076 |            | Thu Mar 28 09:46:43 2024
|      mont64      |         |   |SAVE/TRACE|           |  VALID EXEC |     515094 |            | Thu Mar 28 09:46:44 2024
|      mont64      | ENCRYPT | 1 |   VERIF  |  SUCCESS  |  VALID EXEC |     515094 |            | Thu Mar 28 09:46:52 2024
|       nbody      |         |   |SAVE/TRACE|           |  VALID EXEC |    4387282 |            | Thu Mar 28 09:46:57 2024
|       nbody      | ENCRYPT | 1 |   VERIF  |  SUCCESS  |  VALID EXEC |    4387282 |            | Thu Mar 28 09:48:02 2024
|    nettle-aes    |         |   |SAVE/TRACE|           |  VALID EXEC |     540220 |            | Thu Mar 28 09:48:03 2024
|    nettle-aes    | ENCRYPT | 1 |   VERIF  |  SUCCESS  |  VALID EXEC |     540220 |            | Thu Mar 28 09:48:11 2024
|   nettle-sha256  |         |   |SAVE/TRACE|           |  VALID EXEC |     277932 |            | Thu Mar 28 09:48:12 2024
|   nettle-sha256  | ENCRYPT | 1 |   VERIF  |  SUCCESS  |  VALID EXEC |     277932 |            | Thu Mar 28 09:48:17 2024
|     nsichneu     |         |   |SAVE/TRACE|           |  VALID EXEC |     306970 |            | Thu Mar 28 09:48:18 2024
|     nsichneu     | ENCRYPT | 1 |   VERIF  |  SUCCESS  |  VALID EXEC |     306970 |            | Thu Mar 28 09:48:24 2024
|     picojpeg     |         |   |SAVE/TRACE|           |  VALID EXEC |    1927668 |            | Thu Mar 28 09:48:27 2024
|     picojpeg     | ENCRYPT | 1 |   VERIF  |  FAILURE  |  REF ERROR  |      75190 |      75169 | Thu Mar 28 09:48:53 2024
|    primecount    |         |   |SAVE/TRACE|           |  VALID EXEC |     896720 |            | Thu Mar 28 09:48:54 2024
|    primecount    | ENCRYPT | 1 |   VERIF  |  SUCCESS  |  VALID EXEC |     896720 |            | Thu Mar 28 09:49:08 2024
|      qrduino     |         |   |SAVE/TRACE|           |  VALID EXEC |    1672566 |            | Thu Mar 28 09:49:10 2024
|      qrduino     | ENCRYPT | 1 |   VERIF  |  FAILURE  |  REF ERROR  |     109746 |     109725 | Thu Mar 28 09:49:32 2024
|  sglib-combined  |         |   |SAVE/TRACE|           |  VALID EXEC |     688540 |            | Thu Mar 28 09:49:34 2024
|  sglib-combined  | ENCRYPT | 1 |   VERIF  |  SUCCESS  |  VALID EXEC |     688540 |            | Thu Mar 28 09:49:45 2024
|       slre       |         |   |SAVE/TRACE|           |  VALID EXEC |     306600 |            | Thu Mar 28 09:49:46 2024
|       slre       | ENCRYPT | 1 |   VERIF  |  SUCCESS  |  VALID EXEC |     306600 |            | Thu Mar 28 09:49:52 2024
|        st        |         |   |SAVE/TRACE|           |  VALID EXEC |    1126622 |            | Thu Mar 28 09:49:53 2024
|        st        | ENCRYPT | 1 |   VERIF  |  SUCCESS  |  VALID EXEC |    1126622 |            | Thu Mar 28 09:50:11 2024
|     statemate    |         |   |SAVE/TRACE|           |  VALID EXEC |     240826 |            | Thu Mar 28 09:50:12 2024
|     statemate    | ENCRYPT | 1 |   VERIF  |  SUCCESS  |  VALID EXEC |     240826 |            | Thu Mar 28 09:50:16 2024
|      tarfind     |         |   |SAVE/TRACE|           |  VALID EXEC |     717312 |            | Thu Mar 28 09:50:17 2024
|      tarfind     | ENCRYPT | 1 |   VERIF  |  SUCCESS  |  VALID EXEC |     717312 |            | Thu Mar 28 09:50:29 2024
|        ud        |         |   |SAVE/TRACE|           |  VALID EXEC |     588562 |            | Thu Mar 28 09:50:30 2024
|        ud        | ENCRYPT | 1 |   VERIF  |  SUCCESS  |  VALID EXEC |     588562 |            | Thu Mar 28 09:50:39 2024
|    verifypin_0   |         |   |SAVE/TRACE|           |  VALID EXEC |      18938 |            | Thu Mar 28 09:50:40 2024
|    verifypin_0   | ENCRYPT | 1 |   VERIF  |  SUCCESS  |  VALID EXEC |      18938 |            | Thu Mar 28 09:50:41 2024
|     wikisort     |         |   |SAVE/TRACE|           |  VALID EXEC |    3579694 |            | Thu Mar 28 09:50:45 2024
|     wikisort     | ENCRYPT | 1 |   VERIF  |  SUCCESS  |  VALID EXEC |    3579694 |            | Thu Mar 28 09:51:39 2024
|       crc32      | ENCRYPT | 2 |   VERIF  |  SUCCESS  |  VALID EXEC |    2298139 |            | Thu Mar 28 09:51:46 2024
|       cubic      | ENCRYPT | 2 |   VERIF  |  SUCCESS  |  VALID EXEC |    2760543 |            | Thu Mar 28 09:51:49 2024
|     dhrystone    | ENCRYPT | 2 |   VERIF  |  SUCCESS  |  VALID EXEC |    1223079 |            | Thu Mar 28 09:51:50 2024
|        edn       | ENCRYPT | 2 |   VERIF  |  SUCCESS  |  VALID EXEC |    1284783 |            | Thu Mar 28 09:51:52 2024
|     fibonacci    | ENCRYPT | 2 |   VERIF  |  SUCCESS  |  VALID EXEC |     375367 |            | Thu Mar 28 09:51:52 2024
|     huffbench    | ENCRYPT | 2 |   VERIF  |  SUCCESS  |  VALID EXEC |    1808371 |            | Thu Mar 28 09:51:54 2024
|    matmult-int   | ENCRYPT | 2 |   VERIF  |  SUCCESS  |  VALID EXEC |    1678503 |            | Thu Mar 28 09:51:56 2024
|      md5sum      | ENCRYPT | 2 |   VERIF  |  SUCCESS  |  VALID EXEC |    1362251 |            | Thu Mar 28 09:51:57 2024
|      minver      | ENCRYPT | 2 |   VERIF  |  SUCCESS  |  VALID EXEC |    1570131 |            | Thu Mar 28 09:51:59 2024
|      mont64      | ENCRYPT | 2 |   VERIF  |  SUCCESS  |  VALID EXEC |    1030167 |            | Thu Mar 28 09:52:00 2024
|       nbody      | ENCRYPT | 2 |   VERIF  |  SUCCESS  |  VALID EXEC |    8774543 |            | Thu Mar 28 09:52:09 2024
|    nettle-aes    | ENCRYPT | 2 |   VERIF  |  SUCCESS  |  VALID EXEC |    1080419 |            | Thu Mar 28 09:52:11 2024
|   nettle-sha256  | ENCRYPT | 2 |   VERIF  |  SUCCESS  |  VALID EXEC |     555843 |            | Thu Mar 28 09:52:11 2024
|     nsichneu     | ENCRYPT | 2 |   VERIF  |  SUCCESS  |  VALID EXEC |     613919 |            | Thu Mar 28 09:52:12 2024
|     picojpeg     | ENCRYPT | 2 |   VERIF  |  FAILURE  |  REF ERROR  |     150359 |     150338 | Thu Mar 28 09:52:12 2024
|    primecount    | ENCRYPT | 2 |   VERIF  |  SUCCESS  |  VALID EXEC |    1793419 |            | Thu Mar 28 09:52:14 2024
|      qrduino     | ENCRYPT | 2 |   VERIF  |  FAILURE  |  REF ERROR  |     219471 |     219450 | Thu Mar 28 09:52:15 2024
|  sglib-combined  | ENCRYPT | 2 |   VERIF  |  SUCCESS  |  VALID EXEC |    1377059 |            | Thu Mar 28 09:52:16 2024
|       slre       | ENCRYPT | 2 |   VERIF  |  SUCCESS  |  VALID EXEC |     613179 |            | Thu Mar 28 09:52:17 2024
|        st        | ENCRYPT | 2 |   VERIF  |  SUCCESS  |  VALID EXEC |    2253223 |            | Thu Mar 28 09:52:19 2024
|     statemate    | ENCRYPT | 2 |   VERIF  |  SUCCESS  |  VALID EXEC |     481631 |            | Thu Mar 28 09:52:20 2024
|      tarfind     | ENCRYPT | 2 |   VERIF  |  SUCCESS  |  VALID EXEC |    1434603 |            | Thu Mar 28 09:52:21 2024
|        ud        | ENCRYPT | 2 |   VERIF  |  SUCCESS  |  VALID EXEC |    1177103 |            | Thu Mar 28 09:52:23 2024
|    verifypin_0   | ENCRYPT | 2 |   VERIF  |  SUCCESS  |  VALID EXEC |      37855 |            | Thu Mar 28 09:52:23 2024
|     wikisort     | ENCRYPT | 2 |   VERIF  |  SUCCESS  |  VALID EXEC |    7159367 |            | Thu Mar 28 09:52:30 2024
|       crc32      | ENCRYPT | 3 |   VERIF  |  SUCCESS  |  VALID EXEC |    3447198 |            | Thu Mar 28 09:52:33 2024
|       cubic      | ENCRYPT | 3 |   VERIF  |  SUCCESS  |  VALID EXEC |    4140804 |            | Thu Mar 28 09:52:36 2024
|     dhrystone    | ENCRYPT | 3 |   VERIF  |  SUCCESS  |  VALID EXEC |    1834608 |            | Thu Mar 28 09:52:37 2024
|        edn       | ENCRYPT | 3 |   VERIF  |  SUCCESS  |  VALID EXEC |    1927164 |            | Thu Mar 28 09:52:39 2024
|     fibonacci    | ENCRYPT | 3 |   VERIF  |  SUCCESS  |  VALID EXEC |     563040 |            | Thu Mar 28 09:52:39 2024
|     huffbench    | ENCRYPT | 3 |   VERIF  |  SUCCESS  |  VALID EXEC |    2712546 |            | Thu Mar 28 09:52:41 2024
|    matmult-int   | ENCRYPT | 3 |   VERIF  |  SUCCESS  |  VALID EXEC |    2517744 |            | Thu Mar 28 09:52:43 2024
|      md5sum      | ENCRYPT | 3 |   VERIF  |  SUCCESS  |  VALID EXEC |    2043366 |            | Thu Mar 28 09:52:44 2024
|      minver      | ENCRYPT | 3 |   VERIF  |  SUCCESS  |  VALID EXEC |    2355186 |            | Thu Mar 28 09:52:46 2024
|      mont64      | ENCRYPT | 3 |   VERIF  |  SUCCESS  |  VALID EXEC |    1545240 |            | Thu Mar 28 09:52:47 2024
|       nbody      | ENCRYPT | 3 |   VERIF  |  SUCCESS  |   TIMEOUT   |   10000000 |            | Thu Mar 28 09:52:55 2024
|    nettle-aes    | ENCRYPT | 3 |   VERIF  |  SUCCESS  |  VALID EXEC |    1620618 |            | Thu Mar 28 09:52:56 2024
|   nettle-sha256  | ENCRYPT | 3 |   VERIF  |  SUCCESS  |  VALID EXEC |     833754 |            | Thu Mar 28 09:52:57 2024
|     nsichneu     | ENCRYPT | 3 |   VERIF  |  SUCCESS  |  VALID EXEC |     920868 |            | Thu Mar 28 09:52:58 2024
|     picojpeg     | ENCRYPT | 3 |   VERIF  |  FAILURE  |  REF ERROR  |     225528 |     225507 | Thu Mar 28 09:52:58 2024
|    primecount    | ENCRYPT | 3 |   VERIF  |  SUCCESS  |  VALID EXEC |    2690118 |            | Thu Mar 28 09:53:00 2024
|      qrduino     | ENCRYPT | 3 |   VERIF  |  FAILURE  |  REF ERROR  |     329196 |     329175 | Thu Mar 28 09:53:00 2024
|  sglib-combined  | ENCRYPT | 3 |   VERIF  |  SUCCESS  |  VALID EXEC |    2065578 |            | Thu Mar 28 09:53:02 2024
|       slre       | ENCRYPT | 3 |   VERIF  |  SUCCESS  |  VALID EXEC |     919758 |            | Thu Mar 28 09:53:03 2024
|        st        | ENCRYPT | 3 |   VERIF  |  SUCCESS  |  VALID EXEC |    3379824 |            | Thu Mar 28 09:53:05 2024
|     statemate    | ENCRYPT | 3 |   VERIF  |  SUCCESS  |  VALID EXEC |     722436 |            | Thu Mar 28 09:53:06 2024
|      tarfind     | ENCRYPT | 3 |   VERIF  |  SUCCESS  |  VALID EXEC |    2151894 |            | Thu Mar 28 09:53:07 2024
|        ud        | ENCRYPT | 3 |   VERIF  |  SUCCESS  |  VALID EXEC |    1765644 |            | Thu Mar 28 09:53:09 2024
|    verifypin_0   | ENCRYPT | 3 |   VERIF  |  SUCCESS  |  VALID EXEC |      56772 |            | Thu Mar 28 09:53:09 2024
|     wikisort     | ENCRYPT | 3 |   VERIF  |  SUCCESS  |   TIMEOUT   |   10000000 |            | Thu Mar 28 09:53:16 2024
|       crc32      | ENCRYPT | 6 |   VERIF  |  SUCCESS  |  VALID EXEC |    6894375 |            | Thu Mar 28 09:53:33 2024
|       cubic      | ENCRYPT | 6 |   VERIF  |  SUCCESS  |  VALID EXEC |    8281587 |            | Thu Mar 28 09:53:36 2024
|     dhrystone    | ENCRYPT | 6 |   VERIF  |  SUCCESS  |  VALID EXEC |    3669195 |            | Thu Mar 28 09:53:38 2024
|        edn       | ENCRYPT | 6 |   VERIF  |  SUCCESS  |  VALID EXEC |    3854307 |            | Thu Mar 28 09:53:40 2024
|     fibonacci    | ENCRYPT | 6 |   VERIF  |  SUCCESS  |  VALID EXEC |    1126059 |            | Thu Mar 28 09:53:40 2024
|     huffbench    | ENCRYPT | 6 |   VERIF  |  SUCCESS  |  VALID EXEC |    5425071 |            | Thu Mar 28 09:53:42 2024
|    matmult-int   | ENCRYPT | 6 |   VERIF  |  SUCCESS  |  VALID EXEC |    5035467 |            | Thu Mar 28 09:53:45 2024
|      md5sum      | ENCRYPT | 6 |   VERIF  |  SUCCESS  |  VALID EXEC |    4086711 |            | Thu Mar 28 09:53:46 2024
|      minver      | ENCRYPT | 6 |   VERIF  |  SUCCESS  |  VALID EXEC |    4710351 |            | Thu Mar 28 09:53:49 2024
|      mont64      | ENCRYPT | 6 |   VERIF  |  SUCCESS  |  VALID EXEC |    3090459 |            | Thu Mar 28 09:53:50 2024
|       nbody      | ENCRYPT | 6 |   VERIF  |  SUCCESS  |   TIMEOUT   |   10000000 |            | Thu Mar 28 09:53:55 2024
|    nettle-aes    | ENCRYPT | 6 |   VERIF  |  SUCCESS  |  VALID EXEC |    3241215 |            | Thu Mar 28 09:53:56 2024
|   nettle-sha256  | ENCRYPT | 6 |   VERIF  |  SUCCESS  |  VALID EXEC |    1667487 |            | Thu Mar 28 09:53:57 2024
|     nsichneu     | ENCRYPT | 6 |   VERIF  |  SUCCESS  |  VALID EXEC |    1841715 |            | Thu Mar 28 09:53:58 2024
|     picojpeg     | ENCRYPT | 6 |   VERIF  |  FAILURE  |  REF ERROR  |     451035 |     451014 | Thu Mar 28 09:53:58 2024
|    primecount    | ENCRYPT | 6 |   VERIF  |  SUCCESS  |  VALID EXEC |    5380215 |            | Thu Mar 28 09:54:01 2024
|      qrduino     | ENCRYPT | 6 |   VERIF  |  FAILURE  |  REF ERROR  |     658371 |     658350 | Thu Mar 28 09:54:01 2024
|  sglib-combined  | ENCRYPT | 6 |   VERIF  |  SUCCESS  |  VALID EXEC |    4131135 |            | Thu Mar 28 09:54:03 2024
|       slre       | ENCRYPT | 6 |   VERIF  |  SUCCESS  |  VALID EXEC |    1839495 |            | Thu Mar 28 09:54:04 2024
|        st        | ENCRYPT | 6 |   VERIF  |  SUCCESS  |  VALID EXEC |    6759627 |            | Thu Mar 28 09:54:07 2024
|     statemate    | ENCRYPT | 6 |   VERIF  |  SUCCESS  |  VALID EXEC |    1444851 |            | Thu Mar 28 09:54:08 2024
|      tarfind     | ENCRYPT | 6 |   VERIF  |  SUCCESS  |  VALID EXEC |    4303767 |            | Thu Mar 28 09:54:09 2024
|        ud        | ENCRYPT | 6 |   VERIF  |  SUCCESS  |  VALID EXEC |    3531267 |            | Thu Mar 28 09:54:11 2024
|    verifypin_0   | ENCRYPT | 6 |   VERIF  |  SUCCESS  |  VALID EXEC |     113523 |            | Thu Mar 28 09:54:11 2024
|     wikisort     | ENCRYPT | 6 |   VERIF  |  SUCCESS  |   TIMEOUT   |   10000000 |            | Thu Mar 28 09:54:16 2024




## ToExplain:
- jalr_successors.csv
- new cv32e40p branch: adding comments to ignore specifically Verilator Warnings

