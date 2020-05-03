FROM python:3.7.6-slim

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY entrypoint.py /entrypoint.py

ENTRYPOINT python /entrypoint.py
