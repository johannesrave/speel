FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1


COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install


COPY . app
WORKDIR /app
RUN ["chmod", "+x", "start_django.sh"]

#EXPOSE 8000

#ENTRYPOINT ["sh", "start_django.sh"]
#CMD ["start_django.sh"]