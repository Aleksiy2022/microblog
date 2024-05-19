FROM python:3.12

COPY twitter_api twitter_api
COPY pyproject.toml poetry.lock ./
COPY README.md ./
COPY alembic alembic
COPY alembic.ini alembic.ini

RUN pip install --upgrade pip  \
    && pip install poetry  \
    && poetry config virtualenvs.create false  \
    && poetry install --no-dev

CMD alembic revision --autogenerate -m "create initial tables"  \
    && alembic upgrade head  \
    && uvicorn twitter_api.main:app --reload --port 8000 --host 0.0.0.0
