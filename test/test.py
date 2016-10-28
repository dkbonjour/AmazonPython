# !/usr/bin/python3.4
# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
import os
import shutil

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

# 取得URL参数
def geturlattr(url):
    # p/seller/at-a-glance.html/ref=dp_merchant_link?ie=UTF8&seller=AJ11J3FSAZ6XV&isAmazonFulfilled=
    returnmap = {}
    try:
        temp = url.split("?")[1].split("&")
        for i in temp:
            temptemp = i.split("=")
            try:
                returnmap[temptemp[0]] = temptemp[1]
            except:
                pass
    except:
        pass
    return returnmap

def pinfoparse(content):
    returnlist = {}
    soup = BeautifulSoup(content, 'html.parser')
    #--------------------------------------------------#


    header = soup.find("div", attrs={"id": "centerCol"})
    if header == None:
        header = soup.find("div", attrs={"id": "leftCol"})
    if header == None:
        header = soup.find("div", attrs={"id": "ppdBuyBox"})
    if header == None:
        header = soup.find("div", attrs={"id": "center-col"})

    dafen = header.find("span", attrs={"id": "acrPopover"})

    # 打分
    if dafen:
        try:
            dafentemp = float(dafen["title"].replace(" out of 5 stars", ""))
            returnlist["score"] = dafentemp

        except Exception as err:
            try:
                dafentemp = float(dafen.get_text().strip().replace(" out of 5 stars", ""))
                returnlist["score"] = dafentemp
            except Exception as err:

                #logger.error(err, exc_info=1)
                returnlist["score"] = -1

    else:
        try:
            # <div id="averageCustomerReviewRating" class="txtnormal clearboth">4.0 out of 5 stars</div>
            dafen = soup.find("div", attrs={"id": "averageCustomerReviewRating"})
            dafentemp = float(dafen["title"].replace(" out of 5 stars", ""))
            returnlist["score"] = dafentemp
        except Exception as err:
            try:
                dafen = soup.find("div", attrs={"id": "averageCustomerReviewRating"})
                dafentemp = float(dafen.get_text().strip().replace(" out of 5 stars", ""))
                returnlist["score"] = dafentemp
            except Exception as err:

                #logger.error(err, exc_info=1)
                returnlist["score"] = -1
    return returnlist

if __name__ == '__main__':

    filepath = "../data/"
    files = listfiles(filepath, ".html")
    for i in files:
        print(i)
        temp = filepath + i
        with open(temp, "rb") as f:
            content = f.read().decode("utf-8", "ignore")
            print(pinfoparse(content))
    # os.remove("./sh.sh")
    shutil.rmtree("./dd")