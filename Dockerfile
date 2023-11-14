FROM python:3.11

ARG MY_ENV
ENV MY_ENV=${MY_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.4.0

RUN pip install "poetry==$POETRY_VERSION"
WORKDIR /pilligrim
COPY poetry.lock pyproject.toml /pilligrim/
RUN poetry config installer.max-workers 10
RUN poetry config virtualenvs.create false \
  && poetry install $(test "$MY_ENV" == production && echo "--no-dev") --no-interaction --no-ansi

COPY . /pilligrim
RUN chmod -R 0777 /pilligrim

EXPOSE 8008
RUN adduser --disabled-password docker-admin
USER docker-admin


