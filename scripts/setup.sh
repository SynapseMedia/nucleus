#!/usr/bin/env bash
#Zorrillos#00Dev
#ssh root@167.71.11.115
apt-get -yqq update
apt-get remove docker docker-engine
apt-get install curl
apt-get install python-software-properties
apt-get install build-essential
apt-get install software-properties-common
apt-get install apt-transport-https ca-certificates

#Install docker
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
apt-key fingerprint 0EBFCD88
add-apt-repository  "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

apt-get -yqq update
apt-get install docker-ce

#Install compose
curl -L --fail https://github.com/docker/compose/releases/download/1.26.2/run.sh > /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
# Linux, “failed to sufficiently increase receive buffer size”
sysctl -w vm.max_map_count=262144

#Env directory
touch .env
chmod +x .env

##Init compose
docker rmi $(docker images -q)
docker volume rm $(docker volume ls -qf dangling=true)
docker-compose down --rmi all

wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"

#sudo docker-compose exec watchit_certbot sh run.sh
#sudo docker-compose exec watchit_certbot sh certbot certonly --authenticator standalone --preferred-challenges http --noninteractive -d marketplace.watchitapp.site -d web.watchitapp.site -d watchitapp.site --force-renewal

