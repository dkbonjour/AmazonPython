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