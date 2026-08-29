#!/bin/bash
/usr/lib/postgresql/17/bin/pg_dump -U postgres -h 127.0.01 -p 5432 -d salesdb --schema public --schema-only -f ./salesdb.sql
/usr/lib/postgresql/17/bin/pg_dump -U postgres -h 127.0.01 -p 5432 -d salesdb -F t -f salesdb_backup.tar