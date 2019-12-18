# Implementing Python Microservices with OpenID-Connect/OAuth2


## Index

* [ License ](LICENSE.md)
* [SSO setup - Using Ansible to deploy KeyCloak / Kong](./sso/README.md)
* [Webapp setup - Setup resource web application to endpoint with KeyCloak / Kong](./webapp/README.md)


## Synopsis

This project is intended as a reference archicture for implementing OIDC/OAuth2 secure microserices using Python.


## Description
This is intended to be a reference architecture to demonstrate various IAM implementations with Python.

## Features
- [x] KeyCloak, Kong, and Mock endpoint
- [x] Resource endpoint
- [x] Ansible playbooks
- [ ] Ansible Roles
- [ ] UI with JS module imports
- [ ] Proxy KeyCloak / Kong
<!---
- [ ] Cookiecutter
- [ ] Task queue
- [ ] GRPC
- [ ] OpenShift deployment
--->

## Setup

### Using Vagrant

Start VM with application
```
vagrant up
```

Removing application from VM
```
vagrant provision --provision-with remove
```

Login
```
vagrant ssh
```

### Using pipenv

Setup a virtual environment
```
pipenv shell
```

Install development dependencies
```
pipenv install --dev
```

### Using automake

Build the application
```
make start
```

Tear-down the application
```
make stop
```

Check help for additional commands
```
make help
```

<!---
## See also

- [The Twelve-Factor App](https://12factor.net/)
- [The Reactive Manifesto](https://www.reactivemanifesto.org/)
--->
