FROM python:3.8-slim
# Get envsubst from gettext-base
RUN apt-get update &&\
    apt-get install gettext-base &&\
    pip install pywebpush requests
WORKDIR /push
COPY . .
CMD envsubst < config.json.example > config.json && python sendpush.py
