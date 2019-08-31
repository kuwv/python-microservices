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
  yum install ansible python2-pip -y
  pip install docker docker-compose
ANSIBLE

Vagrant.configure("2") do |config|
  config.vm.box = "bento/centos-7"

  config.vm.synced_folder "projects", "/home/vagrant/projects", type: "virtualbox"

  config.vm.provision "shell", inline: $base
  config.vm.provision "shell", inline: $python
  config.vm.provision "shell", inline: $docker
  config.vm.provision "shell", inline: $ansible
end
