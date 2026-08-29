select row_id, label
	, col_00
	, col_01
	, col_02 
	, col_03 
	, col_04 
	, col_05 
	, col_06 
	, col_07 
	, col_08 
	, col_09 
from myio.item_state_fsm_visualizer
where org_id = '00000000-0000-0000-0000-000000000000'
order by row_id
