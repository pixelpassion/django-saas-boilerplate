FROM redis:5.0.4

COPY healthcheck.sh /usr/local/bin/

RUN chmod +x /usr/local/bin/healthcheck.sh

HEALTHCHECK CMD sh /usr/local/bin/healthcheck.sh

EXPOSE 6379