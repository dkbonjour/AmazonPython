# !/usr/bin/python3.4
# -*-coding:utf-8-*-
# Created by Smartdo Co.,Ltd. on 2016/10/19.
# 功能:
#  导出一个URL的某一天数据
from config.config import *
from tool.jmysql.mysql import *
from tool.jfile.file import  *

def getdata(url, days):
    url = url.strip()
    config = getconfig()["basedb"]
    db = Mysql(config)
    sql = 'select id,`database`,url from smart_category where url like"' + url + '%"'
    dbname = db.ExecQuery(sql)
    dbvalid = []
    for i in dbname:
        if i[1] == None:
            continue
        else:
            dbvalid.append([i[0], i[1]])
    for j in dbvalid:
        try:
            realconfig = getconfig()[j[1]]
            realdb = Mysql(realconfig)
            # SELECT smallrank,name,bigname,rank,title,price,score,asin,url,
            # soldby,shipby,commentnum,commenttime,createtime FROM `3-1-1-2` where id like "20161018%" order by smallrank;
            realsql ='SELECT smallrank,name,bigname,rank,title,price,score,asin,url,' \
                     'soldby,shipby,commentnum,commenttime,createtime FROM `{tablename}` where id like "{days}%" ' \
                     'order by smallrank;'.format(tablename=j[0], days=days)
            result = realdb.ExecQuery(realsql)
            if result == None:
                continue
            else:
                return j[0],result
        except Exception as err:
            pass
    return None


def writefile(data,id,url):
    # print(data)
    temp=[]
    temp.append(["小类排名","小类名称","大类名称","大类排名","商品标题","商品价格","商品评分","ASIN","URL","Soldby","Shipby","评论数","较早评论时间","数据获取时间"])
    dir = getconfig()["datadir"]+"/export/"+todaystring(3)
    createjia(dir)
    filename=dir+"/"+id+".xlsx"
    for i in data:
        temp.append(list(i))
    temp.append([url])
    try:
        writeexcel(filename,temp)
    except Exception as err:
        return "写入Excel出错"
    return "保存在："+filename

if __name__ == "__main__":
    url = input("输入类目URL：")
    days = "20161018"
    try:
        id,data=getdata(url, days)
        if data==None:
            print("找不到数据")
        print(writefile(data,id,url))
    except Exception as err:
        print("出错")