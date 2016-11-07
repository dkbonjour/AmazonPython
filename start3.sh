#!/bin/sh
nohup python3 m7.py 1 > m7.txt 2>&1 &
nohup python3 m8.py 1 > m8.txt 2>&1 &
nohup python3 m9.py 1 > m9.txt 2>&1 &