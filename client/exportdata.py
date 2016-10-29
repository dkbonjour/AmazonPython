# !/usr/bin/python3.4
# -*-coding:utf-8-*-
# Created by Smartdo Co.,Ltd. on 2016/10/19.
# 功能:
#  导出一个URL的某一天数据
from config.config import *
from tool.jmysql.mysql import *
from tool.jfile.file import *


def getdata(url, days):
    url = url.strip().split("/ref")[0]
    config = getconfig()["basedb"]
    db = Mysql(config)
    sql = 'select id,`database`,url from smart_category where url like"' + url + '%"'
    dbname = db.ExecQuery(sql)
    dbvalid = []
    for i in dbname:
        if i[1] == None:
            continue
        else:
            dbvalid.append([i[0], getconfig()["dbprefix"] + i[1]])
    for j in dbvalid:
        try:
            realconfig = getconfig()[j[1]]
            realdb = Mysql(realconfig)
            # SELECT smallrank,name,bigname,rank,title,price,score,asin,url,
            # soldby,shipby,commentnum,commenttime,createtime FROM `3-1-1-2` where id like "20161018%" order by smallrank;
            realsql = 'SELECT smallrank,name,bigname,rank,title,price,score,asin,url,' \
                      'soldby,shipby,commentnum,commenttime,createtime FROM `{tablename}` where id like "{days}%" ' \
                      'order by smallrank;'.format(tablename=j[0], days=days)
            result = realdb.ExecQuery(realsql)
            # print(realsql)
            if result == None:
                continue
            else:
                if not result:
                    continue
                return j[0], result
        except Exception as err:
            print(err)
    return 0, None


def writefile(data, id, url):
    # print(data)
    temp = []
    temp.append(
            ["小类排名", "小类名称", "大类名称", "大类排名", "商品标题", "商品价格", "商品评分", "ASIN", "URL", "Soldby", "Shipby", "评论数", "较早评论时间",
             "数据获取时间"])
    dir = getconfig()["datadir"] + "/export/" + todaystring(3)
    createjia(dir)
    filename = dir + "/" + id + ".xlsx"
    for i in data:
        dataone = list(i)
        temp.append(dataone)
    temp.append([url])
    try:
        writeexcel(filename, temp)
    except Exception as err:
        return "写入Excel出错，请关闭该Excel文件后重试"
    return "数据保存在：" + filename


if __name__ == "__main__":
    while True:
        url = input("输入类目URL：")
        todays = todaystring(3)
        days = input("请输入日期(如" + todays + "):")

        try:
            id, data = getdata(url, days)
            if data == None:
                raise Exception("找不到数据")
            print(writefile(data, id, url))
        except Exception as err:
            print(err)
