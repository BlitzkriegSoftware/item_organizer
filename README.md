# item_organizer
An open source easy to run item organizer for backlog management

- [item\_organizer](#item_organizer)
  - [See also](#see-also)
  - [Project organization](#project-organization)
  - [Environment Variables](#environment-variables)
    - [Docker Postgres SQL Connection String](#docker-postgres-sql-connection-string)
  - [Running locally](#running-locally)
    - [Setup Python](#setup-python)
    - [Make sure Docker is running](#make-sure-docker-is-running)
    - [Start Postgres \& Plug-ins, and program](#start-postgres--plug-ins-and-program)
  - [Project Organization](#project-organization-1)

## See also

- [./scripts](./scripts/README.md)

## Project organization

Classic Python + Postgres

| Folder | Purpose |
| :--- |:--- |
| .github | Github Automations and Templates (ignore) |

## Environment Variables

in powershell [setx](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/setx) is friend followed by a **restart of the shell**, or if you have [chocolatey](https://chocolatey.org/) installed, `refreshenv`.

| Variable | Description | Example |
|:---|:---|:---|
| IOR_SQL | Connection string (2) | See Text  |
| IOR_SALT | Password Salt (1) | JDJiJDEyJGU1QTV0Zzk1VGxxVmpBLjdsRERmRnU= |
| | | |
| | | |
| | | |

(1) See [auth manager](tests\test_auth_manager.py)::test_hash_password to see how this is generated
(2) See connection string below

### Docker Postgres SQL Connection String

> You should change the password for production!

```text
postgresql://postgres:password123-@localhost:5432/postgres
```

Seach the scripts to find out where it is used.

## Running locally

### Setup Python

```powershell
uv venv
 .\.venv\Scripts\activate
uv sync
```

### Make sure Docker is running

Docker must be running

### Start Postgres & Plug-ins, and program

```powershell
.\start-pg.ps1
```

## Project Organization