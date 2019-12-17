# OAuth2 Webapp example

This is a prototype for using authlib and FastAPI integrating with the auth stack from section one.

## Description

FastAPI is a very fast asynchronous Python web framework that has support of OpenID-Connect and OAuth. Currently, this support is mostly limited to the legacy password based OAuth flow. This flow is fine when building systems that self-host auth, but becomes problematic when passwords must be shared between a user, thier identity provider and a third party app. This section is designed to provide a working example for implementing three-legged auth using FastAPI with Authlib to protect a resource. Instead of using the password flow it is designed to utilize the much regarded authorization flow instead.

## Features
- [x] OpenAPI integration
- [x] Resource Protector
- [ ] Client
- [x] Identity Propagation
- [x] Scopes
- [ ] RBAC
- [x] Logging
- [ ] Access Audit
- [x] Authlib JOSE
- [ ] OpenID-Connect
- [ ] UI (via multiprocessing)
- [ ] tls/http2

## Manual testing

Setup environment
```
SSO_REALM=master
SSO_USERNAME=admin
SSO_PASSWORD=admin
SSO_CLIENT_ID=webapp
SSO_CLIENT_SECRET=<retrieve from keycloak>
```

Retrieve token using client.

```
export TOKEN=$(curl -s \
-X POST "http://localhost:8080/auth/realms/${SSO_REALM}/protocol/openid-connect/token" \
-d 'grant_type=client_credentials' \
-d "client_id=${SSO_CLIENT_ID}" \
-d "client_secret=${SSO_CLIENT_SECRET}" \
-d 'redirect_uri=http://localhost:8000/webapp/token' | jq -r '.access_token')
```

Retrieve token using CLI.
```
export TOKEN=$(curl -s \
-X POST "http://localhost:8080/auth/realms/${SSO_REALM}/protocol/openid-connect/token" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "username=${SSO_USERNAME}" \
-d "password=${SSO_PASSWORD}" \
-d 'grant_type=password' \
-d 'client_id=admin-cli' | jq -r '.access_token')
```

Check if the token can access the Webapp
```
curl -s -H "Authorization: Bearer ${TOKEN}" http://localhost:8000/webapp/token | jq .
```
