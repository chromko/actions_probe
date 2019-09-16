
FROM python:3.7-alpine

ARG BUILD_SOURCE
ARG REPO_NAME
ARG REPO_OWNER

LABEL org.opencontainers.image.vendor=${REPO_OWNER} \
      org.opencontainers.image.title=${REPO_NAME} \
      org.opencontainers.image.source=${BUILD_SOURCE}

ARG USER=app
ARG WORKDIR=/app


RUN set -ex; \
    addgroup ${USER} && adduser -D -s /bin/sh -G ${USER} ${USER};

EXPOSE 5000

COPY requirements.txt ./
RUN set -ex;\
    apk add postgresql-dev; \
    pip3 install -r requirements.txt;
COPY . .

RUN set -xe; \
    chmod a+x ./docker-entrypoint.sh; \
    mkdir data; \
    chown ${USER}:${USER} ./data
USER $USER
ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["python3" , "-u", "app/app.py"]
