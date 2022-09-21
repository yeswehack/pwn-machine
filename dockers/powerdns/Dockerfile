FROM ubuntu:20.04
ARG API_KEY
# Setup powerdns repositories
RUN apt-get update && apt-get install curl gnupg dnsutils rsyslog -y
COPY pdns.list /etc/apt/sources.list.d/pdns.list
COPY pdns /etc/apt/preferences.d/pdns

RUN bash -c 'curl https://repo.powerdns.com/CBC8B383-pub.asc | apt-key add -'

# Instal dependencies
RUN apt-get update
RUN apt-get install pdns-server pdns-backend-mysql mariadb-client  -y


# Copy files
COPY pdns.conf /etc/powerdns/pdns.conf
COPY 00-pdns.conf /etc/rsyslog.d/00-pdns.conf
RUN echo "\napi-key=$API_KEY" >> /etc/powerdns/pdns.conf
COPY start.sh ./
EXPOSE 53/tcp 53/tcp 8081/tcp

CMD bash ./start.sh

