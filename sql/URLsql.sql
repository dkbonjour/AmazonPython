select * from smart_category where url like "https://www.amazon.com/Best-Sellers-Home-Kitchen-Bassinet-Beddin%"
union
select * from smart_category where id=1018
union
select * from smart_category where id=1037
union
select * from smart_category where id=101
union
select * from smart_category where id=103

# 导出
select CONCAT("'",id),url,name,level,page,CONCAT("'",pid),bigpname,bigpid,ismall,isvalid from smart_category limit 40000 into outfile 'G:/amzonurl.csv' fields terminated by ',' optionally enclosed by '"' escaped by '"'
lines terminated by '\r\n';

# 抓取的类目
SELECT id,url,name,level,page,pid,bigpid,bigpname FROM smart_base.smart_category where isvalid=1 and bigpname="Appliances";

SELECT id,url,name,page,bigpname FROM smart_category where isvalid=1 and (bigpname="Appliances" or bigpname="Industrial & Scientific")


# 重复的类目
select count(*) from (SELECT url,`database`,count(*) as j FROM smart_category group by url) as a where j>=2