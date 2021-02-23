
select * from dev_psql_update;

select part,
       subpart
from dev_all_parts2
order by id_num
limit 10;


update dev_psql_update
set htext = 'ugh'
where id_num = 1;

 

