select * from dev_all_parts05 where protocol = 1;

select t1.*,
       t2.protocol as protocol
from dev_tag_counts02 t1
join dev_all_prot01 t2 on t1.id_num = t2.id_num;

select *
from dev_tag_counts04
where reg = 'sofars'
;

select * from dev_all_html_prot1;
