
define get_sid
  curl -s -X GET http://localhost:8001/services/$(1) | jq .id
endef

define register_client
  docker exec -it sso_keycloak_1 keycloak/bin/kcreg.sh config credentials --server http://localhost:8080/auth --realm master --user admin --password admin --secret password
  docker exec -it sso_keycloak_1 keycloak/bin/kcreg.sh create -t password -s clientId=kong -s protocol=openid-connect -s rootUrl=http://localhost:8000/$(2)/*
endef

.PHONY: build-sso
build-sso:
	docker build -t kong:0.14-centos-oidc sso/kong/

.PHONY: build
build: build-sso

.PHONY: start-sso
start-sso: build-sso
	docker-compose -f sso/docker-compose.yml up -d kong-db
	docker-compose -f sso/docker-compose.yml run --rm kong kong migrations up
	docker-compose -f sso/docker-compose.yml up -d kong
	docker-compose -f sso/docker-compose.yml up -d keycloak-db
	docker-compose -f sso/docker-compose.yml up -d keycloak

test:
	SID=$(call get_sid,mock-service)
	$(call register_client,mock-service)

.PHONY: stop-sso
stop-sso:
	docker-compose -f sso/docker-compose.yml down

.PHONY: start
start: start-sso

.PHONY: stop
stop: stop-sso
