FROM python:3.7

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV DEBIAN_FRONTEND noninteractive

RUN ls
WORKDIR /app


ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

COPY ./requirements.txt ./
RUN pip install -r requirements.txt
COPY . /app
RUN mkdir ./_static ./_media || true

COPY ./devops/docker/python/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
RUN chmod +x ./manage.py

CMD /entrypoint.sh

HEALTHCHECK CMD curl -s -S -H http://$HOSTNAME:8000

EXPOSE 8000