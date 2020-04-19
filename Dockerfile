# FROM python:3-alpine
FROM tejasa97/alpine_python
ENV PYTHONUNBUFFERED 1

# RUN apk add --no-cache postgresql-libs bash && \
# 	apk add --no-cache --virtual .build-deps musl-dev 

# Allows docker to cache installed dependencies between builds
RUN apk add --no-cache bash
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt --no-cache-dir
# RUN apk --purge del .build-deps

COPY . code
WORKDIR code

EXPOSE 5000
ENV FLASK_APP main

# CMD python main.py
CMD gunicorn --bind 0.0.0.0:5000 --access-logfile - wsgi:app -w 9 --threads 12
