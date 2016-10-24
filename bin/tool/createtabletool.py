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
    except Exception as err:
        print(database + "存在")
        pass
    db = Mysql(config)
    for table in tables:
        sql = '''
CREATE TABLE `{tablename}` (
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
    '''.format(tablename=table)
        try:
            db.ExecNonQuery(sql)
            print(sql)
        except Exception as err:
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
    for i in range(2,23):
        db = str(i)
        allconfig = getconfig()
        try:
            baseconfig = allconfig["basedb"]
            tables = selecttable(baseconfig, db)
            print(tables)
            db = "db" + db
            dbconfig = allconfig[db]
            database = allconfig[db]["db"]
            createtable(dbconfig, database, tables)
        except:
            raise Exception("数据库配置出错")
