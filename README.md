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
* Helpful [Github templates](https://help.github.com/en/articles/about-issue-and-pull-request-templates) for issue creation and pull requests 

### Layout

```
django-rest-boilerplate
├── .circleci                           // CircleCI configuration
|   ├── config.yml                      
├── .github                             
|   ├── ISSUE_TEMPLATE                  
|   |   ├── bug---problem.md            // A Github template for reporting bugs
|   |   └── feature_request.md          // A Github template for posting new features
|   ├── PULL_REQUEST_TEMPLATE.md        // A Github template layout for Pull requests
├── apps                                
|   ├── core                            // Django core app
|   ├── users                           // Django Users app
├── conf                                // Django configuration folder
|   ├── urls.py                         // The main url.py file
|   ├── wsgi.py                         // The WSGI handler
|   ├── settings                        // Django settings
|   |   ├── base.py                     // General settings
|   |   ├── local.py                    // Local settings
|   |   ├── production.py               // Production settings
|   |   ├── test.py                     // Test settings
├── devops                              // Devops + Infastructure
|   ├── Docker                          // Docker container
|   |   ├── postgres                    // Postgres Docker
|   |   ├── redis                       // Redis Docker
├── .coveragerc                         
├── .env.example                        // Copy to .env for local development                  
├── .gitignore                          // Default .gitignore                         
├── .pre-commit-config.yaml                         
├── .prospector.yaml                         
├── LICENSE                         
├── Pipfile                             // Pipenv file                      
├── Pipfile.lock                        // Pipenv lock file                         
├── Procfile                            // Declaration of Heroku processes                       
├── README.md                         
├── app.json                            // For automated Heroku deployment                         
├── conftest.py                         
├── docker-compose.yml                  // Docker handling for local development                        
├── manage.py                         
├── pytest.ini                         
├── runtime.txt                         // Python version for Heroku deployment                         
├── setup.cfg                         
├── tasks.py                                             
```

## Documentation

Read our documentation at ..

## Local setup

Download & install the Docker Community edition
* https://www.docker.com/community-edition

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

## Install & Run Locally

This project contains docker integration. You can run it with `pipenv run go-docker`.

In any case before you need to write your `.env` file with correct variables: when using the dockerized
local development setup, copy `.env.local`; otherwise copy `.env.example` to `.env`, and modifiy
accordingly.


## Add git hooks

We are using prospectr + pre-commit to make things workable and clear. Before write any code you need to install
dev dependencies and run `pre-commit install -f` after that. Then whenever you run `git commit` you'll have a fancy
output with checks according to our code standards.

## Prepare a new branch for your work

Work on new `bug/features` will be done in a new branch (*)
There is a convention in the name of the branches used:
**`1-short-description-of-purpose`**

Naming a Branch:
    - Start branch name with the Issue Number: `#1 Initial Issue` > `1-initial-branch-name`
    - Use lowercase only
    - Use dashes to separate words

## Make awesome commits

Commits are the smallest portion of code that can be reviewed and has a
purpose in the codebase. Each commit counts in a branch, not only the full set
of changes.

Please follow this guideline:
https://udacity.github.io/git-styleguide/

To use cool github linking to the issue please add #taskNumber in the end. E.g.:

`docs: add changes to the Readme #123`

## Documentation

Please make sure that each public class, method and function has meaningful documentation which describes the purpose of the code.
To make things easier to follow we use Python annotations to the public functions and method.
Cheat sheet:
https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html

More info here:
https://docs.python.org/3/library/typing.html


