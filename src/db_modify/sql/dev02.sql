
-- Check for all tables
select table_schema,table_name
from information_schema.tables
where table_schema = 'public'
order by table_schema,table_name;

drop table if exists dev_add_html01,
                     dev_all_parts04,
                     dev_all_parts05,
                     dev_all_prot01,
                     dev_reg_links01,
                     dev_tag_counts01,
                     dev_tag_counts02,
                     dev_tag_counts03,
                     dev_tag_counts04,
                     dev_tag_prot0,
                     dev_tag_prot1,
                     dev_tag_prot2,
                     dev_tag_prot3,
                     dev_tag_prot4;
           

-- View all
select * from dev_all_parts01;
select * from dev_reg_links01;
select * from dev_add_html01 order by id_num;
select * from dev_all_parts04 order by id_num;
select * from dev_tag_counts01 order by id_num;


--------------------------------------------------------------------------------
-- Things to look out for:
-- - check to see if all articles are section separators
-- - nfs: literally no formatting except for paragraphs
--     - p class="p-Normal" and go to next siblings for each section
-- - vaar: h2's are actually h1's
--     - h3's are h2's
--     - strong are the main tags (why...)


select * from dev_tag_prot0;


select *
from dev_all_parts04;
where part = '20';

select reg from dev_tag_counts03 group by reg;
select *
from dev_tag_counts01
where reg = 'far'
order by id_num;
-- 20, 21, 40

select *
from dev_tag_counts01
where part in ('20', '21', '40')
order by id_num;


select *
from dev_tag_counts01
where article > 0
order by id_num;

--far
--chapter_99
--dfars
--dfarsappendix
--dfarspgi
--diar
--epaar
--gsam
--hsar
--hudar




drop table dev_dupes07;


select * from dev_tag_counts01 order by id_num;
select * from dev_reg_links01;

select count(*) from dev_all_parts01;

select * from dev_add_html01 order by id_num;

select * from dev_all_parts01 where reg like '%dfar%';

select
select * from dev_all_parts04 where reg = 'affarsmp';





select *
from dev_header_counts
where h1 > 0 and
      h2 > 0 and
      h3 > 0 and
      h4 > 0 and 
      bld > 0
order by id_num;


select *
from dev_tag_counts
where h1 = 0
order by id_num;


select *
from dev_tag_counts01
order by id_num;




select *
from dev_all_parts03
order by id_num;
where length(part) > 2
order by part;









