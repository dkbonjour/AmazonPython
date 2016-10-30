# -*-coding:utf-8-*-
# Created by 一只尼玛 on 16-8-26.
# 功能:
# 　抓取网页
#

from tool.jhttp.spider import *
from spider.parse.phonedetail import *
from tool.jfile.file import *
import tool

if __name__ == "__main__":
    createjia(tool.log.BASE_DIR + "/data/phonelist/")
    passua = []
    uas = readfilelist(tool.log.BASE_DIR + "/config/base/UA.txt")
    i = 0
    for ua in uas:
        ua = ua.strip().replace("\r", "")
        header = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            'User-Agent': ua,
            # "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Accept-Language": "en-US;q=0.8,en;q=0.5",
            "Upgrade-Insecure-Requests": "1",
            # 'Referer': 'https://www.amazon.com/',
            'Host': 'www.amazon.com'
        }
        # ip="http://smart:smart2016@146.148.149.209:808"
        # ip = "http://36.42.32.32:8080"
        # proxies = {"http": ip}
        url = "https://www.amazon.com/Best-Sellers-Automotive-Replacement-Transmission-Seals-Rings/zgbs/automotive/15724751"
        # data=requests.get(url=url, headers=header, proxies=proxies, timeout=60)
        # print(data.text)
        try:
            mulspider(url="https://www.amazon.com", headers=header, ua=str(i), timeout=5)
            resdata = mulspider(url=url, headers=header, ua=str(i), timeout=5)
        except Exception as e:
            print(e)
            continue
        print("开始:" + str(i) + ":" + ua)
        try:
            with open(tool.log.BASE_DIR + "/data/phonelist/" + str(i) + ".html","wb") as f:
                f.write(resdata)
            data=phonelistparse(resdata.decode("utf-8", "ignore"))
            print(data)
            if data:
                passua.append(ua)
        except Exception as e:
            print(e)
            print(ua)
        i = i + 1
    for j in passua:
        print(j)
