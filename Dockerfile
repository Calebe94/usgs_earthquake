FROM python:3.11-slim

WORKDIR /code

RUN pip install --upgrade pip && pip install poetry

COPY . /code/

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

ADD ./entrypoint.sh /

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

EXPOSE 8000
