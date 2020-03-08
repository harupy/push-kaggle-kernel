FROM python:3.7.6-slim

RUN pip install kaggle
COPY entrypoint.py /entrypoint.py

ENTRYPOINT python /entrypoint.py
