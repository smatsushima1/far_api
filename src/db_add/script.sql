
-- First, find all the dupes
drop table if exists dev_dupes1;
create table dev_dupes1 as
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
         substring(part from '([0-9]+)')::numeric;
select * from dev_dupes1;


-- Inner join all values to include the hlinks
drop table if exists dev_dupes2;
create table dev_dupes2 as
select d0.part,
       d0.reg,
	   d0.hlink,
	   d0.order_num
from dev_all_parts d0
join dev_dupes1 d1 on d0.part = d1.part and
                      d0.reg = d1.reg and
					  d0.order_num = d1.order_num
order by d0.order_num,
         substring(d0.part from '([0-9]+)')::numeric;
select * from dev_dupes2;


-- Fix the dupes in the dlad regs
drop table if exists dev_dupes3;
create table dev_dupes3 as
select part,
       'dladpgi' as reg,
       hlink,
	   (order_num + .1) as order_num
from dev_dupes2
where reg = 'dlad' and
      (hlink like '%acquisitions%' or
	   hlink like '%-0')
order by order_num,
         substring(part from '([0-9]+)')::numeric;
select * from dev_dupes3;


-- Fix the dupes in the nmcars regs
drop table if exists dev_dupes4;
create table dev_dupes4 as
select part,
       'nmcarsannex' as reg,
       hlink,
	   (order_num + .1) as order_num
from dev_dupes2
where reg = 'nmcars' and
      hlink like '%annex%'
order by order_num,
         substring(part from '([0-9]+)')::numeric;
select * from dev_dupes4;


-- create new dev_all_parts table that has the updated values
drop table if exists dev_all_parts2;
create table dev_all_parts2
select 


















