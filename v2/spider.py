# -*-coding:utf-8-*-
# Created by 一只尼玛 on 16-8-26.
# 功能:
# 　抓取网页

from tool.jhttp.spider import *

# 时间函数
def timetochina(longtime, formats='{}天{}小时{}分钟{}秒'):
    day = 0
    hour = 0
    minutue = 0
    second = 0
    try:
        if longtime > 60:
            second = longtime % 60
            minutue = longtime // 60
        else:
            second = longtime
        if minutue > 60:
            hour = minutue // 60
            minutue = minutue % 60
        if hour > 24:
            day = hour // 24
            hour = hour % 24
        return formats.format(day, hour, minutue, second)
    except:
        raise Exception('时间非法')



def alone(url, proxies):
    header = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
        # "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Accept-Language": "en-US;q=0.8,en;q=0.5",
        "Upgrade-Insecure-Requests": "1",
        # 'Referer': 'https://www.amazon.com/',
        'Host': 'www.amazon.com'
    }
    return spider(url=url, proxies=proxies, headers=header)



if __name__ == "__main__":
    a = time.clock()
    url = "https://www.amazon.com"
    ip = "146.148.179.174:808"
    proxies = {"http": "http://smart:smart2016@" + ip}
    err = 0
    success = 0
    robot = 0
    for i in range(1):
        try:
            data = alone(url, proxies)
            # with open("./file/"+daili.split(":")[0]+".html","wb") as f:
            #     f.write(data)
            success = success + 1
            print(data.decode("utf-8","ignore"))
            if "Robot Check" in data.decode("utf-8", "ignore"):
                robot = robot + 1
        except Exception as e:
            print(e)
            err = err + 1
        print(i,success,err,robot)
    b = time.clock()
    today = time.strftime('%Y%m%d', time.localtime())

    print('运行时间：' + timetochina(b - a))
