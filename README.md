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
  - [Documentation: Sphinx](#documentation-sphinx)
    - [Clean output folder](#clean-output-folder)
    - [Generating Documentation](#generating-documentation)
    - [Live HTML documentation](#live-html-documentation)

## See also

- [./scripts](./scripts/README.md)

## Project organization

Classic Python + Postgres

| Folder | Purpose |
| :--- |:--- |
| .github | Github Automations and Templates (ignore) |

## Environment Variables

in powershell [setx](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/setx) is friend followed by a **restart of the shell**, or if you have [chocolatey](https://chocolatey.org/) installed, `refreshenv`.

See [Admin](./docs/README.md)

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


## Documentation: Sphinx

- See:
  - [sphinx-doc.org](https://www.sphinx-doc.org/en/master/index.html)

### Clean output folder

```powershell
 .\make.ps1 clean
 ```

### Generating Documentation

```powershell
uv run sphinx-build -M markdown docs/source docs/build
```

### Live HTML documentation

```powershell
uv run sphinx-autobuild docs/source docs/build/html
```
