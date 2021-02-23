
select *
from dev_all_parts_headers
where reg = 'dfars'
order by substring(part from '([0-9]+)')::numeric;


select *
from dev_all_parts2
where reg = 'dfars' and
      part = '36'
order by substring(part from '([0-9]+)')::numeric;

