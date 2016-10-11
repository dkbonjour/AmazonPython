# !/usr/bin/python3.4
# -*-coding:utf-8-*-
# Created by Smartdo Co.,Ltd. on 2016/10/11.
# 功能:
#  
import sys
import traceback

if __name__ == "__main__":

    try:
        1/0
    except Exception as e:
        exc_type, exc_value, exc_tb = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_tb)