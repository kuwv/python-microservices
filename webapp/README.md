# OAuth2 Webapp example

This is a prototype for using authlib and FastAPI integrating with the auth stack from section one.

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

## Manual testing

Setup environment
```
SSO_REALM=master
SSO_USERNAME=admin
SSO_PASSWORD=admin
SSO_CLIENT_ID=userId
SSO_CLIENT_SECRET=<client_secret>
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
