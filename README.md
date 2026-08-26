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

| Variable | Description | Example |
|:---|:---|:---|
| IOR_SQL | Connection string |   |
| | | |
| | | |
| | | |
| | | |

### Docker Postgres SQL Connection String

```text
postgresql://postgres:password123-@localhost:5432/postgres
```


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