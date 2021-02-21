
-- drop table if exists dev_dupes;
-- create table dev_dupes as
select part,
       reg,
	   order_num,
	   count(*) as cnt
from dev_all_parts
group by part,
         reg,
		 order_num
    having count(*) > 1
order by order_num,
         part;


