# !/usr/bin/python3.4
# -*- coding: utf-8 -*-

import redis
import time


# 这里用来读取ip
def getips():
    ip = []
    # 读取ip
    file = open("../ip/ip.txt")
    ips = file.readlines()
    # 将ip写入数组并加上时间戳
    for item in ips:
        # 标记时间戳
        markedtime = int(time.time())
        ip.append(item.strip() + "*" + str(markedtime))
    return ip


# 传入带有时间戳的ip数组
def test(ips):
    # 在这里打开redis
    r = redis.Redis(host='127.0.0.1', port=6379, db=0)

    # 删除旧的列队
    r.delete("mylist")

    # 将ip添加进消息列队
    for item in ips:
        r.lpush("mylist", item)

    # 逐个取出和存储
    # 因为要一直取所以用while
    while True:
        # 逐个取出
        temppop = r.rpop("mylist")

        # 去除*号后面的东西
        splitstar = temppop.decode('utf-8', 'ignore').split("*")

        # 得到间隔大于3秒的ip
        # 当前时间
        nowtime = int(time.time())
        # 如果时间间隔大于3就取出来使用
        if nowtime - int(splitstar[1]) >= 3:
            ip = splitstar[0]
            print("取出ip：" + str(ip))
        else:
            # 如果间隔小于3秒则重新写入列队
            r.lpush("mylist", temppop)
            # 跳过这次循环
            continue

        # 这里写解析函数
        # 如果消费了这个ip就逐个写入
        # ......


        # 逐个写入
        # 标记时间戳
        markedtime = int(time.time())
        # 构造格式
        temppush = str(ip) + "*" + str(markedtime)

        # 写入列队
        r.lpush("mylist", temppush)
        # 不知道怎么一个一个的返回
        input('---' * 10)
        # return ip


if __name__ == '__main__':
    a = test(getips())
    print(a)
