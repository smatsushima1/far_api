
-- Remove annex, appendix, and chapter_99
drop table if exists dev_tag_counts02;
create table dev_tag_counts02 as
select *
from dev_tag_counts01
where reg like '%annex%' or
      reg like '%app%' or
      reg = 'chapter_99' or
      lower(part) = 'reserved' or
      part like '%-%' or
      part in ('20', '21', '40')
order by id_num;
--select * from dev_tag_counts02 order by id_num;

 
-- Main table to include everything but records in dev_tag_counts02
drop table if exists dev_tag_counts03;
create table dev_tag_counts03 as
select *
from dev_tag_counts01
where id_num not in (
    select id_num
    from dev_tag_counts02
    )
order by id_num;
--select * from dev_tag_counts03 order by id_num;


-- Protocol 0: everything has articles and headers, with no bold or lists
drop table if exists dev_tag_prot0;
create table dev_tag_prot0 as
select t1.*,
       0 as protocol
from dev_tag_counts03 t1
where article > 0
order by id_num;
--select * from dev_tag_prot0 order by id_num;


-- Main table to include everything but records in dev_tag_counts02
drop table if exists dev_tag_counts04;
create table dev_tag_counts04 as
select *
from dev_tag_counts03 t1
where id_num not in (
    select id_num
    from dev_tag_prot0
    )
order by id_num;
--select * from dev_tag_counts04 order by id_num;


-- Protocol 1: no headers, bold and lists for paragraphs
drop table if exists dev_tag_prot1;
create table dev_tag_prot1 as
select *
from dev_tag_counts04
where reg in ('sofars',
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
              )
order by id_num;
-- select * from dev_tag_prot1 order by id_num;


-- Protocol 2: vaar specific, strong for everything and h2 = h1
drop table if exists dev_tag_prot2;
create table dev_tag_prot2 as
select *
from dev_tag_counts04
where reg = 'vaar'
order by id_num;
-- select * from dev_tag_prot2 order by id_num;


-- Protocol 3: nfs, only p tags and literally nothing else
drop table if exists dev_tag_prot3;
create table dev_tag_prot3 as
select *
from dev_tag_counts04
where reg = 'nfs'
order by id_num;
-- select * from dev_tag_prot3 order by id_num;


-- Protocol 4: pull all the other regs not in the previous protocols
drop table if exists dev_tag_prot4;
create table dev_tag_prot4 as
select *
from dev_tag_counts04
where reg not in (
      select reg
      from dev_tag_prot1
      union
      select reg
      from dev_tag_prot2
      union
      select reg
      from dev_tag_prot3
      )
order by id_num;
-- select * from dev_tag_prot4 order by id_num;











