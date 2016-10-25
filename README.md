# An Amazon Crawler

## Source Framework
Develope by Python, Look at the following：

    spider (Crawler module)
        --- download  (Crawler Download Module)
        --- parse     (Crawler Parser Module)
        --- logic     (Crawler Logic Module)
    bin (Crawler Execution File)
        --- spider (Crawler Entrance)
        --- tool   (Auxiliary Tool)
    config (Config Module)
        --- base  (Config File)
        --- config.py
            config.json
            log.json
    tool (Basic Tool)
        --- jfile
        --- jhttp
        --- jjson
        --- jmysql
        --- log.py
    acion (Action Module，Such as proxy IP,Useragent...)
    test (Test Dir)
    data (Data Keep)
    log  (Log Keep)
    
    client (Export Data)
    
    doc (Help Doc)

## Third Party Library (to be installed)
```
pip3 install xlsxwriter
pip3 install pymysql
pip3 install requests
pip3 install bs4
pip3 install redis
yum install libxslt-devel
pip3 install lxml
pip3 install -U selenium
```

## Setting Environment Variables
```
set PYTHONPATH="G:/smartdo"  Window
export name="path"  Linux
```

## Using of the Basic Tool
Please look at the test dir for example

1.jjson (JSON Deal Package)

```
json字符串解析成对象
def stringToObject(jstring)

json字符串校验是否正确,可打印错误
def isRightJson(jstring, printerror=False)

对象解析成json字符串,支持排序和缩进
def objectToString(jobject, sort=False, indent=None)

格式化json字符串,默认按键排序
def formatStringToString(jstring, sort=True)

格式化json字符串,并可选择存入文件
def formatStrigToFile(filepath, sort=True, filesavepath="")
```

2.jhttp　(Network Package)

```
自己封装的抓取函数
getHtml(url, daili='', postdata={}, header={})

header:
   {'User-Agent'：'Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
   'Referer'：'http://s.m.taobao.com',
   'Host'：'h5.m.taobao.com'
  }
 
postdata:
    {"dd":"dd"}
    
数据URL转义
def urlencode(postdata={}):
    
```

3.jfile　(File Package)

```
找出文件夹下所有xml后缀的文件，可选择递归，选择全路径
def listfiles(rootdir, prefix='.xml', isall=False, iscur=False)

将数据写入Excel
def writeexcel(path, dealcontent=[])

去除标题中的非法字符 (Windows)
def validateTitle(title)

递归创建文件夹
def createjia(path)

今天日期的字符串
def todaystring(level=3)

获取文件类型，传入文件名
def filetype(filename)

文件路径拼接
def filejoin(file=[])

从文件中读取行，变成列表
def readfilelist(filepath)

时间函数
def timetochina(longtime, formats='{}天{}小时{}分钟{}秒')
    today=time.strftime('%Y%m%d', time.localtime())
    a=time.clock()
    b=time.clock()
    print('运行时间：'+timetochina(b-a))
    
判断文件是否存在
def fileexsit(path)

切分文件列表
def devidelist(files=[],num=0)

取得URL参数
def geturlattr(url)

拼接参数join
def joinany(things, sep=",")
```

4.jmysql (Database Package)

```
config = {"host": "localhost", "user": "root", "pwd": "6833066", "db": "doubanbook"}
mysql=Mysql(config)
mysql.ExecNonQuery("insert into `booktag` (bookname) values ('你哈') ")
mysql.ExecQuery('SELECT bookname,bookkind,bookno FROM booktag limit 0,10;')
```


```
Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Readability counts.
```

## Over the wall(In China)

```
C:\Windows\System32\drivers\etc put host
Windows: press Windows+R key，run cmd ，Run command at the command prompt: ipconfig /flushdns
```

## How to Use?
Doc!!!

# 亚马逊美国站爬虫软件使用

爬虫有两只，第一只是抓取类目，总共2万多个，保存在一个文件夹中，并需要使用辅助函数处理。

第二只是高级亚马逊排名爬虫，支持并行，容错，反爬虫等功能。

爬虫使用先需要更改配置文件，导入数据库，运行执行文件

## 修改配置文件 config/config.json和log.json   （#连同后面内容需去掉）

