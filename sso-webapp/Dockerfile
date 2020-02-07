FROM node:lts-alpine AS build

WORKDIR /app

COPY ./ui/package*.json /app/

RUN apk add --no-cache --virtual .build-deps python3 ;\
  npm install @vue/cli @vue/cli-service-global -g ;\
  npm install

COPY ./ui /app

RUN npm run build

FROM python:3.7-alpine

RUN adduser -D -h /app webapp

WORKDIR /app
COPY . /app
COPY --from=build /app/dist /app/static

RUN apk update --no-cache ;\
  apk upgrade --no-cache ;\
  apk add --no-cache --virtual .build-deps \
    gcc \
    libffi-dev \
    mariadb-dev \
    postgresql-dev \
    python3-dev \
    musl-dev ;\
  apk add --no-cache openssl ;\
  pip install --no-cache-dir -r requirements.txt ;\
  apk del --no-cache --purge .build-deps ;\
  rm -rf /var/cache/apk/*

USER webapp
CMD ["daphne", "-b", "0.0.0.0", "-p", "3000", "app:app"]
