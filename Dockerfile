FROM postgres:16.9-trixie
# Install packages
RUN apt update -y
RUN apt upgrade -y
RUN apt install curl ca-certificates cron -y
RUN apt install postgresql-16-cron -y
RUN apt install postgresql-16-pldebugger -y
RUN apt update -y
RUN apt upgrade -y
RUN apt-get install -y python3
RUN apt-get install -y python-is-python3
RUN apt install -y python3-pip python3-venv
RUN apt-get clean 
# UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ENV UV_NO_DEV=1
# .pgpass
RUN mkdir -p /var/lib/postgresql/data
COPY ./data/.pgpass /var/lib/postgresql/data/.pgpass
RUN chmod 0600 /var/lib/postgresql/data/.pgpass
# pg_hba.conf with updates
RUN mkdir -p /var/lib/postgresql/data/pgdata
COPY ./data/pg_hba.conf /var/lib/postgresql/data/pgdata/pg_hba.conf
RUN chmod 0600 /var/lib/postgresql/data/pgdata/pg_hba.conf
# postgres configuration for pg_cron
RUN mkdir -p /var/lib/postgresql/data/pgdata
COPY ./data/configure_pg.sh /var/lib/postgresql/data/configure_pg.sh
RUN chmod +rx /var/lib/postgresql/data/configure_pg.sh
COPY ./data/pg_cron_add.sh /var/lib/postgresql/data/pg_cron_add.sh
RUN chmod +rx /var/lib/postgresql/data/pg_cron_add.sh
COPY ./data/postgresql.conf.cron /var/lib/postgresql/data/postgresql.conf.cron
RUN chmod +r /var/lib/postgresql/data/postgresql.conf.cron
ENV POSTGRES_SHARED_PRELOAD_LIBRARIES="pg_cron"
ENV CRON_DATABASE_NAME="postgres"
ENV IOR_SALT="JDJiJDEyJGU1QTV0Zzk1VGxxVmpBLjdsRERmRnU="
ENV IOR_DB="postgres"
# Use: POSTGRES_USER
# Use: PGPASSWORD 
ENV IOR_SCHEMA="myio"
ENV IOR_PORT="5432"
# Install Application
ENV PYTHONUNBUFFERED=1
ENV LOG_LEVEL=DEBUG
WORKDIR /src
COPY ./pyproject.toml /src
COPY ./src /src
ENV PATH="/app/.venv/bin:$PATH"
RUN uv sync
# Run the application
# RUN uv run main.py