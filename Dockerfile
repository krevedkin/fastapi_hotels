FROM python:3.10

ARG CONTEXT=dev

RUN echo "CONTEXT=$CONTEXT"

WORKDIR /code

RUN pip install poetry 

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /code/

# RUN poetry install --no-dev

RUN [ "$CONTEXT" = "dev" ] && poetry install --no-dev || poetry install

COPY . .

RUN chown root /code/docker/*.sh && chmod a+x /code/docker/*.sh
