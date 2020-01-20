.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo
	@echo Implementing Python Microservices with OpenID-Connect/OAuth2
	@echo
	@fgrep "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/:.*## / - /'
	@echo

.PHONY: start-sso
start-sso: ## Start SSO instances
	ansible-playbook -i localhost, sso/deploy.yml

.PHONY: stop-sso
stop-sso: ## Stop SSO instances
	ansible-playbook -i localhost, sso/deploy.yml --tags=remove -e sso_volume_state=absent

.PHONY: rebuild-sso
rebuild-sso: stop-sso start-sso ## Rebuild SSO instances

.PHONY: start-webapp 
start-webapp: ## Start webapp instance
	pushd sso-webapp && pipenv lock -r > requirements.txt && popd
	ansible-playbook -i localhost, sso-webapp/deploy.yml

.PHONY: stop-webapp
stop-webapp: ## Stop webapp instance
	ansible-playbook -i localhost, sso-webapp/deploy.yml --tags=remove -e webapp_volume_state=absent

.PHONY: rebuild-webapp
rebuild-webapp: stop-webapp start-webapp ## Rebuild webapp instance

.PHONY: start
start: start-sso start-webapp ## Start all stack components

.PHONY: stop
stop: stop-webapp stop-sso ## Stop all stack components

.PHONY: rebuild
rebuild: stop start ## Rebuild all stack components
