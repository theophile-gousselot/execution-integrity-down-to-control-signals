
## Getting Started

1. Simulate execution of `fibonacci`, without encryption and save PC/instr in Fetch at every cycle.
``` bash
 make OBJ/PROGRAMS/fibonacci/SIM/LOG/fibonacci_save_ref.log PROGRAM=fibonacci 
```

2. Simulate execution of `fibonacci`, without encryption, save PC/instr in Fetch at every cycle and **generate waveform**.
``` bash
 make OBJ/PROGRAMS/fibonacci/SIM/LOG/fibonacci_save_ref.log PROGRAM=fibonacci VCD=1
```

3. Simulate execution of `fibonacci`, without encryption, **compare PC/instr in Fetch at every cycle with previously saved reference** and generate waveform.
``` bash
 make OBJ/PROGRAMS/fibonacci/SIM/LOG/fibonacci_verif.log PROGRAM=fibonacci VCD=1
```
  
4. Simulate execution of `fibonacci`, **with encryption**, compare PC/instr in Fetch at every cycle with previously saved reference and generate waveform.
``` bash
 make OBJ/PROGRAMS/fibonacci/SIM/LOG/fibonacci_c_verif.log PROGRAM=fibonacci ENCRYPT=1 VCD=1
```

5. For all programs: simulate without encryption to save PC/instr and with encryption with comparison of PC/instr.
``` bash
source ./launch_sim_all_programs__save_ref__verif.sh
```

6. Every time a simulation is performed, a log file is generated :
    - `OBJ/PROGRAMS/<program_name>/SIM/LOG/<program_name>_save_ref.log`
    - `OBJ/PROGRAMS/<program_name>/SIM/LOG/<program_name>_verif.log`
    - `OBJ/PROGRAMS/<program_name>/SIM/LOG/<program_name>_c_verif.log`

7. Every time a simulation is performed, a line is added in `OBJ/LOG/overview.log`, after `source ./launch_sim_all_programs__save_ref__verif.sh` execution, `overview.log` looks like this:

|   PROGRAM_NAME   | ENCRYPT |   MODE   |    TEST   | REASON END. |  SIM_TIME  | FIRST ERR. |       TIMESTAMP        |
|:----------------:|:-------:|:--------:|:---------:|:-----------:|:----------:|:----------:|:----------------------:|
|       crc32      |         | SAVE_REF |           |  VALID EXEC |    1149079 |            | Tue Mar 19 15:18:06 2024
|       cubic      |         | SAVE_REF |           |  VALID EXEC |    1166633 |            | Tue Mar 19 15:18:07 2024
|     dhrystone    |         | SAVE_REF |           |  VALID EXEC |     611549 |            | Tue Mar 19 15:18:07 2024
|        edn       |         | SAVE_REF |           |  VALID EXEC |     642401 |            | Tue Mar 19 15:18:08 2024
|     fibonacci    |         | SAVE_REF |           |  VALID EXEC |     187693 |            | Tue Mar 19 15:18:08 2024
|     huffbench    |         | SAVE_REF |           |  VALID EXEC |     904147 |            | Tue Mar 19 15:18:09 2024
|    matmult-int   |         | SAVE_REF |           |  VALID EXEC |     839261 |            | Tue Mar 19 15:18:10 2024
|      md5sum      |         | SAVE_REF |           |  VALID EXEC |     681135 |            | Tue Mar 19 15:18:10 2024
|      minver      |         | SAVE_REF |           |  VALID EXEC |     785075 |            | Tue Mar 19 15:18:11 2024
|      mont64      |         | SAVE_REF |           |  VALID EXEC |     515093 |            | Tue Mar 19 15:18:11 2024
|       nbody      |         | SAVE_REF |           |  VALID EXEC |    4387281 |            | Tue Mar 19 15:18:14 2024
|    nettle-aes    |         | SAVE_REF |           |  VALID EXEC |     540219 |            | Tue Mar 19 15:18:15 2024
|   nettle-sha256  |         | SAVE_REF |           |  VALID EXEC |     277931 |            | Tue Mar 19 15:18:15 2024
|     nsichneu     |         | SAVE_REF |           |  VALID EXEC |     306969 |            | Tue Mar 19 15:18:16 2024
|     picojpeg     |         | SAVE_REF |           |  VALID EXEC |    1927667 |            | Tue Mar 19 15:18:18 2024
|    primecount    |         | SAVE_REF |           |  VALID EXEC |     896719 |            | Tue Mar 19 15:18:19 2024
|      qrduino     |         | SAVE_REF |           |  VALID EXEC |    1672565 |            | Tue Mar 19 15:18:20 2024
|  sglib-combined  |         | SAVE_REF |           |  VALID EXEC |     688539 |            | Tue Mar 19 15:18:21 2024
|       slre       |         | SAVE_REF |           |  VALID EXEC |     306599 |            | Tue Mar 19 15:18:22 2024
|        st        |         | SAVE_REF |           |  VALID EXEC |    1126621 |            | Tue Mar 19 15:18:23 2024
|     statemate    |         | SAVE_REF |           |  VALID EXEC |     240825 |            | Tue Mar 19 15:18:23 2024
|      tarfind     |         | SAVE_REF |           |  VALID EXEC |     717311 |            | Tue Mar 19 15:18:24 2024
|        ud        |         | SAVE_REF |           |  VALID EXEC |     588561 |            | Tue Mar 19 15:18:24 2024
|    verifypin_0   |         | SAVE_REF |           |  VALID EXEC |      18937 |            | Tue Mar 19 15:18:25 2024
|     wikisort     |         | SAVE_REF |           |  VALID EXEC |    4297655 |            | Tue Mar 19 15:18:28 2024


