FROM postgres:11.2

COPY init.sh /docker-entrypoint-initdb.d/
RUN chmod +x /docker-entrypoint-initdb.d/init.sh

HEALTHCHECK CMD pg_isready -U ${PROJECT_NAME}