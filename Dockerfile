FROM python:3.9-buster

WORKDIR /usr/src/app/tg_bot

COPY requirements.txt /usr/src/app/tg_bot/
RUN pip install -r /usr/src/app/tg_bot/requirements.txt
COPY . /usr/src/app/tg_bot
