# -*- mode: ruby -*-
# vi: set ft=ruby :

#
# Vagrant file for local provisioning
#
Vagrant::configure("2") do |config|

  # download from https://atlas.hashicorp.com/madrid/boxes/ubuntu-14.04-jp
  config.vm.box = "oinume/ubuntu-14.04-jp"
  config.vm.hostname = "dmm-eikaiwa-tsc"

  # MySQL
  #config.vm.network :forwarded_port, guest: 3306, host: 13306

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  config.vm.network :private_network, ip: "192.168.111.222"

  # VM option
  config.vm.provider "virtualbox" do |v|
    v.customize ["modifyvm", :id, "--memory", 384]
    v.customize ["modifyvm", :id, "--cpus", 1]
    v.customize ["modifyvm", :id, "--nictype1", "virtio"]
    v.customize ["modifyvm", :id, "--nictype2", "virtio"]
    v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
  end

  if Vagrant.has_plugin?("vagrant-cachier")
    config.cache.scope = :box
  end

  # If you do not want to install ansible to local machine, Try this
  config.vm.provision :shell do |shell|
    shell.inline = <<"EOS"
echo mysql-server-5.5 mysql-server/root_password password root | debconf-set-selections
echo mysql-server-5.5 mysql-server/root_password_again password root | debconf-set-selections
sudo apt-get update && sudo apt-get install -y mysql-server-5.5
perl -pi -e 's/127.0.0.1/0.0.0.0/g' /etc/mysql/my.cnf
mysql -uroot -proot -e "GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'root'"
sudo service mysql restart
EOS
  end
end
