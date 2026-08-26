# Scripts

Guide to scripts

- [Scripts](#scripts)
  - [Start Postgres and install cron \& pg\_cron](#start-postgres-and-install-cron--pg_cron)
    - [What does it do?](#what-does-it-do)
  - [open a bash shell on Postgres container](#open-a-bash-shell-on-postgres-container)
  - [stop postgres](#stop-postgres)


## Start Postgres and install cron & pg_cron

```powershell
.\start-pg.ps1
```

### What does it do?

1. Creates a custom variation of **posgres** from `Dockerfile`, Adds in plugins we want (see file above), Configures plugins 

2. Starts container running, which starts base postgres

3. Reconfigures postgres + Restarts postgres, via:

```bash
./data/configure_pg.sh
```

4. Finishes up by running SQL script:

```bash
./data/pg_cron_add.sh
```

5. Postgres w. plugins ready for use

6. Starts python application

Notes:
* Horrible work arounds, if you have a better way, create an issue, or put in a PR
* It works though.

## open a bash shell on Postgres container

```powershell
.\bash-pg.ps1
```

It opens a bash shell...with handy guidance

```text
SQL Scripts Folder: /var/lib/postgresql/data
Postgres Logs: /var/log/postgresql
Postgres Utilities Folder: /usr/lib/postgresql/16/bin
In general to run postgres commands you will have to run as the 'postgres' user
su -- postgres -c {pg_command}
```

```bash
root@9022c51945a7:/var/lib/postgresql/data# 
```

## stop postgres

```powershell
.\stop-pg.ps1
```
