# PwnMachine

PwnMachine is a self hosting solution based on docker aiming to provide an easy to use pwning station for bughunters.

The basic install include a DNS server, a reverse proxy and a webserver.


## Requirements

#### On your home computer

* docker-machine
* sshfs (optional)
* python3

You need to create a docker-machine for your server.
 
```shell
docker-machine create \ 
 --driver generic \
 --generic-ip-address=0.0.0.0 \
 --generic-ssh-user=root \
 --generic-ssh-key=/home/user/.ssh/id_rsa \
 your_machine_name
```

For more information: https://docs.docker.com/machine/drivers/generic/


#### On your server

required available port:
* tcp: `80` `443` `53`
* udp: `53`

On a fresh Ubuntu server installation systemd listen on port 53 you will need to shut the service down and change your dns.

```bash
systemctl disable --now systemd-resolved.service
echo "nameserver 208.67.222.222" > /etc/resolv.conf #opendns servers
```

#### DNS

You must set your host as your authoritative nameserver.
You must wait for the DNS propagation or the domain verification by let's encrypt will fail.


## Installation

First install the pm client.
```shell
pip install pwn-machine
```

On your first run you need to setup PwnMachine with

```shell
pm setup
```

Then you can build and start all your services.
```shell
pm service build
pm service start
```

This will start an interactive installer. The installer will create the configuration directory and add the required environment variable and autocompletion to your shell init file.



Check the [wiki](https://github.com/yeswehack/pwn-machine/wiki) for more informations.
