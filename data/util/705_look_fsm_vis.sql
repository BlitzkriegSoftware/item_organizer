select row_id, label
	, COALESCE(col_01,'') as col_01
	, COALESCE(col_02 ,'') as col_02
	, COALESCE(col_03 ,'') as col_03
	, COALESCE(col_04 ,'') as col_04
	, COALESCE(col_05 ,'') as col_05
	, COALESCE(col_06 ,'') as col_06
	, COALESCE(col_07 ,'') as col_07
	, COALESCE(col_08 ,'') as col_08
	, COALESCE(col_09 ,'') as col_09
	--, COALESCE(col_10 ,'') as col_10
	--, COALESCE(col_11 ,'') as col_11
from {schema}.item_state_fsm_visualizer
where org_id = '00000000-0000-0000-0000-000000000000'
order by row_id
