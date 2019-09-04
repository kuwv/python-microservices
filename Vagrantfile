# -*- mode: ruby -*-
# vi: set ft=ruby :

$base = <<-BASE
  yum update -y
  yum install epel-release git vim-enhanced jq -y
BASE

$python = <<-PYTHON
  yum install python36 python36-devel python36-setuptools -y
  /usr/bin/python3.6 -m ensurepip
  /usr/local/bin/pip3.6 install pipenv
PYTHON

$docker = <<-DOCKER
  yum install docker -y

  if ! getent group docker > /dev/null 2>&1
  then
    groupadd docker
  fi

  if ! id -nG vagrant | grep -q docker
  then
    usermod -aG docker vagrant
  fi

  if ! grep OPTIONS /etc/sysconfig/docker | grep -q tcp://.*:2375
  then
    sed -i "s|OPTIONS='|OPTIONS='-H tcp://127.0.0.1:2375 |g" /etc/sysconfig/docker
  fi

  if ! grep OPTIONS /etc/sysconfig/docker | grep -q unix://.*/docker.sock
  then
    sed -i "s|OPTIONS='|OPTIONS='-H unix://var/run/docker.sock |g" /etc/sysconfig/docker
  fi

  if ! systemctl is-enabled docker.service >/dev/null 2>&1
  then
    systemctl enable docker
  fi

  if ! systemctl is-active docker.service >/dev/null 2>&1
  then
    systemctl start docker
  fi
DOCKER

$ansible = <<-ANSIBLE
  # /usr/local/bin/pip3.6 install ansible docker docker-compose
  yum install ansible python-docker python2-pip -y
ANSIBLE

Vagrant.configure("2") do |config|
  config.vm.box = "bento/centos-7"

  config.vm.network "private_network", ip: "192.168.122.10"
  config.vm.network "forwarded_port", guest: 8000, host: 8000
  config.vm.network "forwarded_port", guest: 8001, host: 8001
  config.vm.network "forwarded_port", guest: 8180, host: 8180
  config.vm.network "forwarded_port", guest: 8443, host: 8443
  config.vm.network "forwarded_port", guest: 8444, host: 8444

  config.vm.provision "base", type: "shell", inline: $base
  config.vm.provision "python", type: "shell", inline: $python
  config.vm.provision "docker", type: "shell", inline: $docker
  config.vm.provision "deploy", type: "shell", inline: $ansible

  config.vm.provision "provision", type: "ansible_local" do |ansible|
    ansible.playbook = "sso/deploy.yml"
  end

  config.trigger.after :provision do |trigger|
    trigger.ignore = [:up, :destroy, :halt, :package]
    trigger.ruby do
      system("open", "http://localhost:8000/mock")
    end
  end
end
