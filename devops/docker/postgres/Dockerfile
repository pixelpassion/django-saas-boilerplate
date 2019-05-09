FROM postgres:11.2

COPY init.sh /docker-entrypoint-initdb.d/

RUN chmod +x /docker-entrypont-initdb.d/init.sh

HEALTHCHECK CMD pg_isready -U $POSTGRES_USER