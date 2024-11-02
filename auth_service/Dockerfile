FROM python:3.11-slim

RUN mkdir /auth_service && apt-get update && apt-get install -y git
WORKDIR /auth_service

COPY ./poetry.lock /auth_service/
COPY ./pyproject.toml /auth_service/

RUN pip install poetry && poetry config virtualenvs.create false && poetry install

COPY ./ /auth_service/
