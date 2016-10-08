# -*-coding:utf-8-*-
# Created by 一只尼玛 on 2016/10/8.
# 功能:
#
from tool.jmysql.mysql import *


def init():
    return Mysql(host="localhost", user="root", pwd="6833066", db="doubanbook")


def initdoubanbook():
    mysql = pymysql.connect(host="localhost", user="root", passwd="6833066", charset="utf8")
    cur = mysql.cursor()
    createsql = """
CREATE SCHEMA `doubanbook` ;
use `doubanbook`;
CREATE TABLE `book` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `bookname` varchar(100) NOT NULL COMMENT '书名',
  `bookurl` varchar(150) NOT NULL COMMENT '书入口',
  `bookimg` varchar(150) DEFAULT NULL COMMENT '书图片',
  `bookinfo` varchar(250) DEFAULT NULL COMMENT '书出版信息',
  `bookstar` varchar(45) DEFAULT NULL COMMENT '书评价星数',
  `bookno` varchar(45) NOT NULL COMMENT '书编号',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='书表';
CREATE TABLE `booktag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bookname` varchar(100) DEFAULT NULL COMMENT '书名',
  `bookno` varchar(45) DEFAULT NULL COMMENT '书编号',
  `booktag` varchar(45) DEFAULT NULL COMMENT '书标签',
  `bookkind` varchar(45) DEFAULT NULL COMMENT '书分类',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='书标签';
CREATE TABLE `bookdetial` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bookname` varchar(100) DEFAULT NULL COMMENT '书名',
  `bookno` varchar(45) DEFAULT NULL COMMENT '书编号',
  `bookinfo` text COMMENT '书出版信息',
  `bookintro` text COMMENT '书介绍',
  `authorintro` text COMMENT '作者介绍',
  `peoples` int(11) DEFAULT NULL COMMENT '评价人数',
  `starts` varchar(100) DEFAULT NULL COMMENT '星级情况',
  `other` text COMMENT '其他信息',
  `mulu` mediumtext COMMENT '图书目录',
  `comments` mediumtext COMMENT '评论人',
  PRIMARY KEY (`id`),
  UNIQUE KEY `bookno_UNIQUE` (`bookno`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COMMENT='图书详情表';"""
    try:
        cur.execute(createsql)
        mysql.commit()
        return createsql
    except:
        mysql.rollback()
        print("执行失败，请先删除已存在的数据库和数据库表")


def testinsert():
    mysql1 = init()
    mysql1.ExecNonQuery("insert into `booktag` (bookname) values ('你哈') ")


def testselect():
    mysql1 = init()
    print('第一条记录一个值：'+mysql1.ExecQuery('SELECT bookname,bookkind,bookno FROM booktag group by bookno limit 0,5;')[0][0])
    print(mysql1.ExecQuery('SELECT bookname,bookkind,bookno FROM booktag limit 0,5;'))
    print('-' * 50)
    print(mysql1.ExecQuery('SELECT bookname,bookkind,bookno FROM booktag limit 0,10;'))


if __name__ == '__main__':
    # initdoubanbook()
    testinsert()
    testselect()
