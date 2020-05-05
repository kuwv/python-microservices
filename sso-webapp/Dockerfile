FROM node:lts-alpine AS build

WORKDIR /usr/local/src/app

COPY ./ui/package*.json /usr/local/src/app/

RUN apk add --no-cache --virtual .build-deps python3 ;\
  npm install @vue/cli @vue/cli-service-global -g ;\
  npm install

COPY ./ui /usr/local/src/app

RUN npm run build -- --dest ./dist

FROM python:3.7-alpine

RUN adduser -D -h /usr/local/app webapp

WORKDIR /usr/local/app
COPY . /usr/local/app
COPY --from=build /usr/local/src/app/dist /usr/local/app/static

RUN apk update --no-cache ;\
  apk upgrade --no-cache ;\
  apk add --no-cache --virtual .build-deps \
    gcc \
    libffi-dev \
    mariadb-dev \
    postgresql-dev \
    python3-dev \
    musl-dev ;\
  pip install --no-cache-dir -r requirements.txt ;\
  apk del --no-cache --purge .build-deps ;\
  rm -rf /var/cache/apk/*  ;\
  chown webapp:root /usr/local/app/static/config.json

USER webapp
CMD ["daphne", "-b", "0.0.0.0", "-p", "3000", "app:app"]
