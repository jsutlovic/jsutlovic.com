FROM python:2
RUN apt-get update -qq && apt-get install -y build-essential libpq-dev
RUN mkdir /app
RUN mkdir /public /public/media /public/static

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uwsgi", "--socket", "0.0.0.0:3031", "-w", "JSutlovic.wsgi:application", "--master", "--processes", "2", "--max-requests", "5000"]

EXPOSE 3031
