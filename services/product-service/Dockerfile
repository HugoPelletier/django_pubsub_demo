FROM python:3.7.0-slim-stretch  as base

COPY requirements.txt /tmp/
RUN pip install --upgrade pip

WORKDIR /code

## Release target for running into QA and Production ##
FROM base as release
RUN pip install -r /tmp/requirements.txt
COPY . /code

## Development Image including SonarQube Dependencies for local and CI Pipeline ##
FROM base as develop
RUN pip install -r /tmp/requirements.txt
COPY . /code