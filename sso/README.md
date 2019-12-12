# SSO setup - Using Ansible to deploy KeyCloak / Kong


## Synopsis

Setup SSO with KeyCloak / Kong using Ansible and Docker.


## Description

KeyCloak is an IAM that provides openid-connect, SAML, and JWT for security. Kong is an API gateway
that secures access to API endpoints. An API Geteway allows multiple microservices to be consolidated
within one endpoint. Authentication and authorization can then be delegated to the IAM server. This
guide provides a mock deployment demonstrating Ansible instead of docker-compose.


## Setup

### Using pipenv for development (or siloed environment)

Setup a virtual environment
```
pipenv shell
```

Install development dependencies
```
pipenv install --dev
```

Execute deployment
```
ansible-playbook -i localhost, deploy.yml
```

Remove deployment
```
ansible-playbook -i localhost, deploy.yml --tags=remove
```


## Refrences
- https://www.jerney.io/secure-apis-kong-keycloak-1/
