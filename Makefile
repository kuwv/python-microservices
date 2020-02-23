.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo
	@echo Implementing Python Microservices with OpenID-Connect/OAuth2
	@echo
	@fgrep "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/:.*## / - /'
	@echo

.PHONY: lint-yaml
lint-yaml: ## Perform YAML lint
	yamllint .

.PHONY: lint-ansible
lint-ansible: ## Perform Ansible lint
	ansible-lint **/*.yml

.PHONY: lint
lint: lint-ansible lint-yaml ## Peform lint

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

.PHONY: start-proxy
start-proxy: ## Start proxy instance
	ansible-playbook -i localhost, app-shell/deploy.yml

.PHONY: stop-proxy
stop-proxy: ## Stop webapp instance
	ansible-playbook -i localhost, app-shell/deploy.yml --tags=remove

.PHONY: rebuild-proxy
rebuild-proxy: stop-proxy start-proxy ## Rebuild proxy instance

.PHONY: start
start: start-sso start-webapp start-proxy ## Start all stack components

.PHONY: stop
stop: stop-proxy stop-webapp stop-sso ## Stop all stack components

.PHONY: clean
clean: stop ## Stop and Clean environment
	rm -rf sso-webapp/static/
	rm -rf sso-webapp/ui/{dist,node_modules}

.PHONY: rebuild
rebuild: clean start ## Rebuild all stack components
