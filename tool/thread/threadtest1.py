# -*-coding:utf-8-*-
# Created by 一只尼玛 on 2016/10/8.
# 功能:
#

import time
import threading
Goo = 1


def threada(list, name):
    exit()
    global Goo
    time.sleep(2)
    print(name + ":" + str(Goo))
    Goo = Goo + 1
    print(name + ":" + str(Goo))
    print(list)


def threada11(list, name):
    global Goo
    time.sleep(10)
    print(name + ":" + str(Goo))
    Goo = Goo + 2
    print(name + ":" + str(Goo))
    print(list)