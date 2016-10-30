# -*-coding:utf-8-*-
# Created by 一只尼玛 on 2016/10/8.
# 功能:
#
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
import time
from tool.thread.threadtest1 import *




if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=6) as e:
        tasklist = {"0": [1, 2, 3, 4]}
        for task in tasklist:
            f = e.submit(threada, tasklist[task], task + "t")
            ff = e.submit(threada11, tasklist[task], task + "tt")
        print("inko")
