# !/usr/bin/python3.4
# -*-coding:utf-8-*-
# Created by Smartdo Co.,Ltd. on 2016/10/11.
# 功能:
#  
import sys
import traceback
from tool.jfile.file import *
import random
from lxml import etree

if __name__ == "__main__":
    for i in range(88):
        print(random.randint(5-1,5+2))
    print([] is None)
    print([] == None)
    print(not [])
    print(False == [])
    print(False is [])
    print('-' * 10)
    print({} is None)
    print({} == None)
    print(not {})
    print(False == {})
    print(False is {})
    print('-' * 10)
    print('' is None)
    print('' == None)
    print(not '')
    print(False == '')
    print(False is '')
    print('-' * 10)
    print(None is None)
    print(None == None)
    print(not None)
    print(False == None)
    print(False is None)
    # try:
    #     1/0
    # except Exception as e:
    #     exc_type, exc_value, exc_tb = sys.exc_info()
    #     traceback.print_exception(exc_type, exc_value, exc_tb)

    # if "dd".encode("utf-8")==0 or 0==None:
    #     print("*"*10)
    # for i in listfiles("../data/rateurl/2urls", "-url.md"):
    #     print(i)
    # try:
    #     raise Exception("机器人")
    # except Exception as e:
    #     if (str(e) == "机器人"):
    #         print("fff")
    text='''
    <html>
<head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" /></head>
<body>
<h1>Unauthorized ...</h1>
<h2>
IP Address: 116.21.25.191<br>
MAC Address: <br>
Server Time: 2016-10-28 22:42:07<br>
Auth Result: 无效用户.
</h2>
</body>
</html>
    '''
    contents = etree.HTML(text)
    # <title dir="ltr">Robot Check</title>
    try:
        robots = contents.xpath('//title/text()')
        if robots==[]:
            print("dd")
    except Exception as e:
        raise
    if robots==[]:
        print("dd")