**1.全局配置**
```
{
  "company": "Smartdo Co.,Ltd", 
  "version": "v1",   
  "developer": "陶彦百，陈锦瀚",
  "time": "2016-11",
  "datadir":"G:",   # 重要数据保存位置，全路径
  "iperror":50,     # 代理IP的反爬最大数量（存于数据库，select后判断）
  "itemnum":90,     # 商品类目抓取的最大置信数，大于该数，不重抓
  "sleep":true,     # 爬虫下载是否睡眠1-3秒
  "koip":false,     # 遭遇机器人限制时是否剔除该IP并写数据库
  "localkeep":false, # 详情页是否保存本地（很大，建议关闭）
  "catchurl":["Appliances", "Arts_ Crafts & Sewing"], # 抓取的大类列表，select其下的子类
  "processnum":12, # 并行进程数（不是并发）
  "urlnum":200, # 类目数限制（建议20000，不限制）
  "basedb": {  # 代理IP和类目信息数据库位置
    "host": "192.168.0.152",
    "user": "bai",
    "pwd": "123456",
    "db": "smart_base"
  },
  "ratedb1": { # 类目抓取数据存储的数据库，类目信息database字段指明了该数据库
    "host": "192.168.0.152",
    "user": "bai",
    "pwd": "123456",
    "db": "smart_item1"
  },
  "ratedb2": { # 同上
    "host": "192.168.0.152",
    "user": "bai",
    "pwd": "123456",
    "db": "smart_base"
  }
}
```

**2.日志配置**

```
  "root": {
    "level": "ERROR", # 可改CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET 建议不改
    "handlers": [
      "console",
      "error_file_handler"
    ]
  }
```

日志将自动以时间20161018创建文件夹，进程号-日志名为文件名来存储，存储于log文件夹下

## 建立数据库

**1.基础数据库smart_base**

```
CREATE TABLE `smart_category` (
  `id` varchar(100) NOT NULL,
  `url` varchar(255) DEFAULT NULL COMMENT '类目链接',
  `name` varchar(255) DEFAULT NULL COMMENT '类目名字',
  `level` tinyint(4) DEFAULT NULL COMMENT '类目级别',
  `pid` varchar(100) DEFAULT NULL COMMENT '父类id',
  `createtime` datetime DEFAULT NULL COMMENT '创建时间',
  `updatetime` datetime DEFAULT NULL COMMENT '更新时间',
  `isvalid` tinyint(4) DEFAULT '0' COMMENT '是否有效',
  `page` tinyint(4) DEFAULT '5' COMMENT '抓取页数',
  `database` varchar(255) DEFAULT NULL COMMENT '存储数据库',
  `col1` varchar(255) DEFAULT NULL COMMENT '预留字段',
  `col2` varchar(255) DEFAULT NULL,
  `col3` varchar(255) DEFAULT NULL,
  `bigpname` varchar(255) DEFAULT NULL COMMENT '大类名字',
  `bigpid` varchar(100) DEFAULT NULL COMMENT '大类ID',
  `ismall` tinyint(4) DEFAULT '0' COMMENT '是否最小类',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='类目';
```

id为标志位，如1，1-1，1-1-1，表明是第一个分类下面的第一个分类下面的第一个分类。

爬虫原理是根据bigpname筛选出isvalid为1的类目，然后根据进程数平均分配，开始抓取，抓取之前判断database字段在配置文件
是否存在，存在的话判断该数据库是否存在这张表，表名为id，没有则报错退出。

```
CREATE TABLE `smart_ip` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip` varchar(45) NOT NULL,
  `createtime` datetime DEFAULT NULL COMMENT '添加时间',
  `updatetime` datetime DEFAULT NULL COMMENT '更新时间',
  `failtimes` int(11) DEFAULT '0' COMMENT '失效次数',
  `zone` varchar(200) DEFAULT NULL COMMENT '区域',
  `col1` varchar(200) DEFAULT NULL COMMENT '预留字段',
  `col2` varchar(200) DEFAULT NULL,
  `col3` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ip_UNIQUE` (`ip`)
) ENGINE=InnoDB AUTO_INCREMENT=9218 DEFAULT CHARSET=utf8 COMMENT='IP池';
```

