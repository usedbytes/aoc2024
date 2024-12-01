#!/bin/bash

DAY=$(printf %d $1)
ZERO_DAY=$(printf %02d $1)

mkdir ${ZERO_DAY}

curl -b "session=${AOC_SESSION}" -o ${ZERO_DAY}/input.txt https://adventofcode.com/2024/day/${DAY}/input

tail -n 3 ${ZERO_DAY}/input.txt

if [ ! -f ${ZERO_DAY}/solve.py ]
then
	cp template.py ${ZERO_DAY}/solve.py
fi
