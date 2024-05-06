FROM python:3.12

COPY api api
COPY pyproject.toml poetry.lock ./
COPY README.md ./

RUN pip install --upgrade pip  \
    && pip install poetry  \
    && poetry config virtualenvs.create false  \
    && poetry install --no-dev

WORKDIR api
CMD python main.py