代理IP数据表zone字段指明地理位置，如美国，failtimes指明失效次数，如果大于配置文件所需次数，抽取时被弃用。

**2.商品数据库smart_item1**

```
CREATE TABLE `smart_item1`.`1-1-1` (
  `id` VARCHAR(255),
  `smallrank` INT NULL COMMENT '小类排名',
  `name` VARCHAR(255) NULL COMMENT '小类名',
  `bigname` VARCHAR(255) NULL COMMENT '大类名',
  `title` TINYTEXT NULL COMMENT '商品标题',
  `asin` VARCHAR(255) NULL,
  `url` VARCHAR(255) NULL,
  `rank` INT NULL COMMENT '大类排名',
  `soldby` VARCHAR(255) NULL COMMENT '卖家',
  `shipby` VARCHAR(255) NULL COMMENT '物流',
  `price` FLOAT NULL COMMENT '价格',
  `score` FLOAT NULL COMMENT '打分',
  `commentnum` INT NULL COMMENT '评论数',
  `commenttime` VARCHAR(255) NULL COMMENT '第一条评论时间',
  `createtime` DATETIME NULL,
  PRIMARY KEY (`id`) )ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='类目表';
```

表名为类目id，id字段命名为20161018-1-B00NFDQL66   时间-小类排名-asin

类目数据要放在哪个数据库，需要手动建表（我写了python脚本），先在smart_category表将该类目isvalid置为1且database字段填入ratedb1，如下

```
"ratedb1": { # 类目抓取数据存储的数据库，类目信息database字段指明了该数据库
    "host": "192.168.0.152",
    "user": "bai",
    "pwd": "123456",
    "db": "smart_item1"
  }
```

然后配置文件真正的数据库是smart_item1，在该库建立1-1-1表（以此类推）


## 爬虫使用bin/spider
**1.urlspider排名类目爬虫**

因为是顺序型爬虫，且随着类目级别增多，爬的时间也变多，分了很多只，本应顺序爬取，但是每一级类目都是依靠上一级，所以可以同时开启

存储文件架构如下：

```
1. 首页抓下来，提取所有一级类目保存文件名 oneurl.md
2. 根据oneurl.md抓取二级类目，保存在2urls文件夹下，命名：
 
    2urls
        1-url.md    第一个一级类目下的二级类目们
        2-url.md    第二个一级类目下的二级类目们

3.扫描2urls文件夹，读取所有文件，按文件中二级链接分别抓取三级类目，保持在3urls，命名:

    3urls
        1-1-url.md  表示1-url.md文件下的第一条链接的三级类目们
        1-2-url.md  表示1-url.md文件下的第二条链接的三级类目们


以此类推

    4urls
        1-1-1-url.md 表示1-1-url.md文件下的第一条链接的四级类目们
        1-1-2-url.md 表示1-1-url.md文件下的第二条链接的四级类目们

    5urls
        1-1-1-1-url.md 表示1-1-1-url.md文件下的第一条链接的五级类目们
        1-1-1-2-url.md 表示1-1-1-url.md文件下的第二条链接的五级类目们
```

ausaspider.py抓取后存到oneurl.md,ausaspider1.py抓取后存到2urls

```
if __name__ == "__main__":
    a = time.clock()
    isdead = False
    while not isdead:
        try:
            ausalogic("1-2")
            isdead = True
        except Exception as err:
            logger.error(err, exc_info=1)
    b = time.clock()
    logger.error('运行时间：' + timetochina(b - a))
```

ausaspider2.py，ausaspider3.py类目过多，循环检测上一级新增的类目

```
if __name__ == "__main__":
    a = time.clock()
    isdead = False
    while not isdead:
        try:
            ausalogic("3-4")
            # isdead = True
        except Exception as err:
            logger.error(err, exc_info=1)
            pass
        time.sleep(3600)
        logger.error("一分钟后又跑一次")
    b = time.clock()
    logger.error('运行时间：' + timetochina(b - a))

```

最后一级太多了，使用了并行fastspider.py，可根据源代码将其他级别也设置为并行

```
if __name__ == "__main__":
    fastlevel5(num=25)
```

**2.ratespider排名爬虫**

