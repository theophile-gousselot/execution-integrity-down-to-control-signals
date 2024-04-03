#!/bin/bash

questa_folders=$(find $1 -iname "*questa" | grep "\.sim") 


for folder in ${questa_folders}
do
	if test -f "${folder}/simulate.log"; then
		if test -f "${folder}/compile.log"; then
			if cat ${folder}/simulate.log | grep -q "EXIT VALID EXECUTION"; then
				simulate_end=$(stat -c '%Y' ${folder}/simulate.log)
				compile_end=$(stat -c '%Y' ${folder}/compile.log)
				simulation_delay=$((${simulate_end}-${compile_end}))
				echo "${folder} ===> $(date -ud "@${simulation_delay}" +"$(( ${simulation_delay}/3600/24 ))j %H:%M:%S")"
			elif cat ${folder}/simulate.log | grep -q "MAXIMUM CYCLE LIMIT"; then
				echo "${folder} ===> MAXIMUM CYCLE LIMIT"
			elif cat ${folder}/simulate.log | grep -q "EXIT ILLEGAL INSN DECODE"; then
				echo "${folder} ===> EXIT ILLEGAL INSN DECODE"
			else
				echo "${folder} ===> ERROR NOT KNOW/IN PROGRESS"
			fi
		fi
	fi
done
