# SSO setup - Using Ansible to deploy KeyCloak / Kong


## Synopsis

Setup SSO with KeyCloak / Kong using Ansible and Docker.


## Description

KeyCloak is an IAM that provides openid-connect, SAML, and JWT for security. Kong is an API gateway
that secures access to API endpoints. An API Geteway allows multiple microservices to be consolidated
within one endpoint. Authentication and authorization can then be delegated to the IAM server. This
guide provides a mock deployment demonstrating Ansible instead of docker-compose.


## Manual testing

Setup environment
```
SSO_REALM=master
SSO_USERNAME=admin
SSO_PASSWORD=admin
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
curl -s -H "Authorization: Bearer ${TOKEN}" http://localhost:8000/mock | jq .
```

## Refrences
- https://www.jerney.io/secure-apis-kong-keycloak-1/
