#!/bin/bash

if [[ ! -f ${1} ]] ; then
	echo "please provide a file as input!"
	exit 1
fi
in_file="${1}"
out_file="cleanup.csv"

head -n 1 "${in_file}" > ${out_file}
# make each line unique based on the date+time column
tail -n +2 "${in_file}" | sort -u -t, -k1,2 >> ${out_file}

mv ${out_file} "${in_file}"
