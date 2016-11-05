# -*-coding:utf-8-*-
# Created by 一只尼玛 on 16-8-26.
# 功能:
# 　测试UA找到页面是手机还是pc
#

from tool.jhttp.spider import *
from spider.parse.phonedetail import *
from tool.jfile.file import *
import tool
import shutil

if __name__ == "__main__":
    cookiepath = tool.log.BASE_DIR + "/data/cookie"
    try:
        shutil.rmtree(cookiepath)
    except:
        pass
    createjia(cookiepath)
    createjia(tool.log.BASE_DIR + "/data/phonelist/")
    passua = {}
    uas = readfilelist(tool.log.BASE_DIR + "/config/base/UA.txt")
    i = 0
    print(uas)
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
            print("准备:" + ua)
            resdata = mulspider(url=url, headers=header, ua=str(i), path=cookiepath, timeout=20)
        except Exception as e:
            print(e)
            continue
        print("开始:" + str(i) + ":" + ua)
        try:
            with open(tool.log.BASE_DIR + "/data/phonelist/" + str(i) + ".html", "wb") as f:
                f.write(resdata)
            data, isphone = phonelistparse(resdata.decode("utf-8", "ignore"))
            print("是手机端吗:" + str(isphone) + ":" + ua)
            # print(data)
            if data:
                print(data)
                passua[ua] = 1
            else:
                raise Exception("没数据")
        except Exception as e:
            print("错误")
            print(e)
            print(ua)
        print('*'*10)
        i = i + 1
    for j in passua:
        print(j)
