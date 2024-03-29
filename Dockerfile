FROM python:3.9

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install

COPY . .
RUN ["chmod", "+x", "/app/start_django.sh"]
CMD ["/bin/sh", "-c", "sh /app/start_django.sh"]
