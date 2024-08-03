FROM python:3.9

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT 8000
EXPOSE 8000

CMD exec gunicorn Fin4All.wsgi:application --bind :$PORT --workers 1 --threads 8