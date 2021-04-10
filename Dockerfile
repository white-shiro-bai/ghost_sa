FROM tiangolo/uwsgi-nginx-flask:python3.8-2020-12-19

COPY ./app/app/requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

# RUN echo 172.18.5.10    bigdata-master-01.chinagoods.te bigdata-master-01 >> /etc/hosts && \
#     echo 172.18.5.14    bigdata-util-gateway-01.chinagoods.te bigdata-util-gateway-01 >> /etc/hosts && \
#     echo 172.18.5.17    bigdata-node-01.chinagoods.te bigdata-node-01 >> /etc/hosts  && \
#     echo 172.18.5.15    bigdata-node-02.chinagoods.te bigdata-node-02 >> /etc/hosts  && \
#     echo 172.18.5.16    bigdata-node-03.chinagoods.te bigdata-node-03 >> /etc/hosts  && \
#     echo 172.18.5.2    bigdata-node-04.chinagoods.te bigdata-node-04 >> /etc/hosts   && \
#     echo 172.18.5.3    bigdata-node-05.chinagoods.te bigdata-node-05 >> /etc/hosts   && \
#     echo 172.18.5.4    bigdata-node-06.chinagoods.te bigdata-node-06 >> /etc/hosts

ENV UWSGI_INI /app/uwsgi.ini
ENV LISTEN_PORT 8000
ENV UWSGI_CHEAPER 1
ENV UWSGI_PROCESSES 2
ENV NGINX_MAX_UPLOAD 10m
ENV NGINX_WORKER_PROCESSES auto
ENV NGINX_WORKER_CONNECTIONS 20480

COPY ./app /app
    
RUN mkdir -p /app/logs/ && \
    mkdir -p ~/.pip

COPY ./pip.conf ~/.pip/

EXPOSE 8000