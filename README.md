# Satechi Media Button with Sonos


## Install Node

	curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash
	source /home/pi/.bashrc 
	nvm install 12
	nvm use 12


## Setup Bluetooth connection with Satechi device

	sudo bluetoothctl
	power on
	agent on
	default-agent
	scan on
	pair <:xx:xx:...>

> My device ID was 'DC:2C:26:D1:E1:00' when initially setting up shop.
> You possibly have to trust the device manually. This can be done using the 'trust' command from 'bluetoothctl'.


## Clone Sonos HTTP API

	git clone https://github.com/jishi/node-sonos-http-api.git
	cd node-sonos-http-api
	npm install --production
	npm install -g pm2


## Setup Python

	sudo apt-get update
	sudo apt-get install python-dev python-pip gcc
	sudo apt-get install linux-headers-$(uname -r)
	sudo pip install evdev==1.2.0
	sudo pip install python-daemon

	git clone https://github.com/Voles/BlueSonosButton.git
	cd BlueSonosButton


## Run the scripts

	cd node-sonos-http-api
	NODE_ENV=production pm2 start server.js

	cd BlueSonosButton
	python run.py


## Todo
	
	1. ~~Run the Node and Python commands in the background.~~
	1. ~~Python script should not exit when the bluetooth device disconnects.~~
	1. Restart NPM & Python commands on reboot (https://github.com/Unitech/pm2#startup-scripts-generation).
	1. Loop through favorites when pressing previous/next
	1. Monitor from time to time :-)

## Helpful commands

	kill -11 <pid>
	ps -A | grep python
	tail -f output.log

	pm2 describe <id>
	pm2 list
	pm2 monit
	pm2 stop <id>
	pm2 delete <id>


## Sources

- [Original instructions](https://github.com/SvenSommer/BlueSonosButton)
