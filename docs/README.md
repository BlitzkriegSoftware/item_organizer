# Administration and Setup Guide

This is the guide to customizing your system

Make sure to read:

- [Base Readme](../README.md)
- [Data](../data/README.md)
- [Scripts](../scripts/README.md)

## Environment Variables

| Variable | Description | Example |
| :--------------- | :------------------------------------ | :----------------------------------------------------------------------- |
| POSTGRES_USER | postgres user | postgres |
| PGPASSWORD | password | password123- |
| IOR_APP_PORT | python app port | 8097 |
| IOR_DB_PORT | postgres port | 5432 |
| IOR_HOST | Hostname | localhost |
| IOR_DB | DB Name | postgres |
| IOR_FERMAT | encryption key | must be generated andd set as an environment variable, must not change after IO has been made, use unit tests to generate |
| IOR_JWT_KEY | openssl rand -hex 32 | Key for JWT Tokens |
| IOR_SALT | password salt | must be generated and set as an environment variable, must not change after IO has been made, use unit tests to generate |
| IOR_SCHEMA | schema | myio is the default, change this if you generate some other schema |
| IOR_SQL | Connection string | postgresql://postgres:password123-@localhost:5432/postgres |
| LOG_LEVEL | DEBUG, INFO, WARNING, ERROR, CRITICAL | Debug is default |
| UV_NO_DEV | Cache UV build steps | leave unless issues |
| PYTHONUNBUFFERED | Stop buffering log output | solves lost log issue in containers |

## Link-Helpers

In hyperlinks and other elements created by a helper, these conventions are used to supply context and data:

- `data-kind`= {table name}
- `data-id` = {id into that table} note these exceptions
  - `-1` look in 'href' property for url
  - `-2` look in 'anchor text' for info
