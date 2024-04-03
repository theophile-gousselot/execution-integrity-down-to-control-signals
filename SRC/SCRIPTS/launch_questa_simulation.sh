#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Error: missing path to questa folder"
	exit
fi

# Execute compile.sh, elaborate.sh and simulate.sh in the questa dir given
(cd $1 && ./compile.sh && ./elaborate.sh && ./simulate.sh)
