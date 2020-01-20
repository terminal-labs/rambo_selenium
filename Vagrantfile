# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|  
  config.vm.box = "selenium"  
  config.vm.box_url = "http://terminal-labs-vagrant-boxes.s3.amazonaws.com/tl_debjesse64.box"

  config.vm.provision :salt do |salt|
    salt.bootstrap_options = "-P"
	  salt.verbose = true
  end

  config.vm.provision "shell", inline: "sudo cp /etc/salt/minion{,-dist} && sudo cp /vagrant/salt/minion /etc/salt/minion && sudo salt-call --local state.highstate"

  config.vm.network :forwarded_port, :guest => 8001, :host => 8001, auto_correct: true
  config.vm.network :forwarded_port, :guest => 8002, :host => 8002, auto_correct: true

  config.vm.network :forwarded_port, :guest => 80, :host => 8080, auto_correct: true

  config.vm.network :private_network, ip: "192.168.33.10"
  config.ssh.forward_agent = true

end
