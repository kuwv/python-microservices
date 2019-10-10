FROM python:3.7-alpine

RUN adduser -D -h /app hypercorn

WORKDIR /app
COPY . /app

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

USER hypercorn
CMD ["hypercorn", "-b", "0.0.0.0:5000", "app:app"]
