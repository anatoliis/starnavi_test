FROM python:3.8.2-alpine3.11

RUN set -ex && mkdir -p /opt/sn_api

WORKDIR /opt/sn_api

RUN set -ex && apk update && apk upgrade
RUN apk add gcc make musl-dev postgresql-dev linux-headers

RUN set -ex && pip install pipenv --upgrade

ADD Pipfile /opt/sn_api
ADD Pipfile.lock /opt/sn_api

RUN set -ex && pipenv install --ignore-pipfile --system --deploy

ADD . /opt/sn_api

RUN set -ex && python3.8 -m compileall .
RUN set -ex && chmod +x /opt/sn_api/docker-entrypoint.sh

ENTRYPOINT ["/opt/sn_api/docker-entrypoint.sh"]
