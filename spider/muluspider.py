# !/usr/bin/python3.4
# -*-coding:utf-8-*-
# Created by Smartdo Co.,Ltd. on 2016/10/10.
# 功能:
#

import requests
from lxml import etree
import os
import time
import random
from action.proxy import *




# 找出文件夹下所有xml后缀的文件，可选择递归
def listfiles(rootdir, prefix='.xml', iscur=False):
    file = []
    for parent, dirnames, filenames in os.walk(rootdir):
        if parent == rootdir:
            for filename in filenames:
                if filename.endswith(prefix):
                    file.append(filename)
            if not iscur:
                return file
        else:
            if iscur:
                for filename in filenames:
                    if filename.endswith(prefix):
                        file.append(filename)
            else:
                pass
    return file


if __name__ == '__main__':

    if 'onename.txt' in listfiles("../txt","txt"):
        # 将文件写入数组
        arr_oneurl = []
        arr_onename = []
        fileurlone = open("../txt/oneurl.txt")
        urllines = fileurlone.readlines()
        for line in urllines:
            arr_oneurl.append(line.replace("\n",""))
        fileurlone.close()

        filenameone = open("../txt/onename.txt")
        namelines = filenameone.readlines()
        for line in namelines:
            arr_onename.append(line.replace("\n",""))
        filenameone.close()
        print("一级类目已经存在，直接抓取二级类目的url...")
    else:
        ##下面是一级类目的抓取
        # 一级目录下的网址
        firsturl = "https://www.amazon.com/Best-Sellers/zgbs"

        # ('UTF-8')('unicode_escape')('gbk','ignore')
        onecontent = get(firsturl).decode('Utf-8', 'ignore')

        # xpath解析需要的东西
        onecontents = etree.HTML(onecontent)

        # 找到一级类目下的url
        oneurls = onecontents.xpath('//ul[@id="zg_browseRoot"]/ul/li/a/@href')

        # 将一级目录下的url储存到数组
        arr_oneurl = []
        for oneurl in oneurls:
            arr_oneurl.append(oneurl)
        print(arr_oneurl)
        #print(len(arr_oneurl))


        # 找到一级类目下的类目名称
        onenames = onecontents.xpath('//ul[@id="zg_browseRoot"]/ul/li/a/text()')

        # 将一级目录下的泪目名称储存到数组
        arr_onename = []
        for onename in onenames:
            arr_onename.append(onename)
        #print(arr_onename)
        #print(len(arr_onename))

        # 写入txt
        fileurlone = open("../txt/oneurl.txt","w+")
        for item in arr_oneurl:
            fileurlone.write(str(item)+"\n")
        fileurlone.close()

        filenameone = open("../txt/onename.txt","w+")
        for item in arr_onename:
            filenameone.write(str(item)+"\n")
        filenameone.close()
        print("已经抓取了一级类目下的所有url...")

    ##下面是二级类目的抓取
    # 用来储存二级类目下的数组
    arr_towurl = []
    arr_towname = []

    # 用来记录抓取的是哪一个txt文件
    arr_towurlnum = []
    arr_townamenum = []

    if '1-1name.txt' in listfiles("../txt/2urls","txt"):
        alltxt = listfiles("../txt/2urls","txt")
        for txt in alltxt:
            # 建立两个临时数组来构造多维数组
            temp_towurl = []
            temp_towname = []
            #print(txt)
            if "url" in txt:
                fileurltow = open("../txt/2urls/" + txt)
                urllines = fileurltow.readlines()
                for line in urllines:
                    temp_towurl.append(line.replace("\n",""))
                fileurltow.close()

                arr_towurlnum.append(txt.replace("-1url.txt",""))
                arr_towurl.append(temp_towurl)
            else:
                filenametow = open("../txt/2urls/" + txt)
                namelines = filenametow.readlines()
                for line in namelines:
                    temp_towname.append(line.replace("\n",""))
                filenametow.close()

                arr_townamenum.append(txt.replace("-1name.txt",""))
                arr_towname.append(temp_towname)

        print("二级类目已经存在，直接抓取三级类目的url...")

    else:
        for tow in range(0,len(arr_oneurl)):

            towcontent = get(arr_oneurl[tow]).decode('Utf-8', 'ignore')
            # xpath解析需要的东西
            towcontents = etree.HTML(towcontent)
            # 建立一个临时数组来储存二级类目下的东西
            tempurl = []
            tempname = []

            # 找到二级类目下的url
            towurls = towcontents.xpath('//ul[@id="zg_browseRoot"]/ul/ul/li/a/@href')

            # 将二级目录下的url储存到临时数组
            for towurl in towurls:
                tempurl.append(towurl)

            # 找到二级类目下的类目名称
            townames = towcontents.xpath('//ul[@id="zg_browseRoot"]/ul/ul/li/a/text()')

            # 将二级目录下的泪目名称储存到临时数组
            for towname in townames:
                tempname.append(towname)

            arr_towurl.append(tempurl)
            arr_towname.append(tempname)
            print("已经抓取了第" + str(tow + 1) + "个一级类目下的二级类目...")
            # 每一次下载都暂停1-3秒
            loadtime = random.randint(1, 3)
            print("抓取网页暂停" + str(loadtime) + "秒")
            #time.sleep(loadtime)

        number = 1
        for itemurl1 in arr_towurl:
            num = 1
            fileurltow = open("../txt/2urls/" + str(number) + "-" + str(num) + "url.txt","w+")
            for itemurl2 in itemurl1:
                fileurltow.write(str(itemurl2)+"\n")
            fileurltow.close()
            number = number + 1

        number = 1
        for itemname1 in arr_towname:
            num = 1
            filenametow = open("../txt/2urls/" + str(number) + "-" + str(num) + "name.txt","w+")
            for itemname2 in itemname1:
                filenametow.write(str(itemname2)+"\n")
            filenametow.close()
            number = number + 1

    # 用来打印检查的
    #print(arr_towurl)
    #print(arr_towname)
    #print(len(arr_towurl))
    #print(len(arr_towname))


    ##下面是三级类目的抓取
    # 用来储存三级类目下的数组
    arr_threeurl = []
    arr_threename = []

    # 用来记录抓取的是哪一个txt文件
    arr_threeurlnum = []
    arr_threenamenum = []

    if '1-1-1-2name.txt' in listfiles("../txt/2urls/3urls","txt"):
        alltxt = listfiles("../txt/2urls/3urls","txt")
        for txt in alltxt:
            # 建立两个临时数组来构造多维数组
            temp_threeurl = []
            temp_threename = []
            #print(txt)
            if "url" in txt:
                fileurlthree = open("../txt/2urls/3urls/" + txt)
                urllines = fileurlthree.readlines()
                for line in urllines:
                    temp_threeurl.append(line.replace("\n",""))
                fileurlthree.close()

                arr_threeurlnum.append(txt.replace("-2url.txt",""))
                arr_threeurl.append(temp_threeurl)
            else:
                filenamethree = open("../txt/2urls/3urls/" + txt)
                namelines = filenamethree.readlines()
                for line in namelines:
                    temp_threename.append(line.replace("\n",""))
                filenamethree.close()

                arr_threenamenum.append(txt.replace("-2name.txt",""))
                arr_threename.append(temp_threename)
        print("三级类目已经存在，直接抓取四级类目的url...")

    else:
        print(len(arr_towurl))
        for three1 in range(0,len(arr_towurl)):
            print(len(arr_towurl) - three1)
            # 建立一个临时数组来储存三级类目下的东西
            tempurlthree = []
            tempnamethree = []
            if len(arr_towurl[three1]) != 0:
                for three2 in range(0,len(arr_towurl[three1])):
                    print(arr_towurl[three1][three2])
                    threecontent = get(arr_towurl[three1][three2]).decode('Utf-8', 'ignore')

                    # 保存html到本地
                    #filehtml = open("../html/2html/3html", "w+")


                    # xpath解析需要的东西
                    threecontents = etree.HTML(threecontent)
                    # 建立一个临时数组来储存三级类目下的东西
                    tempurl = []
                    tempname = []

                    # 找到三级类目下的url
                    threeurls = threecontents.xpath('//ul[@id="zg_browseRoot"]/ul/ul/ul/li/a/@href')

                    # 将三级目录下的url储存到临时数组
                    for threeurl in threeurls:
                        tempurl.append(threeurl)

                    # 找到三级类目下的类目名称
                    threenames = threecontents.xpath('//ul[@id="zg_browseRoot"]/ul/ul/ul/li/a/text()')

                    # 将三级目录下的类目名称储存到临时数组
                    for threename in threenames:
                        tempname.append(threename)

                    tempurlthree.append(tempurl)
                    tempnamethree.append(tempname)

            arr_threeurl.append(tempurlthree)
            arr_threename.append(tempnamethree)

            print("已经抓取了第" + str(three1 + 1) + "个二级类目下的三级类目...")

            if(three1 == 40):
                break

        number = 1
        for itemurl1 in arr_threeurl:
            num = 2
            num1 = 1
            for itemurl2 in itemurl1:
                fileurlthree = open("../txt/2urls/3urls/" + str(number) + "-" + str(num1) + "-" + str(arr_towurlnum[number - 1]) + "-" + str(num) + "url.txt","w+")
                for itemurl3 in itemurl2:
                    fileurlthree.write(str(itemurl3)+"\n")
                fileurlthree.close()
                num1 = num1 + 1
            number = number + 1

        number = 1
        for itemname1 in arr_threename:
            num = 2
            num1 = 1
            for itemname2 in itemname1:
                filenamethree = open("../txt/2urls/3urls/" + str(number) + "-" + str(num1) + "-" + str(arr_townamenum[number - 1]) + "-" + str(num) + "name.txt","w+")
                for itemname3 in itemname2:
                    filenamethree.write(str(itemname3)+"\n")
                filenamethree.close()
                num1 = num1 + 1
            number = number + 1

    # 用来打印检查的
    #print(arr_threeurl)
    #print(arr_threename)
    #print(len(arr_threeurl))
    #print(len(arr_threename))


    ##下面是四级类目的抓取
    # 用来储存四级类目下的数组
    arr_foururl = []
    arr_fourname = []

    # 用来记录抓取的是哪一个txt文件
    arr_foururlnum = []
    arr_fournamenum = []

    if "1-1-1-1-3name.txt" in listfiles("../txt/2urls/3urls/4urls","txt"):
        alltxt = listfiles("../txt/2urls/3urls/4urls","txt")
        for txt in alltxt:
            # 建立两个临时数组来构造多维数组
            temp_foururl = []
            temp_fourname = []
            #print(txt)
            if "url" in txt:
                fileurlthree = open("../txt/2urls/3urls/4urls/" + txt)
                urllines = fileurlthree.readlines()
                for line in urllines:
                    temp_foururl.append(line.replace("\n",""))
                fileurlthree.close()

                arr_foururlnum.append(txt.replace("-3url.txt",""))
                arr_foururl.append(temp_foururl)
            else:
                filenamefour = open("../txt/2urls/3urls/4urls/" + txt)
                namelines = filenamefour.readlines()
                for line in namelines:
                    temp_fourname.append(line.replace("\n",""))
                filenamefour.close()

                arr_fournamenum.append(txt.replace("-3name.txt",""))
                arr_fourname.append(temp_fourname)

        print("四级类目已经存在，直接抓取五级类目的url...")

    else:
        for four1 in range(0,len(arr_threeurl)):
            # 建立一个临时数组来储存四级类目下的东西
            tempurlfour = []
            tempnamefour = []

            if len(arr_threeurl[four1]) != 0:
                for four2 in range(0,len(arr_threeurl[four1])):
                    print(arr_threeurl[four1][four2])
                    fourcontent = get(arr_threeurl[four1][four2]).decode('Utf-8', 'ignore')

                    # xpath解析需要的东西
                    fourcontents = etree.HTML(fourcontent)

                    # 建立一个临时数组来储存四级类目下的东西
                    tempurl = []
                    tempname = []

                     # 找到四级类目下的url
                    foururls = fourcontents.xpath('//ul[@id="zg_browseRoot"]/ul/ul/ul/ul/li/a/@href')

                    # 将四级目录下的url储存到临时数组
                    for foururl in foururls:
                        tempurl.append(foururl)

                    # 找到四级类目下的类目名称
                    fournames = fourcontents.xpath('//ul[@id="zg_browseRoot"]/ul/ul/ul/ul/li/a/text()')

                    # 将四级目录下的类目名称储存到临时数组
                    for fourname in fournames:
                        tempname.append(fourname)

                    tempurlfour.append(tempurl)
                    tempnamefour.append(tempname)


            arr_foururl.append(tempurlfour)
            arr_fourname.append(tempnamefour)

            print("已经抓取了第" + str(four1 + 1) + "个三级txt下的四级类目url，还剩下" + str(len(arr_threeurl) - four1 + 1) + "个txt的url...")

        # 纯属是用来计数
        number = 1
        for itemurl1 in arr_foururl:
            # 这里的3代表该类目的上级是3
            num = 3
            # 这个代表是该txt下的第几个url
            num1 = 1
            for itemurl2 in itemurl1:
                fileurlfour = open("../txt/2urls/3urls/4urls/" + str(number) + "-" + str(num1) + "-" + str(arr_threeurlnum[number - 1]) + "-" + str(num) + "url.txt","w+")
                for itemurl3 in itemurl2:
                    fileurlfour.write(str(itemurl3)+"\n")
                fileurlfour.close()
                num1 = num1 + 1
            number = number + 1

        # 纯属是用来计数
        number = 1
        for itemname1 in arr_fourname:
            # 这里的3代表该类目的上级是3
            num = 3
            # 这个代表是该txt下的第几个url
            num1 = 1
            for itemname2 in itemname1:
                filenamefour = open("../txt/2urls/3urls/4urls/" + str(number) + "-" + str(num1) + "-" + str(arr_threenamenum[number - 1]) + "-" + str(num) + "name.txt","w+")
                for itemname3 in itemname2:
                    filenamefour.write(str(itemname3)+"\n")
                filenamefour.close()
                num1 = num1 + 1
            number = number + 1

    ##下面是五级类目的抓取
    # 用来储存五级类目下的数组
    arr_fiveurl = []
    arr_fivename = []

    for five1 in range(0,len(arr_foururl)):
        # 建立一个临时数组来储存五级类目下的东西
        tempurlfive = []
        tempnamefive = []

        if len(arr_foururl[five1]) != 0:
            for five2 in range(0,len(arr_foururl[five1])):
                print(arr_foururl[five1][five2])
                fivecontent = get(arr_foururl[five1][five2]).decode('Utf-8', 'ignore')

                # xpath解析需要的东西
                fivecontents = etree.HTML(fivecontent)

                # 建立一个临时数组来储存五级类目下的东西
                tempurl = []
                tempname = []

                 # 找到五级类目下的url
                fiveurls = fivecontents.xpath('//ul[@id="zg_browseRoot"]/ul/ul/ul/ul/ul/li/a/@href')

                # 将五级目录下的url储存到临时数组
                for fiveurl in fiveurls:
                    tempurl.append(fiveurl)

                # 找到五级类目下的类目名称
                fivenames = fivecontents.xpath('//ul[@id="zg_browseRoot"]/ul/ul/ul/ul/ul/li/a/text()')

                # 将五级目录下的类目名称储存到临时数组
                for fivename in fivenames:
                    tempname.append(fivename)

                tempurlfive.append(tempurl)
                tempnamefive.append(tempname)


        arr_fiveurl.append(tempurlfive)
        arr_fivename.append(tempnamefive)

        print("已经抓取了第" + str(four1 + 1) + "个四级txt下的五级类目url，还剩下" + str(len(arr_threeurl) - four1 + 1) + "个txt的url...")

    # 纯属是用来计数
    number = 1
    for itemurl1 in arr_foururl:
        # 这里的4代表该类目的上级是4
        num = 4
        # 这个代表是该txt下的第几个url
        num1 = 1
        for itemurl2 in itemurl1:
            fileurlfive = open("../txt/2urls/3urls/4urls/5urls/" + str(number) + "-" + str(num1) + "-" + str(arr_foururlnum[number - 1]) + "-" + str(num) + "url.txt","w+")
            for itemurl3 in itemurl2:
                fileurlfive.write(str(itemurl3)+"\n")
            fileurlfive.close()
            num1 = num1 + 1
        number = number + 1

    # 纯属是用来计数
    number = 1
    for itemname1 in arr_fourname:
        # 这里的4代表该类目的上级是4
        num = 4
        # 这个代表是该txt下的第几个url
        num1 = 1
        for itemname2 in itemname1:
            filenamefive = open("../txt/2urls/3urls/4urls/5urls/" + str(number) + "-" + str(num1) + "-" + str(arr_fournamenum[number - 1]) + "-" + str(num) + "name.txt","w+")
            for itemname3 in itemname2:
                filenamefive.write(str(itemname3)+"\n")
            filenamefive.close()
            num1 = num1 + 1
        number = number + 1