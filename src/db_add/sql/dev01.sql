
select *
from dev_all_parts_headers
where reg = 'dfars'
order by substring(part from '([0-9]+)')::numeric;


select *
from dev_all_parts2
where htext = 'None'
order by substring(part from '([0-9]+)')::numeric;


drop table if exists dev_psql_update;
create table dev_psql_update as
select *
from dev_all_parts2
order by id_num
limit 10;

