
-- First, find all the dupes
-- Leave out nmcars since those will come in dev_dupes04
drop table if exists dev_idnum01;
create table dev_idnum01 as
select part,
       reg,
	   order_num,
	   count(*) as cnt
from dev_all_parts01
where reg != 'nmcars'
group by part,
         reg,
		 order_num
    having count(*) > 1
order by order_num,
         substring(part from '([0-9]+)')::numeric;
-- select * from dev_idnum01;


-- Inner join all values to include the hlinks
drop table if exists dev_idnum02;
create table dev_idnum02 as
select t1.part,
       t1.reg,
	   t1.hlink,
	   t1.order_num
from dev_all_parts01 t1
join dev_idnum01 t2 on t1.part = t2.part and
                      t1.reg = t2.reg and
					  t1.order_num = t2.order_num
order by t1.order_num,
         substring(t1.part from '([0-9]+)')::numeric;
-- select * from dev_idnum02;


-- Fix the dupes in the dlad regs
drop table if exists dev_idnum03;
create table dev_idnum03 as
select 'dladpgi' as reg,
       hlink,
	   (order_num + .1) as order_num
from dev_idnum02
where reg = 'dlad' and
      (hlink like '%acquisitions%' or
	   hlink like '%-0')
order by order_num,
         substring(part from '([0-9]+)')::numeric;
-- select * from dev_idnum03;


-- Find all annexes in nmcars
drop table if exists dev_idnum04;
create table dev_idnum04 as
select 'nmcarsannex' as reg,
       hlink,
	   (order_num + .1) as order_num
from dev_all_parts01
where reg = 'nmcars' and
      hlink like '%annex%'
order by order_num,
         substring(part from '([0-9]+)')::numeric;
-- select * from dev_idnum04;


-- Update all appendixes with a new reg and order_num
drop table if exists dev_app01;
create table dev_app01 as
select part,
       reg || 'appendix' as reg,
       hlink,
       (order_num + .1) as order_num
from dev_all_parts01
where hlink like '%appendix%' or
      lower(part) in ('aa', 'bb', 'cc', 'dd', 'ee', 'ff', 'gg', 'hh') or
      lower(part) like ('app%');
--select * from dev_app01;

  
-- Add in row numbers relative to each order_num
drop table if exists dev_app02;
create table dev_app02 as
select part,
       reg,
       hlink,
       order_num,
       row_number() over(partition by order_num order by part) as row_num
from dev_app01
order by order_num;
--select * from dev_app02;


-- Modify the order_num yet again to make it sortable ascending later
-- Also keep the original order_num for joining purposes later
drop table if exists dev_app03;
create table dev_app03 as
select part,
       reg,
       hlink,
       order_num as order_num_orig,
       (order_num + (row_num::numeric/100)) as order_num
from dev_app02
order by order_num;
--select * from dev_app03;


-- Combine the changes in one table
drop table if exists dev_idnum05;
create table dev_idnum05 as
select *
from dev_idnum03
union
select *
from dev_idnum04
union
select reg,
       hlink,
       order_num
from dev_app03;
-- select * from dev_idnum05;


-- Create new dev_all_parts table that has the updated values
drop table if exists dev_idnum06;
create table dev_idnum06 as
select t1.part,
       t1.subpart,
       t1.sction,
       t1.subsction,
	   t1.paragraph,
	   (case when t2.reg is null then t1.reg
		else t2.reg end) as reg,
       t1.htype,
       (case when t2.hlink is null then t1.hlink
	 	else t2.hlink end) as hlink,
       t1.htext,
       (case when t2.order_num is null then t1.order_num
		else t2.order_num end) as order_num
from dev_all_parts01 t1
left join dev_idnum05 t2 on t1.hlink = t2.hlink;
-- select * from dev_idnum06;


-- Add in id numbers for each row
drop table if exists dev_idnum07;
create table dev_idnum07 as
select row_number() over(order by t1.order_num,
                                  substring(t1.part from '([0-9]+)')::numeric) as id_num,
       t1.*
from dev_idnum06 t1
order by t1.order_num,
         substring(t1.part from '([0-9]+)')::numeric;
-- select * from dev_idnum07;


-- Create new dev_all_parts table that has id numbers and sorted appropriately
drop table if exists dev_all_parts02;
create table dev_all_parts02 as
select t1.id_num,
       t1.part,
       t1.subpart,
       t1.sction,
       t1.subsction,
       t1.paragraph,
       t1.reg,
       t1.htype,
       t1.hlink,
       t1.htext,
       (case when t2.order_num is null then t1.order_num
        else t2.order_num_orig end) as order_num
from dev_idnum07 t1
left join dev_app03 t2 on t1.hlink = t2.hlink
order by t1.id_num;
--select * from dev_all_parts02;

-- Drop all tables when done
drop table if exists dev_idnum01,
                     dev_idnum02,
                     dev_idnum03,
                     dev_idnum04,
                     dev_idnum05,
                     dev_idnum06,
                     dev_idnum07,
                     dev_app01,
                     dev_app02,
                     dev_app03,
                     dev_all_parts01;

