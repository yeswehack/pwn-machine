# PwnMachine (v2)

PwnMachine is a self hosting solution based on docker aiming to provide an easy to use pwning station for bug hunters.

The basic install include a web interface, a DNS server and a reverse proxy.

## Requirements
To use the PwnMachine, you don't need many prerequisites. You just need to have docker on your machine. We do not provide a tutorial for installing Docker, you can find all the useful information here: [https://docs.docker.com/get-started/](https://docs.docker.com/get-started/).

## Installation

### Using Docker

1. Clone the repository locally on your machine

```bash
git clone https://github.com/yeswehack/pwn-machine.git
```

2. Enter in the repository previously cloned

```
cd pwn-machine/
```

#### Configure the .env

If you start to build direclty the project, you will be faced with an error:

```bash
${LETS_ENCRYPT_EMAIL?Please provide an email for let's encrypt}" # Replace with your email address or create a .env file
```

We highly recommend to create a `.env` file in the PwnMachine directory and to configure an email. It's used for let's encrypt to have a SSL certificate.

```bash
LETS_ENCRYPT_EMAIL="your_email@domain.com"
```

#### Building

1. Build the project (using option `-d` will start the project in background, it's optional). Building can take several minutes (depending on your computer and network connection).

```bash
docker-compose up --build -d
```

2. Once everything is done on docker side, you should be able to access on the PwnMachine at `http://your_address_ip` 

```
Starting pm_powerdns-db_1   ... done
Starting pm_redis_1         ... done
Starting pm_powerdns_1      ... done
Starting pm_filebeat_1      ... done
Recreating traefik          ... done
Recreating pm_manager_1     ... done
```

Check the [wiki](https://github.com/yeswehack/pwn-machine/wiki) for more informations.
