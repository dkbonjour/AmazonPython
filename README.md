# 爬虫代码

## 源码架构
使用Python开发，文件架构：

    spider 爬虫模块
         ---download 爬虫下载器
         ---parse 爬虫解析器
         ---logic 爬虫逻辑器
    bin 爬虫执行文件
    config 配置文件模块
    tool 基础函数工具箱模块
    acion 业务模块，如代理IP,Ua池等杂项
    test 测试文件夹
    data 数据保存地
    log 日志地

## 第三方库
```
pip3 install xlsxwriter
pip3 install pymysql
pip3 install requests
pip3 install bs4
```

## 设置环境变量
```
set PYTHONPATH="G:/smartdo"  Window
export 变量="路径"  Linux
```

## 工具箱用法
请查看test文件夹用法

1.jjson json处理库的封装

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

2.jhttp　网络包

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

3.jfile　文件包

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
```

4.jmysql 数据库包

```
config = {"host": "localhost", "user": "root", "pwd": "6833066", "db": "doubanbook"}
mysql=Mysql(config)
mysql.ExecNonQuery("insert into `booktag` (bookname) values ('你哈') ")
mysql.ExecQuery('SELECT bookname,bookkind,bookno FROM booktag limit 0,10;')
```


```
Beautiful is better than ugly.(美丽优于丑陋)
Explicit is better than implicit.(直白优于含蓄)
Simple is better than complex.(简单优于复杂)
Complex is better than complicated.(复杂优于繁琐)
Readability counts.(可读性很重要)
```

## 翻墙必备

```
C:\Windows\System32\drivers\etc 放host
Windows: 按下 Windows+R 键，运行 cmd ，在命令提示符运行命令 ipconfig /flushdns
```