FROM python:slim

ENV APP_HOME /app
WORKDIR $APP_HOME

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 gday:mate

