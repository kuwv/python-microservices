# Microservices with Python


## Index

* [ License ](LICENSE.md)
1. [SSO setup - Using Ansible to deploy KeyCloak / Kong](./sso/README.md)
2. [Webapp setup - Setup web application to auth to KeyCloak](./webapp/README.md)


## Synopsis

This project is intended as a starting point for creating microserices using Python.


## Description


## Setup

### Using Vagrant

Start VM with application
```
vagrant up --provision-with
```

Removing application from VM
```
vagrant up --provision-with remove
```

Login
```
vagrant ssh -- -A
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


## See also

- [The Twelve-Factor App](https://12factor.net/)
- [The Reactive Manifesto](https://www.reactivemanifesto.org/)
