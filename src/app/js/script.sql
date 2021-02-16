-- Create table for far_parts
-- create table drop_down_data (
--     id serial PRIMARY KEY,
--     jdata json
-- );

--select * from drop_down_data;

--copy f_content "/c/Users/smats/git/far_api/src/app/js/json/parts.json";
--INSERT INTO new_contacts VALUES(:'content');

--alter user postgres password 'peer';

-- INSERT INTO drop_down_data(jdata)
-- FROM json_populate_recordset(
--   '{"reg": "far", "curr_part": 1, "curr_subpart": 1, "curr_section": 1, "tot_subparts": 15, "tot_section": 5, "tot_subsections": 3}'
-- );

-- truncate table drop_down_data;
-- select * from drop_down_data;

--------------------------------------------------------------------------------
-- Works thus far, but doesn't list values:
-- \set content `cat C:\Users\smats\git\far_api\src\app\js\json\parts2.json`
-- insert into drop_down_data values(:'content');

-- create temporary table temp_json (values text);
-- \copy temp_json from 'C:\Users\smats\git\far_api\src\app\js\json\parts2.json';

-- this works, but must have all data on one line:
-- create temporary table temp_ugh (values text)
-- \copy temp_ugh from 'C:\Users\smats\git\far_api\src\app\js\json\parts.json'
-- select values::json->'reg' as name from temp_ugh;
--------------------------------------------------------------------------------

-- File to be pulled must be saved in the Public folder; searching can't be done
--   in the regular file system
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






