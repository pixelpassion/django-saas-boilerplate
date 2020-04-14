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

# Install Poetry & ensure it is in $PATH
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | POETRY_PREVIEW=1 python
ENV PATH "/root/.poetry/bin:/opt/venv/bin:${PATH}"

# Only copying these files here in order to take advantage of Docker cache. We only want the
# next stage (poetry install) to run if these files change, but not the rest of the app.
COPY pyproject.toml poetry.lock ./

# Currently poetry install is significantly slower than pip install, so we're creating a
# requirements.txt output and running pip install with it.
# Follow this issue: https://github.com/python-poetry/poetry/issues/338
# Setting --without-hashes because of this issue: https://github.com/pypa/pip/issues/4995
RUN poetry config virtualenvs.create false \
                && poetry export --without-hashes -f requirements.txt --dev \
                |  poetry run pip install -r /dev/stdin \
                && poetry debug

COPY . /app

# Because initially we only copy the lock and pyproject file, we can only install the dependencies
# in the RUN above, as the `packages` portion of the pyproject.toml file is not
# available at this point. Now, after the whole package has been copied in, we run `poetry install`
# again to only install packages, scripts, etc. (and thus it should be very quick).
# See this issue for more context: https://github.com/python-poetry/poetry/issues/1899
RUN poetry install --no-interaction

RUN mkdir ./_static ./_media || true

COPY ./devops/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
RUN chmod +x ./manage.py

CMD /entrypoint.sh

HEALTHCHECK CMD curl -s -S -H http://$HOSTNAME:8000

EXPOSE 8000