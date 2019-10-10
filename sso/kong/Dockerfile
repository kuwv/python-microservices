FROM kong:0.14-centos

LABEL description="Centos 7 + Kong 0.14 + kong-oidc plugin"

ENV KONG_PLUGINS=oidc

RUN yum install -y git unzip \
  && yum clean all \
  && rm -rf /var/cache/yum \
  && luarocks install kong-oidc
