
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
order by id_num;
