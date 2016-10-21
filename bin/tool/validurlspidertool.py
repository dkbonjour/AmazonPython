# !/usr/bin/python3.4
# -*-coding:utf-8-*-
# Created by Smartdo Co.,Ltd. on 2016/10/15.
# 功能:
#   导入需要抓取的类目
#  
import tool.log
import logging
from tool.jfile.file import *
from tool.jmysql.mysql import *
from config.config import *

# 日志
tool.log.setup_logging()
logger = logging.getLogger(__name__)


def validurlchangemysql(config, dbname, textname):
    # update smart_base.smart_category set isvalid=1 where url like"https://www.amazon.com/Best-Sellers-Arts-Crafts-Sewing-Braid-Trim/zgbs/arts-crafts/2933776011/ref=zg_bs_nav_ac_4_12899421" limit 1;
    validurl = readfilelist(tool.log.BASE_DIR + "/config/base/" + textname)
    mysql = Mysql(config)
    for url in validurl:
        sql = 'update smart_category set isvalid=1 ,`database`="' + dbname + '" where url like "' + url.split("/ref")[
            0] + '%" limit 1';
        try:
            mysql.ExecNonQuery(sql)
            logger.warning("执行sql语句成功:" + sql)
        except Exception as err:
            logging.error(err, exc_info=1)
            logger.error(sql)


if __name__ == "__main__":
    allconfig = getconfig()
    try:
        textname = input("请输入URL所在的文件名（如ValidURL.txt)：")
        dbname = input("请输入数据库配置名：")
        config = allconfig["basedb"]
        validurlchangemysql(config=config, dbname=dbname, textname=textname)
    except:
        raise Exception("数据库配置出错")
