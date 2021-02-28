
-- Add in all the html
drop table if exists dev_all_parts04;
create table dev_all_parts04 as
select t1.id_num,
       t1.reg,
       t1.part,
       t1.subpart,
       t1.sction,
       t1.subsction,
       t1.paragraph,
       t1.htype,
       t1.hlink,
       t2.htext,
       t1.order_num
from dev_all_parts03 t1
join all_html01 t2 on t1.hlink = t2.hlink;
--select * from dev_all_parts04;
--drop table if exists dev_all_parts03;


