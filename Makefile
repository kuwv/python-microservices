.PHONY: start-sso
start-sso:
	ansible-playbook -i localhost, sso/deploy.yml -vvv

.PHONY: stop-sso
stop-sso:
	ansible-playbook -i localhost, sso/deploy.yml --tags=remove -e sso_volume_state=absent

.PHONY: start
start: start-sso

.PHONY: stop
stop: stop-sso