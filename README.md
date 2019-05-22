[![unicorn.supplies](https://img.shields.io/badge/made%20by-Automagically-blue.svg)](https://www.unicorn.supplies/)

# `django-rest-boilerplate`

A boilerplate to get started with Django & django-rest-framework. It helps to kickstart a project with fundamental infastructure and services. 

## Features

* Optimized for Python 3.7+ and Django 2.2+
* A nicely formatted [settings.py](https://docs.djangoproject.com/en/2.2/ref/settings/)
* [12-Factor](12factor.net) based settings via [django-environ](12factor.net)
* Based on an API build with the awesome [django-rest-framework](https://www.django-rest-framework.org)
* Good considerated defaults for API [Throttling](https://www.django-rest-framework.org/api-guide/throttling/), [Pagination](https://www.django-rest-framework.org/api-guide/pagination/) and [Exception handling](https://www.django-rest-framework.org/api-guide/exceptions/)
* API documentation build with [Swagger](https://swagger.io)
* Optimized testing with [py.test](https://docs.pytest.org/en/latest/) & Coverage 100%
* A helpful [Makefile](https://en.wikipedia.org/wiki/Make_(software)) for faster and easier deployments
* Support for asynchronous task handling with [RQ](https://python-rq.org)
* Email sending with [Sendgrid](https://sendgrid.com) support
* Build in support for [Sentry](https://sentry.io) Error monitoring
* Continuous integration with [CircleCI](https://circleci.com)
* Deployment for Heroku with [Procfile](https://devcenter.heroku.com/articles/procfile), [app.json](https://devcenter.heroku.com/articles/app-json-schema), [Whitenoise](https://devcenter.heroku.com/articles/django-assets) and [Foreman](https://devcenter.heroku.com/articles/heroku-local#run-your-app-locally-using-foreman)
* Docker files of [Postgres](https://www.postgresql.org) and [Redis](https://redis.io) for easier local development 
* Support of [Docker deployments on Heroku](https://devcenter.heroku.com/categories/deploying-with-docker)
* Code formatting done with [Black](https://www.mattlayman.com/blog/2018/python-code-black/)
* [Werkzeug](https://github.com/joeyespo/django-werkzeug), [iPython](https://ipython.org/install.html), [django-extensions](https://github.com/django-extensions/django-extensions), [django-debug-toolbar](https://github.com/jazzband/django-debug-toolbar) and [ipdb](https://pypi.org/project/ipdb/) installed for local debugging
* [Pipenv](https://github.com/pypa/pipenv) integrated with the required packages
* [Django Admin](https://docs.djangoproject.com/en/2.2/ref/contrib/admin/) with some links & optimizations

## Documentation

Read our documentation at ..

## Local setup

Download & install the Docker Community edition
* https://www.docker.com/community-edition

Install [docker-dns](https://github.com/zanaca/docker-dns) to make containers available by their hostnames

Run the following commands, it will build & start the needed containers (Django, Worker, Postgres DB, Redis, Mailhog):

```bash
pipenv install --dev
inv db
inv migrate
inv create-admin
inv runserver
```



Open your browser and go to http://localhost:8000/

## Deployment

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

