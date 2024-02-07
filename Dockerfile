FROM python:3.10.12-slim

RUN pip install poetry==1.7.1

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./
# poetry complains if no README.md is found
RUN touch README.md

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --no-dev --no-root

COPY app ./app

RUN poetry install --no-dev

# Make port 8501 available to the world outside this container
EXPOSE 8501

ENTRYPOINT ["poetry", "run", "streamlit", "run", "./app/app.py"]
