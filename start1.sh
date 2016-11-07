#!/bin/sh
nohup python3 m1.py 1 > m1.txt 2>&1 &
nohup python3 m2.py 1 > m2.txt 2>&1 &
nohup python3 m3.py 1 > m3.txt 2>&1 &