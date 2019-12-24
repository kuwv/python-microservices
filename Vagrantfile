# -*- mode: ruby -*-
# vi: set ft=ruby :


$base = <<-BASE
  yum update -y
  yum install epel-release -y
  yum install git vim-enhanced jq ansible -y
BASE

$docker = <<-DOCKER
  yum install docker docker-devel python-docker -y

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

$python = <<-PYTHON
  yum install gcc python36 python36-devel python36-setuptools -y
  /usr/bin/python3.6 -m ensurepip
  /usr/bin/pip3.6 install pipenv
PYTHON

Vagrant.configure('2') do |config|
  if Vagrant::Util::Platform.linux? then
    interface = 'virbr0'
  elsif Vagrant::Util::Platform.darwin? then
    interface = 'en0: Wi-Fi (AirPort)'
  end

  # config.vagrant.plugins = 'vagrant-libvirt'
  if Vagrant.has_plugin?('vagrant-libvirt')
    config.vm.box = 'centos/7'

    config.vm.define "sso-stack" do |config|
      config.vm.hostname = "sso-stack"

      config.vm.network 'public_network',
        type: 'bridge',
        mode: 'bridge',
        dev: 'virbr0'

      config.vm.provider "libvirt" do |lv|
        lv.memory = 1024
        lv.cpus = 1
      end
    end
  else
    config.vm.provider :virtualbox do |vb|
      vb.customize ['modifyvm', :id, '--natdnshostresolver1', 'on']
    end
    config.vm.network 'public_network', bridge: $interface
  end

  # Development
  config.vm.network 'forwarded_port', guest: 3000, host: 3000
  # Kong Public
  config.vm.network 'forwarded_port', guest: 8000, host: 8000
  config.vm.network 'forwarded_port', guest: 8443, host: 8443
  # Kong Management
  config.vm.network 'forwarded_port', guest: 8001, host: 8001
  config.vm.network 'forwarded_port', guest: 8444, host: 8444
  # KeyCloak
  config.vm.network 'forwarded_port', guest: 8080, host: 8080

  config.ssh.forward_agent = true

  config.vm.provision 'base', type: 'shell', inline: $base
  config.vm.provision 'docker', type: 'shell', inline: $docker
  config.vm.provision 'python', type: 'shell', inline: $python

  config.vm.provision 'setup', type: 'ansible_local' do |ansible|
    ansible.playbook = 'deploy.yml'
    ansible.verbose = true
  end

  config.vm.provision 'remove', type: 'ansible_local', run: 'never' do |ansible|
    ansible.playbook = 'deploy.yml'
    ansible.tags = 'remove'
    ansible.extra_vars = {
      sso_purge_volumes: true
    }
  end 

  config.trigger.after :provision do |trigger|
    trigger.ignore = [:destroy, :halt, :package]
    trigger.ruby do
      system('open', 'http://localhost:8000/webapp/token')
    end
  end
end
