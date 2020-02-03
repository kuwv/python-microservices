FROM kong:0.14.1-alpine

LABEL description="Kong 0.14.1-alpine + kong-oidc plugin"

ENV KONG_PLUGINS=oidc

# TODO: Need to do pseudo release because current is obsolescent :(
RUN apk update --no-cache ;\
  apk upgrade --no-cache ;\
  apk add --no-cache git unzip --virtual .build-deps ;\
  git clone https://github.com/nokia/kong-oidc.git /tmp/kong-oidc ;\
  cd /tmp/kong-oidc && \
  sed -i 's/v[0-9]\+\.[0-9]\+\.[0-9]\+/master/g' kong-oidc-*.rockspec && \
  luarocks make && \
  cd - ;\
  apk del --no-cache --purge .build-deps ;\
  rm -rf /var/cache/apk/*

# USER kong
