# !/usr/bin/python3.4
# -*-coding:utf-8-*-
# Created by Smartdo Co.,Ltd. on 2016/10/17.
# 功能:
#  
import tool.log
import logging
from config.config import *
from tool.jmysql.mysql import *

# 日志
tool.log.setup_logging()
logger = logging.getLogger(__name__)


def createtable(config, database, tables):
    db2 = Mysql2(config)
    createdb = "CREATE DATABASE  IF NOT EXISTS `" + database + "`"
    try:
        db2.ExecNonQuery(createdb)
    except:
        print(database + "存在")
        pass
    db = Mysql(config)
    for table in tables:
        sql = '''
CREATE TABLE `{tablename}` (
  `id` VARCHAR(255),
  `purl` varchar(255) DEFAULT NULL COMMENT '父类类目链接',
  `col1` varchar(255) DEFAULT NULL COMMENT '预留字段',
  `col2` varchar(255) DEFAULT NULL,
  `col3` varchar(255) DEFAULT NULL,
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
    '''.format(tablename=table)
        try:
            db.ExecNonQuery(sql)
            print(database + ":" + table + "创建成功")
        except Exception as err:
            print(database + ":" + table + "创建失败")
            print(err)


def selecttable(config, dbname):
    returnlist = []
    db = Mysql(config)
    sql = 'select id from smart_category where `database` like "' + dbname + '"'
    temp = db.ExecQuery(sql)
    for i in temp:
        returnlist.append(i[0])
    return returnlist


if __name__ == "__main__":
    try:
        begin = int(input("从哪里开始："))
        end = int(input("从哪里结束："))
        end = end + 1
    except:
        print("错误，默认1-22")
        begin = 1
        end = 23
    for i in range(begin, end):
        db = str(i)
        allconfig = getconfig()
        try:
            baseconfig = allconfig["basedb"]
            tables = selecttable(baseconfig, db)
            db = "db" + db
            dbconfig = allconfig[db]
            database = allconfig[db]["db"]
            createtable(dbconfig, database, tables)
        except Exception as e:
            print(e)
            raise Exception("数据库配置出错")
