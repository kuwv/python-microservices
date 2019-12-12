FROM kong:0.14.1-centos

LABEL description="Centos 7 + Kong 0.14.1-centos + kong-oidc plugin"

ENV KONG_PLUGINS=oidc

RUN yum install -y git unzip ;\
  yum clean all ;\
  rm -rf /var/cache/yum ;\ 
  git clone https://github.com/nokia/kong-oidc.git /tmp/kong-oidc ;\
  pushd /tmp/kong-oidc \
  && sed -i 's/v[0-9]\+\.[0-9]\+\.[0-9]\+/master/g' kong-oidc-*.rockspec \
  && luarocks make \
  && popd
  # TODO: Need to do pseudo release because current is obsolescent :(
  # && luarocks install kong-oidc

# USER kong
