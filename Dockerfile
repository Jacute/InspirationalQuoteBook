FROM python:3.10-alpine

WORKDIR /app

RUN apk --no-cache add mariadb-connector-c-dev build-base

COPY app ./app
COPY project ./project
COPY requirements.txt .
COPY manage.py .
COPY db.json .

RUN pip install --no-cache-dir Django==4.2.7 python-dotenv==1.0.0 mysqlclient==2.2.1 scikit-learn==1.4.0

RUN mkdir logs && touch logs/django.log && touch logs/django_sql_queries.log

CMD ["sh", "-c", "python manage.py migrate && python manage.py loaddata db.json && python manage.py runserver 0.0.0.0:8000"]
