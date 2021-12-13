FROM python:3.9

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

#RUN pip install rcssmin --install-option="--without-c-extensions"
#RUN pip install rjsmin --install-option="--without-c-extensions"
RUN #apt-get install python3-dev
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install

COPY . .
#RUN ["chmod", "+x", "start_django.sh"]
#RUN ["python", "manage.py", "makemigrations", "player"]
#RUN ["python", "manage.py", "migrate"]
#CMD ["python", "manage.py", "runserver", "8000"]

#EXPOSE 8000

#ENTRYPOINT ["sh", "start_django.sh"]
#CMD ["start_django.sh"]