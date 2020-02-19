# -*- mode: ruby -*-
# vi: set ft=ruby :


$base = <<~BASE
  yum update -y
  yum install epel-release -y
  yum install gcc kernel-devel kernel-headers dkms make bzip2 perl -y
  yum install git vim-enhanced jq ansible -y
BASE

$docker = %Q(
  yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
  yum install yum-utils device-mapper-persistent-data lvm2 -y
  yum install docker-ce python-docker -y

  sudo sed -i "s|-H\s*fd://\s*||g" /usr/lib/systemd/system/docker.service
  systemctl daemon-reload

  cat > /etc/docker/daemon.json <<-DAEMON
	{
	  "hosts": ["unix:///var/run/docker.sock", "tcp://127.0.0.1:2375"]
	}
	DAEMON

  if ! getent group docker > /dev/null 2>&1
  then
    groupadd docker
  fi

  if ! id -nG vagrant | grep -q docker
  then
    usermod -aG docker vagrant
  fi

  if ! systemctl is-enabled docker.service >/dev/null 2>&1
  then
    systemctl enable docker
  fi

  if ! systemctl is-active docker.service >/dev/null 2>&1
  then
    systemctl start docker
  fi
)

$python = <<~PYTHON
  yum install gcc python36 python36-devel python36-setuptools -y
  /usr/bin/python3.6 -m ensurepip
  sudo -u vagrant -s /usr/bin/pip3.6 install --user pipenv
PYTHON

$npm = %Q(
  yum install centos-release-scl-rh -y
  yum install rh-nodejs10 -y
  cat > /etc/profile.d/npm.sh <<-NPM
	#!/bin/bash
	source /opt/rh/rh-nodejs10/enable
	export X_SCLS="`scl enable rh-nodejs10 'echo $X_SCLS'`"
	NPM
  scl enable rh-nodejs10 'npm install @vue/cli @vue/cli-service-global -g'
)

Vagrant.configure('2') do |config|
  if Vagrant::Util::Platform.linux? then
    interface = 'virbr0'
  elsif Vagrant::Util::Platform.darwin? then
    interface = 'en0: Wi-Fi (AirPort)'
  end

  config.vm.hostname = "sso-stack"
  # config.vagrant.plugins = 'vagrant-libvirt'
  if Vagrant.has_plugin?('vagrant-libvirt')
    config.vm.box = 'centos/7'
    config.vm.define "sso-stack" do |config|
      config.vm.network 'public_network',
        type: 'bridge',
        mode: 'bridge',
        dev: "#{interface}"

      config.vm.provider "libvirt" do |lv|
        lv.memory = 1024
        lv.cpus = 1
      end

      config.vm.synced_folder './', '/vagrant', type: 'rsync'
    end
  else
    config.vm.box = 'bento/centos-7'
    config.vm.provider :virtualbox do |vb|
      vb.customize ['modifyvm', :id, '--natdnshostresolver1', 'on']
    end
    config.vm.network 'public_network', bridge: "#{interface}"
  end

  # Proxy
  config.vm.network 'forwarded_port', guest: 80, host: 80
  config.vm.network 'forwarded_port', guest: 443, host:443
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

  # if File.exist?("~/.gitconfig")
  config.vm.provision "file", source: "~/.gitconfig", destination: ".gitconfig"
  # end

  config.vm.provision 'base', type: 'shell', inline: $base
  config.vm.provision 'docker', type: 'shell', inline: $docker
  config.vm.provision 'python', type: 'shell', inline: $python
  config.vm.provision 'npm', type: 'shell', inline: $npm

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

  config.trigger.after :up do |trigger|
    trigger.ignore = [:destroy, :halt, :package]
    trigger.ruby do
      system('open', 'http://localhost:8000/webapp/token')
    end
  end
end
