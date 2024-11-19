FROM python:3.11-slim

RUN mkdir /company_structure_service && apt-get update && apt-get install -y git
WORKDIR /company_structure_service

COPY ./poetry.lock /company_structure_service/
COPY ./pyproject.toml /company_structure_service/

RUN pip install poetry && poetry config virtualenvs.create false && poetry install

COPY ./ /company_structure_service/
