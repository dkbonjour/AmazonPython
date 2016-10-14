select * from smart_category where url like "https://www.amazon.com/Best-Sellers-Home-Kitchen-Bassinet-Beddin%"
union
select * from smart_category where id=1018
union
select * from smart_category where id=1037
union
select * from smart_category where id=101
union
select * from smart_category where id=103


select id,url,name,level,page,pid,bigpname,bigpid,ismall,isvalid from smart_category limit 20000 into outfile 'G:/amzonurl.csv' fields terminated by ',' optionally enclosed by '"' escaped by '"'
lines terminated by '\r\n';


SELECT id,url,name,level,page,pid,bigpid,bigpname FROM smart_base.smart_category where ismall=1 and isvalid=1;