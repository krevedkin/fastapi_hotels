FROM python:3.10

RUN mkdir /code

WORKDIR /code

RUN pip install poetry 

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /code/

RUN poetry install --no-dev

COPY . .

RUN chown root /code/docker/*.sh && chmod a+x /code/docker/*.sh