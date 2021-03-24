FROM tiangolo/uwsgi-nginx-flask:python3.8-2020-12-19

COPY ./app/app/requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

ENV LISTEN_PORT 8000
ENV UWSGI_CHEAPER 4
ENV UWSGI_PROCESSES 16
ENV NGINX_MAX_UPLOAD 10m
ENV NGINX_WORKER_PROCESSES auto
ENV NGINX_WORKER_CONNECTIONS 2048

COPY ./app /app

RUN mkdir -p /app/logs/

EXPOSE 8000