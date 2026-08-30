# About DATA folder

- [About DATA folder](#about-data-folder)
  - [Files and folders](#files-and-folders)
  - [Scripts](#scripts)
  - [References](#references)

## Files and folders

| Object | Description | Used By |
| :--- | :--- | :--- |
| .pgpass | Generated File | docker |
| configure_pg.sh | script | docker |
| create_extensions.sql | script | docker |
| dump_schema.sh | utility | handy script to dump schemas to the `./backup` folder |
| iodb/ | The files used to generate an `IO` | Templates |
| pgdata/ | (DO NOT CHANGE) | (REGENERATED) |
| pg_cron_add.sh | script | docker |
| pg_hba.conf | file | docker |
| pg_script_run.sh | script | plays a SQL at docker postgres |
| postgresql.conf.cron | file | docker |
| README.md | (sic) | This document |
| temp/ | (DO NOT CHANGE) | (REGENERATED) |
| util/ | Utilities | Handy |

## Scripts

The script [make-itemorg](..\scripts\make-itemorg.ps1) is used to transform the SQL scripts in `iodb/` which are in the form of:

- `###` the order the script will be executed in lowest starting at 100 to `...`
- `_` separator
- `{script name}` which can contain `_`
- `_{suffix}`:
  - `` (nothing) a table definition with indexes
  - `_data` seed data
  - `_fx` function
  - `_p` procedure

Scripts are transformed by the script, substituting these tokens for the actual values:

- `{schema}` the schema name the default being `myio`
- `{role}` custom role, currently not used

Transformed scripts are put into `temp/` so you can see what is "played" at Postgres. 

## References

- [Full Text Search](https://tacnode.io/post/full-text-search-postgresql-complete-guide)