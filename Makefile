.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo
	@echo Implementing Python Microservices with OpenID-Connect/OAuth2
	@echo
	@fgrep "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/:.*## / - /'
	@echo

.PHONY: lint-yaml
lint-yaml:  ## Perform YAML lint
	yamllint .

.PHONY: lint-ansible
lint-ansible:  ## Perform Ansible lint
	ansible-lint **/*.yml

.PHONY: lint
lint: lint-ansible lint-yaml  ## Peform lint

.PHONY: start-sso
start-sso:  ## Start SSO instances
	ansible-playbook -i localhost, sso/deploy.yml

.PHONY: stop-sso
stop-sso:  ## Stop SSO instances
	ansible-playbook -i localhost, sso/deploy.yml --tags=remove -e sso_volume_state=absent

.PHONY: rebuild-sso
rebuild-sso: stop-sso start-sso  ## Rebuild SSO instances

.PHONY: start-webapp 
start-webapp:  ## Start webapp instance
	pushd sso-webapp && pipenv lock -r > requirements.txt && popd
	ansible-playbook -i localhost, sso-webapp/deploy.yml

.PHONY: stop-webapp
stop-webapp:  ## Stop webapp instance
	ansible-playbook -i localhost, sso-webapp/deploy.yml --tags=remove -e webapp_volume_state=absent

.PHONY: rebuild-webapp
rebuild-webapp: stop-webapp start-webapp  ## Rebuild webapp instance

.PHONY: start-webui
start-webui:  ## Start webui instance
	ansible-playbook -i localhost, webui/deploy.yml

.PHONY: stop-webui
stop-webui:  ## Stop webapp instance
	ansible-playbook -i localhost, webui/deploy.yml --tags=remove

.PHONY: rebuild-webui
rebuild-webui: stop-webui start-webui  ## Rebuild webui instance

.PHONY: start
start: start-sso start-webapp start-webui  ## Start all stack components

.PHONY: stop
stop: stop-webui stop-webapp stop-sso  ## Stop all stack components

.PHONY: clean
clean: stop  ## Stop and Clean environment
	rm -rf sso-webapp/static/
	rm -rf sso-webapp/ui/{dist,node_modules}
	rm -rf webui/nginx/app-shell/node_modules

.PHONY: rebuild
rebuild: clean start  ## Rebuild all stack components
