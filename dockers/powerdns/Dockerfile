FROM ubuntu:latest
ARG API_KEY
RUN apt-get update
RUN apt-get install pdns-server pdns-backend-mysql mariadb-client curl -y
COPY pdns.conf /etc/powerdns/pdns.conf
COPY start.sh /
RUN echo "api-key=$API_KEY" >> /etc/powerdns/pdns.conf

CMD bash /start.sh

