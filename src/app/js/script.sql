--alter user postgres password 'peer';


--------------------------------------------------------------------------------
-- Works thus far, but doesn't list values:
-- \set content `cat C:\Users\smats\git\far_api\src\app\js\json\parts2.json`
-- insert into drop_down_data values(:'content');

-- create temporary table temp_json (values text);
-- \copy temp_json from 'C:\Users\smats\git\far_api\src\app\js\json\parts2.json';
--------------------------------------------------------------------------------

-- File to be pulled must be saved in the Public folder
-- Searching can't be done in the regular file system
drop table if exists temp_json2;
create temporary table temp_json2 (jdata text);
copy temp_json2 from 'C:\Users\Public\parts.json';

drop type if exists json_data;
create type json_data as (reg text,
						  curr_part text,
						  curr_subpart text,
						  curr_section text,
						  tot_subparts text,
						  tot_section text,
						  tot_subsections text
						 );

drop table if exists temp_dd_data;
create table temp_dd_data as
select records.*
from temp_json2,
lateral json_populate_recordset(null::json_data, jdata::json) records;

select *
from temp_dd_data
where curr_section = '4'
;