```
if __name__ == "__main__":
    print(copyright("亚马逊大霸王开爬"))
    a = time.clock()
    # 大类名
    try:
        category = getconfig()["catchurl"]
    except:
        category = ["Appliances", "Arts_ Crafts & Sewing"]

    # 并行数量
    try:
        processnum = getconfig()["processnum"]
    except:
        processnum = 10

    # 类目抓取数量
    try:
        limit = getconfig()["urlnum"]
    except:
        limit = 60
    # 开抓，ko
    ratelogic(category, processnum, limit)

    b = time.clock()

    logger.error('运行时间：' + timetochina(b - a))

```


读取配置开始爬取主要数据！！！


## 辅助工具使用bin/tool
**1.proxyfiletool.py处理代理IP地理位置**

```
if __name__ == "__main__":
    savetofile(filepath="config/base/IPtemp.txt", savepath="config/base/IP.txt")
```

先往config/base/IPtemp.txt按行填入代理IP，如

```
146.148.157.225:808
146.148.157.224:808
```

执行后会在config/base/IP.txt，发现

```
146.148.157.225:808-美国加利福尼亚州洛杉矶
146.148.157.224:808-美国加利福尼亚州洛杉矶 
```

可手动在IP.txt填入。

**2.proxymysqltool.py将代理IP存入数据库(目前IP抽取都在数据库，也可从文件抽取）**

```
if __name__ == "__main__":
    allconfig = getconfig()
    try:
        config = allconfig["basedb"]
        # config = {"host": "localhost", "user": "root", "pwd": "6833066", "db": "smart_base"}
        savetomysql(filepath="config/base/IP.txt",config=config)
    except:
        raise Exception("数据库配置未填")
```

将config/base/IP.txt中的代理IP存到数据库

**3.createtabletool.py数据库建表**

```
if __name__ == "__main__":
    db = "ratedb1"
    allconfig = getconfig()
    try:
        baseconfig = allconfig["basedb"]
        tables = selecttable(baseconfig, db)
        print(tables)
        dbconfig = allconfig[db]
        createtable(dbconfig, tables)
    except:
        raise Exception("数据库配置出错")
```

select类目数据库中字段database为ratedb1的记录，查找配置文件：

```
  "ratedb1": { # 类目抓取数据存储的数据库，类目信息database字段指明了该数据库
    "host": "192.168.0.152",
    "user": "bai",
    "pwd": "123456",
    "db": "smart_item1"
  }
```

按类目数据库字段id命名数据库表，如1-1-1-1

**4.urlspidertool.py将抓取的类目URL汇总保存在config/base/URL.txt并存入类目数据库**

```
if __name__ == "__main__":
    # 处理URL
    dealurlfile()

    # 保存入数据库
    # config = {"host": "localhost", "user": "root", "pwd": "6833066", "db": "smart_base"}
    allconfig = getconfig()
    try:
        config = allconfig["basedb"]
        keeptomysql(config=config)
    except:
        raise Exception("数据库配置出错")
```

```
URL.txt内容
1-10-2,Washers,https://www.amazon.com/Best-Sellers-Appliances-Clothes-Washing-Machines/zgbs/appliances/13397491/ref=zg_bs_nav_la_2_2383576011,1-10,3,1,Appliances,1
1-10-3,All-in-One Combination Washers & Dryers,https://www.amazon.com/Best-Sellers-Appliances-Combination-Washers-Dryers/zgbs/appliances/13755271/ref=zg_bs_nav_la_2_2383576011,1-10,3,1,Appliances,1
1-10-4,Stacked Washer & Dryer Units,https://www.amazon.com/Best-Sellers-Appliances-Stacked-Washer-Dryer-Units/zgbs/appliances/2399957011/ref=zg_bs_nav_la_2_2383576011,1-10,3,1,Appliances,1
```

```
按上面列表插数据库
        sql = 'insert into smart_category (`id`,`url`,`name`,`level`,`pid`,`createtime`,`bigpname`,`bigpid`,`ismall`) values("{id}","{url}","{name}",{level},"{pid}",CURRENT_TIMESTAMP,"{bigpname}","{bigpid}",{ismall}) on duplicate key update updatetime = CURRENT_TIMESTAMP'
        insertsql = sql.format(id=sqlzone[0], url=sqlzone[2], name=sqlzone[1], level=sqlzone[4], pid=sqlzone[3],
                               bigpname=sqlzone[6], bigpid=sqlzone[5], ismall=sqlzone[7])
```

**5.validurlspidertool.py将config/base/ValidURL.txt的类目链接所在记录在类目数据库做有效标记，并加上存储数据库，示意该类目抓取并存到哪里**


```
if __name__ == "__main__":
    allconfig = getconfig()
    try:
        config = allconfig["basedb"]
        validurlchangemysql(config=config,dbname="ratedb1")
    except:
        raise Exception("数据库配置出错")
```

```
ValidURL.txt内容
https://www.amazon.com/Best-Sellers-Arts-Crafts-Sewing-Jewelry-Making-Bead-Looms/zgbs/arts-crafts/12896091/ref=zg_bs_nav_ac_3_8090707011
```

上面类目将抓取并存在ratedb1数据库中，需要查config.json找到真正数据库。


## 客户端工具client/exportdata.py

```
if __name__ == "__main__":
    url = input("输入类目URL：")
    days = input("请输入日期(如20161018):")
    try:
        id,data=getdata(url, days)
        if data==None:
            print("找不到数据")
        print(writefile(data,id,url))
    except Exception as err:
        print("出错")
```

输入类目和时间即可导出Excel数据，所有数据保存在配置文件config.json datadir指定的位置


## 外部文件数据存储架构

datadir = "G:"

将保存在C盘，且

```
detail （商品详情数据）
   ---2015 (年份)
   ---2016
        ---Arts_ Crafts & Sewing (大类名）
            ---20161017 （日期）
            ---20161018
                ---3-1-1-1 （小类ID，小类名太长）
                ---3-1-1-2
                    ---1-B00J5QM832.html （具体网页，可选择不保存，存在该文件不存在md文件，解析该文件）
                    ---1-B00J5QM832.md    （存入数据库之后的json字符串，见后文,如果存在该文件跳过）
                    ---2-B03J5QM832.html （命名：小类排名-Asin)
items   （商品列表数据）
   ---2015 (年份)
   ---2016
        ---Arts_ Crafts & Sewing (大类名）
            ---20161017 （日期）
            ---20161018
                ---3-1-1-1 （小类ID，小类名太长）
                ---3-1-1-2
                    ---1.md(第几页列表页）
                    ---2.md（数据见下文）
                    ---5.md
rateurl (类目链接数据）
export （导出的EXCEL文件）
    ---20161018
        --- 20161019-170256.xlsx

```


详情页json 1-B00J5QM832.md
```
{
    "asin": "B007QNFP40",
    "bigname": "Arts_ Crafts & Sewing",
    "commentnum": 166,
    "commenttime": "",
    "id": "20161019-1-B007QNFP40",
    "name": "Beading Kits",
    "price": 12.59,
    "rank": 835,
    "score": 4.4,
    "shipby": "FBA",
    "smallrank": 1,
    "soldby": "Amazon.com",
    "tablename": "3-1-1-3",
    "title": "Beadery Bead Extravaganza Bead Box Kit- 19.75-Ounce- Pearl",
    "url": "https://www.amazon.com/dp/B007QNFP40"
}
```

列表页数据 1.md
```
41,B00NCV0C8E,New Design Antique Bronze Plated Blan...
42,B01BLVH54U,Disney Princess Melty Beads (1000 Beads)
43,B019MYI268,Ship From US Silicone Bracelets Exped...
44,B005E0CEI2,Bead Mats 2/Pkg-7.75"X7.75"
45,B000RB3EWS,2 Diamond Gemstone Sorting Tray Pearl...
46,B0026HT68M,Beadalon Bead Mats 3/Pkg 9-Inch by...
47,B000I6H4VE,Darice Large 3-Channel Flocked Bead B...
48,B01HF4AFTO,Neon Silicone bracelet Bangles Perfec...

```


# Qestion


协同作战
```
git branch -r -d origin/branch-name
git push origin :branch-name
```

命令等
```
yum install nethogs -y
killall -9 python3
```

浏览器
```
https://selenium-python.readthedocs.io/
https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
```

VPN
```
http://www.wanghailin.cn/centos-7-vpn/
```