.PHONY: start-sso
start-sso:
	ansible-playbook -i localhost, sso/deploy.yml -vvv

.PHONY: stop-sso
stop-sso:
	ansible-playbook -i localhost, sso/deploy.yml --tags=remove -e sso_volume_state=absent

.PHONY: rebuild-sso
rebuild-sso: stop-sso start-sso

.PHONY: start-webapp
start-webapp:
	ansible-playbook -i localhost, webapp/deploy.yml -vvv

.PHONY: stop-webapp
stop-webapp:
	ansible-playbook -i localhost, webapp/deploy.yml --tags=remove -e webapp_volume_state=absent

.PHONY: rebuild-webapp
rebuild-webapp: stop-webapp start-webapp

.PHONY: start
start: start-sso start-webapp

.PHONY: stop
stop: stop-webapp stop-sso

.PHONY: rebuild
rebuild: stop start
