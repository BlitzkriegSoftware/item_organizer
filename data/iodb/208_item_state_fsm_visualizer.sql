-- DROP TABLE IF EXISTS {schema}.item_state_fsm_visualizer;

-- Editor: More than this many states is not a good idea.
CREATE TABLE IF NOT EXISTS {schema}.item_state_fsm_visualizer
(
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id uuid null default '00000000-0000-0000-0000-000000000000',
    row_id int default 0,
    label text COLLATE pg_catalog."default",
    col_01 text COLLATE pg_catalog."default",
    col_02 text COLLATE pg_catalog."default",
    col_03 text COLLATE pg_catalog."default",
    col_04 text COLLATE pg_catalog."default",
    col_05 text COLLATE pg_catalog."default",
    col_06 text COLLATE pg_catalog."default",
    col_07 text COLLATE pg_catalog."default",
    col_08 text COLLATE pg_catalog."default",
    col_09 text COLLATE pg_catalog."default",
    col_10 text COLLATE pg_catalog."default",
    col_11 text COLLATE pg_catalog."default",
    col_12 text COLLATE pg_catalog."default",
    col_13 text COLLATE pg_catalog."default",
    col_14 text COLLATE pg_catalog."default",
    col_15 text COLLATE pg_catalog."default",
    col_16 text COLLATE pg_catalog."default",
    col_17 text COLLATE pg_catalog."default",
    col_18 text COLLATE pg_catalog."default",
    col_19 text COLLATE pg_catalog."default",
    col_20 text COLLATE pg_catalog."default",
    col_21 text COLLATE pg_catalog."default",
    col_22 text COLLATE pg_catalog."default",
    col_23 text COLLATE pg_catalog."default",
    col_24 text COLLATE pg_catalog."default",
    col_25 text COLLATE pg_catalog."default",
    col_26 text COLLATE pg_catalog."default",
    col_27 text COLLATE pg_catalog."default",
    col_28 text COLLATE pg_catalog."default",
    col_29 text COLLATE pg_catalog."default",
    col_30 text COLLATE pg_catalog."default",
    col_31 text COLLATE pg_catalog."default",
    col_32 text COLLATE pg_catalog."default",
    col_33 text COLLATE pg_catalog."default",
    col_34 text COLLATE pg_catalog."default",
    col_35 text COLLATE pg_catalog."default",
    col_36 text COLLATE pg_catalog."default",
    col_37 text COLLATE pg_catalog."default",
    col_38 text COLLATE pg_catalog."default",
    col_39 text COLLATE pg_catalog."default",
    col_40 text COLLATE pg_catalog."default",
    col_41 text COLLATE pg_catalog."default",
    col_42 text COLLATE pg_catalog."default",
    col_43 text COLLATE pg_catalog."default",
    col_44 text COLLATE pg_catalog."default",
    col_45 text COLLATE pg_catalog."default",
    col_46 text COLLATE pg_catalog."default",
    col_47 text COLLATE pg_catalog."default",
    col_48 text COLLATE pg_catalog."default",
    col_49 text COLLATE pg_catalog."default"
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS {schema}.item_state_fsm_visualizer
    OWNER to postgres;