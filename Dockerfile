FROM python:3.12

WORKDIR /api
COPY api api
COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
