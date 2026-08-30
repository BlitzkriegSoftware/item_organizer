#!/usr/bin/env bash

/usr/lib/postgresql/16/bin/pg_dump -U postgres -h 127.0.01 -p 5432 -d postgres --schema myio --schema-only -f ./backup/myio_db.sql
/usr/lib/postgresql/16/bin/pg_dump -U postgres -h 127.0.01 -p 5432 -d postgres -F t -f ./backup/myio_backup.tar