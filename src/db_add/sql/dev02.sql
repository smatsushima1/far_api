

SELECT table_schema,table_name
FROM information_schema.tables
where table_schema = 'public'
ORDER BY table_schema,table_name;

drop table ;

select * from dev_tag_counts01 order by id_num;
select * from dev_tag_counts01 where reg like '%annex%' or reg like '%app%' order by id_num;

select * from dev_reg_links01;

select count(*) from dev_all_parts01;

select * from dev_add_html01 order by id_num;

select * from dev_all_parts01 where reg like '%dfar%';

select * from dev_all_parts02 limit 1;





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




--------------------------------------------------------------------------------
-- Things to look out for:
-- - nfs: literally no formatting except for paragraphs
--     - p class="p-Normal" and go to next siblings for each section
-- - vaar: h2's are actually h1's
--     - h3's are h2's
--     - strong are the main tags (why...)





