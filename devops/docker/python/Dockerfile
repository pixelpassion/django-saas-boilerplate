FROM python:3.7

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV DEBIAN_FRONTEND noninteractive

WORKDIR /app

RUN apt-get clean \
    && apt-get update \
    && apt-get install -y \
       locales \
       locales-all \
       apt-utils \
    && locale-gen en_US.UTF-8

ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

RUN apt-get install -y \
       build-essential \
       libpq-dev \
       postgresql-client \
       curl \
       binutils \
       libproj-dev \
       gdal-bin

RUN pip3 install --upgrade \
    pip \
    wheel \
    setuptools \
    pipenv

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