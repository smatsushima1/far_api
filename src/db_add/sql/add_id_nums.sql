
-- First, find all the dupes
-- Leave out nmcars since those will come in dev_dupes04
drop table if exists dev_dupes01;
create table dev_dupes01 as
select part,
       reg,
	   order_num,
	   count(*) as cnt
from dev_all_parts
where reg != 'nmcars'
group by part,
         reg,
		 order_num
    having count(*) > 1
order by order_num,
         substring(part from '([0-9]+)')::numeric;
-- select * from dev_dupes01;


-- Inner join all values to include the hlinks
drop table if exists dev_dupes02;
create table dev_dupes02 as
select t1.part,
       t1.reg,
	   t1.hlink,
	   t1.order_num
from dev_all_parts t1
join dev_dupes01 t2 on t1.part = t2.part and
                      t1.reg = t2.reg and
					  t1.order_num = t2.order_num
order by t1.order_num,
         substring(t1.part from '([0-9]+)')::numeric;
-- select * from dev_dupes02;


-- Fix the dupes in the dlad regs
drop table if exists dev_dupes03;
create table dev_dupes03 as
select 'dladpgi' as reg,
       hlink,
	   (order_num + .1) as order_num
from dev_dupes02
where reg = 'dlad' and
      (hlink like '%acquisitions%' or
	   hlink like '%-0')
order by order_num,
         substring(part from '([0-9]+)')::numeric;
-- select * from dev_dupes03;


-- Find all annexes in nmcars
drop table if exists dev_dupes04;
create table dev_dupes04 as
select 'nmcarsannex' as reg,
       hlink,
	   (order_num + .1) as order_num
from dev_all_parts
where reg = 'nmcars' and
      hlink like '%annex%'
order by order_num,
         substring(part from '([0-9]+)')::numeric;
-- select * from dev_dupes04;


-- Update all appendixes
drop table if exists dev_app01;
create table dev_app01 as
select reg || 'appendix' as reg,
       hlink,
       (order_num + .1) as order_num
from dev_all_parts
where hlink like '%appendix%' or
      part in ('AA', 'BB', 'CC', 'DD', 'EE', 'FF', 'GG', 'HH');
-- select * from dev_app01;


-- Combine the changes in one table
drop table if exists dev_dupes05;
create table dev_dupes05 as
select *
from dev_dupes03
union
select *
from dev_dupes04
union
select *
from dev_app01;
-- select * from dev_dupes05;


-- Create new dev_all_parts table that has the updated values
drop table if exists dev_dupes06;
create table dev_dupes06 as
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
left join dev_dupes05 t2 on t1.hlink = t2.hlink;
-- select * from dev_dupes06;


-- Create last dupes table to sort everything
drop table if exists dev_dupes07;
create table dev_dupes07 as
select *
from dev_dupes06
order by order_num,
         substring(part from '([0-9]+)')::numeric;
-- select * from dev_dupes07;


-- Create new dev_all_parts table that has id numbers
drop table if exists dev_all_parts2;
create table dev_all_parts2 as
select row_number() over() as id_num,
       t1.*
from dev_dupes07 t1
order by t1.order_num,
         substring(t1.part from '([0-9]+)')::numeric;
-- select * from dev_all_parts2 order by id_num;


-- Drop all tables when done
--drop table if exists dev_dupes01;
--drop table if exists dev_dupes02;
--drop table if exists dev_dupes03;
--drop table if exists dev_dupes04;
--drop table if exists dev_dupes05;
--drop table if exists dev_dupes06;
--drop table if exists dev_dupes07;

