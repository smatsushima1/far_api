
-- Remove annex, appendix, and chapter_99
drop table if exists dev_tag_counts02;
create table dev_tag_counts02 as
select *
from dev_tag_counts01
where reg like '%annex%' or
      reg like '%app%' or
      reg = 'chapter_99' or
      lower(part) = 'reserved' or
      part like '%-%'
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


Protocol list:
0-series = containes articles and proper h1 headings
1-series = no articles


-- Main table to include everything but records in dev_tag_counts02
drop table if exists dev_tag_counts04;
create table dev_tag_counts04 as
select t1.*,
       0 as protocol
from dev_tag_counts03 t1
where article > 0
order by id_num;
--select * from dev_tag_counts04 order by id_num;


-- Main table to include everything but records in dev_tag_counts02
drop table if exists dev_tag_counts05;
create table dev_tag_counts05 as
select *
from dev_tag_counts03 t1
where id_num not in (
    select id_num
    from dev_tag_counts04
    )
order by id_num;
select * from dev_tag_counts05 order by id_num;

