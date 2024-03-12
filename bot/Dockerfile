FROM python:3.10-alpine

WORKDIR /bot

COPY bot.py .
COPY cursor.py .

RUN apk --no-cache add mariadb-connector-c-dev build-base

RUN pip3 install --no-cache-dir mysqlclient==2.2.1 aiogram==3.4.1 python-dotenv==1.0.0

RUN mkdir logs && touch logs/bot.log

CMD [ "python3", "bot.py" ]