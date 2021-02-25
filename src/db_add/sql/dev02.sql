
select * from dev_psql_update;

select part,
       subpart
from dev_all_parts2
order by id_num
limit 10;


update dev_psql_update
set htext = 'ugh'
where id_num = 1;

select *
from dev_all_parts2
where id_num = 278;

select *
from dev_header_counts
where h1 > 0 and
      h2 > 0 and
      h3 > 0 and
      h4 > 0 and 
      bld > 0
order by id_num;


select *
from dev_header_counts
where h1 = 0 and
      bld > 0
order by id_num;


select *
from dev_header_counts
where h1 > 1
order by id_num;

select *
from dev_all_parts2
where htext = 'None'
order by id_num;


select *
from dev_header_counts
where strong > 1
order by id_num;


select * from dev_all_parts where reg = 'nmcars';
select * from dev_dupes1;
select * from dev_dupes2;
select * from dev_dupes4;
select * from dev_dupes5;
select * from dev_dupes6 where reg like 'nmcars%';

select * from dev_all_parts2 where hlink like '%annex%';

--------------------------------------------------------------------------------
-- Things to look out for:
-- - nfs: literally no formatting except for paragraphs
--     - p class="p-Normal" and go to next siblings for each section
-- - vaar: h2's are actually h1's
--     - h3's are h2's
--     - strong are the main tags (why...)





