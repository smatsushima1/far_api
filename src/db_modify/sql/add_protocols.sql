
-- Updated table that removes annexes, appendixes, Chapter 99, and reserved parts
drop table if exists dev_tag_counts02;
create table dev_tag_counts02 as
select *
from dev_tag_counts01
where reg not like '%annex%' and
      reg not like '%app%' and
      reg != 'chapter_99' and
      lower(part) not like '%reserved%' and
      part not like '%-%' and
      part not in ('20', '21', '40');
--select * from dev_tag_counts02;


-- Protocol 0: everything has articles and headers, with no bold or lists
drop table if exists dev_tag_prot0;
create table dev_tag_prot0 as
select t1.*,
       0 as protocol
from dev_tag_counts02 t1
where t1.article > 0 and
      reg in ('far',
              'dfars',
              'dfarspgi',
              'diar',
              'gsam',
              'epaar',
              'hsar',
              'hudar'
              );
--select * from dev_tag_prot0;


-- Main table to include everything but records in dev_tag_counts02
drop table if exists dev_tag_counts03;
create table dev_tag_counts03 as
select *
from dev_tag_counts02 t1
where id_num not in (select id_num
                     from dev_tag_prot0
                     );
--select * from dev_tag_counts04;


-- Protocol 1: no headers, bold and lists for paragraphs
drop table if exists dev_tag_prot1;
create table dev_tag_prot1 as
select t1.*,
       1 as protocol
from dev_tag_counts03 t1
where t1.reg in ('sofars',
                 'agar',
                 'aidar',
                 'car',
                 'dears',
                 'dolar',
                 'dosar',
                 'dtar',
                 'edar',
                 'fehbar',
                 'hhsar',
                 'iaar',
                 'jar',
                 'lifar',
                 'nrcar',
                 'tar'
                 );
-- select * from dev_tag_prot1;


-- Protocol 2: vaar specific, strong for everything and h2 = h1
drop table if exists dev_tag_prot2;
create table dev_tag_prot2 as
select t1.*,
       2 as protocol
from dev_tag_counts03 t1
where t1.reg = 'vaar';
-- select * from dev_tag_prot2;


-- Protocol 3: nfs, only p tags and literally nothing else
drop table if exists dev_tag_prot3;
create table dev_tag_prot3 as
select t1.*,
       3 as protocol
from dev_tag_counts03 t1
where t1.reg = 'nfs';
-- select * from dev_tag_prot3;


-- Protocol 4: contains headers, but no articles
drop table if exists dev_tag_prot4;
create table dev_tag_prot4 as
select t1.*,
       4 as protocol
from dev_tag_counts03 t1
where t1.reg not in (select reg
                     from dev_tag_prot1
                     union
                     select reg
                     from dev_tag_prot2
                     union
                     select reg
                     from dev_tag_prot3
                     );
-- select * from dev_tag_prot4;


-- Combine all tables to be joined
drop table if exists dev_all_prot01;
create table dev_all_prot01 as
select id_num, protocol from dev_tag_prot0
union
select id_num, protocol from dev_tag_prot1
union
select id_num, protocol from dev_tag_prot2
union
select id_num, protocol from dev_tag_prot3
union
select id_num, protocol from dev_tag_prot4
order by id_num;
--select * from dev_all_prot01;


-- Update the dev_all_parts table to mirror the used id_nums
drop table if exists dev_all_parts05;
create table dev_all_parts05 as
select t1.*,
       t2.protocol
from dev_all_parts04 t1
join dev_all_prot01 t2 on t1.id_num = t2.id_num;
--select * from dev_all_parts05


-- Lastly, include all the tags with their protocols
drop table if exists dev_tag_counts04;
create table dev_tag_counts04 as
select t1.*,
       t2.protocol as protocol
from dev_tag_counts02 t1
join dev_all_prot01 t2 on t1.id_num = t2.id_num;
-- select * from dev_all_counts04;


-- Unit test to see if counts are equal
--select count(*) from dev_tag_counts02;
--select count(t1.*) from (select id_num from dev_tag_prot0
--                         union
--                         select id_num from dev_tag_prot1
--                         union
--                         select id_num from dev_tag_prot2
--                         union
--                         select id_num from dev_tag_prot3
--                         union
--                         select id_num from dev_tag_prot4
--                         ) t1;

--select * from dev_tag_counts02;
--select * from dev_tag_prot0;
--select * from dev_tag_counts03;
--select * from dev_tag_prot1;
--select * from dev_tag_prot2;
--select * from dev_tag_prot3;
--select * from dev_tag_prot4;

