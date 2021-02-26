
-- Add in all the html
drop table if exists dev_all_parts04;
create table dev_all_parts04 as
select t1.id_num,
       t1.rpart,
       t1.rsubpart,
       t1.rsection,
       t1.rsubsection,
       t1.rparagraph,
       t1.reg,
       t1.htype,
       t1.fac,
       t1.hlink,
       t2.htext,
       t1.order_num
from dev_all_parts03 t1
join dev_add_html01 t2 on t1.hlink = t2.hlink
order by id_num;
--select * from dev_all_parts04;

