#!/bin/sh
nohup python3 m4.py 1 > m4.txt 2>&1 &
nohup python3 m5.py 1 > m5.txt 2>&1 &
nohup python3 m6.py 1 > m6.txt 2>&1 &