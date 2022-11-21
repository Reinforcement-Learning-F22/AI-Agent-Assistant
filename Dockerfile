FROM python:3.8.6

LABEL MAINTAINER="Bekhruz yoshlikmedia@gmail.com"

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY Aiogram-bot /app

CMD python -u app.py