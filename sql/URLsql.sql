select * from smart_category where url like "https://www.amazon.com/Best-Sellers-Home-Kitchen-Bassinet-Beddin%"
union
select * from smart_category where id=1018
union
select * from smart_category where id=1037
union
select * from smart_category where id=101
union
select * from smart_category where id=103


select id,url,name,level,pid,bigpname,bigpid,ismall from smart_category limit 20000 into outfile 'G:/amzonurl.csv' fields terminated by ',' optionally enclosed by '"' escaped by '"'
lines terminated by '\r\n';