|   PROGRAM_NAME   | ENCRYPT |   MODE   |    TEST   | REASON END. |  SIM_TIME  | FIRST ERR. |       TIMESTAMP        |
|:----------------:|:-------:|:--------:|:---------:|:-----------:|:----------:|:----------:|:----------------------:|
|       crc32      | ENCRYPT |   VERIF  |  SUCCESS  |  VALID EXEC |    1149079 |            | Tue Mar 19 15:18:32 2024
|       cubic      | ENCRYPT |   VERIF  |  SUCCESS  |  VALID EXEC |    1166633 |            | Tue Mar 19 16:25:58 2024
|     dhrystone    | ENCRYPT |   VERIF  |  SUCCESS  |  VALID EXEC |     611549 |            | Tue Mar 19 15:18:34 2024
|        edn       | ENCRYPT |   VERIF  |  SUCCESS  |  VALID EXEC |     642401 |            | Tue Mar 19 15:18:37 2024
|     fibonacci    | ENCRYPT |   VERIF  |  SUCCESS  |  VALID EXEC |     187693 |            | Tue Mar 19 15:18:38 2024
|     huffbench    | ENCRYPT |   VERIF  |  SUCCESS  |  VALID EXEC |     904147 |            | Tue Mar 19 15:18:41 2024
|    matmult-int   | ENCRYPT |   VERIF  |  SUCCESS  |  VALID EXEC |     839261 |            | Tue Mar 19 15:18:44 2024
|      md5sum      | ENCRYPT |   VERIF  |  SUCCESS  |  VALID EXEC |     681135 |            | Tue Mar 19 15:18:47 2024
|      minver      | ENCRYPT |   VERIF  |  SUCCESS  |  VALID EXEC |     785075 |            | Tue Mar 19 15:18:50 2024
|      mont64      | ENCRYPT |   VERIF  |  SUCCESS  |  VALID EXEC |     515093 |            | Tue Mar 19 15:18:52 2024
|       nbody      | ENCRYPT |   VERIF  |  SUCCESS  |  VALID EXEC |    4387281 |            | Tue Mar 19 15:19:06 2024
|    nettle-aes    | ENCRYPT |   VERIF  |  SUCCESS  |  VALID EXEC |     540219 |            | Tue Mar 19 15:19:08 2024
|   nettle-sha256  | ENCRYPT |   VERIF  |  SUCCESS  |  VALID EXEC |     277931 |            | Tue Mar 19 15:19:10 2024
|     nsichneu     | ENCRYPT |   VERIF  |  SUCCESS  |  VALID EXEC |     306969 |            | Tue Mar 19 15:19:13 2024
|     picojpeg     | ENCRYPT |   VERIF  |  FAILURE  |  REF ERROR  |      75189 |      75168 | Tue Mar 19 15:19:15 2024
|    primecount    | ENCRYPT |   VERIF  |  SUCCESS  |  VALID EXEC |     896719 |            | Tue Mar 19 15:19:18 2024
|      qrduino     | ENCRYPT |   VERIF  |  FAILURE  |  REF ERROR  |     109745 |     109724 | Tue Mar 19 15:19:20 2024
|  sglib-combined  | ENCRYPT |   VERIF  |  SUCCESS  |  VALID EXEC |     688539 |            | Tue Mar 19 15:19:23 2024
|       slre       | ENCRYPT |   VERIF  |  SUCCESS  |  VALID EXEC |     306599 |            | Tue Mar 19 15:19:25 2024
|        st        | ENCRYPT |   VERIF  |  SUCCESS  |  VALID EXEC |    1126621 |            | Tue Mar 19 15:19:29 2024
|     statemate    | ENCRYPT |   VERIF  |  SUCCESS  |  VALID EXEC |     240825 |            | Tue Mar 19 15:19:31 2024
|      tarfind     | ENCRYPT |   VERIF  |  SUCCESS  |  VALID EXEC |     717311 |            | Tue Mar 19 15:19:33 2024
|        ud        | ENCRYPT |   VERIF  |  SUCCESS  |  VALID EXEC |     588561 |            | Tue Mar 19 15:19:36 2024
|    verifypin_0   | ENCRYPT |   VERIF  |  SUCCESS  |  VALID EXEC |      18937 |            | Tue Mar 19 15:19:37 2024
|     wikisort     | ENCRYPT |   VERIF  |  SUCCESS  |  VALID EXEC |    4297655 |            | Tue Mar 19 15:19:48 2024




## ToExplain:
- jalr_successors.csv
- new cv32e40p branch: adding comments to ignore specifically Verilator Warnings

