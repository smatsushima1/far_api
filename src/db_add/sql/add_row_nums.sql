
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
-- select * from dev_dupes1;


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
-- select * from dev_dupes2;


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
-- select * from dev_dupes3;


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
-- select * from dev_dupes4;


-- Combine the changes in one table
drop table if exists dev_dupes5;
create table dev_dupes5 as
select *
from dev_dupes3
union
select *
from dev_dupes4;
-- select * from dev_dupes5;


-- Create new dev_all_parts table that has the updated values
drop table if exists dev_dupes6;
create table dev_dupes6 as
select t1.part,
       t1.subpart,
       t1.section,
       t1.subsection,
	   t1.paragraph,
	   (case when t2.reg is null then t1.reg
		    else t2.reg
		end) as reg,
       t1.htype,
       t1.fac,
       (case when t2.hlink is null then t1.hlink
		    else t2.hlink
		end) as hlink,
       t1.htext,
       (case when t2.order_num is null then t1.order_num
		    else t2.order_num
		end) as order_num,
       t1.import_date
from dev_all_parts t1
left join dev_dupes5 t2 on t1.hlink = t2.hlink;
-- select * from dev_dupes6;


-- Create last dupes table to sort everything
drop table if exists dev_dupes7;
create table dev_dupes7 as
select *
from dev_dupes6
order by order_num,
         substring(part from '([0-9]+)')::numeric;
-- select * from dev_dupes7;



-- Create new dev_all_parts table that has id numbers
drop table if exists dev_all_parts2;
create table dev_all_parts2 as
select t1.*,
       row_number() over() as id_num
from dev_dupes7 t1
order by t1.order_num,
         substring(t1.part from '([0-9]+)')::numeric;
-- select * from dev_all_parts2;


-- Drop all tables when done
drop table if exists dev_dupes1;
drop table if exists dev_dupes2;
drop table if exists dev_dupes3;
drop table if exists dev_dupes4;
drop table if exists dev_dupes5;
drop table if exists dev_dupes6;
drop table if exists dev_dupes7;

