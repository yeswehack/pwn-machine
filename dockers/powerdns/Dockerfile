FROM python:3.9-slim-buster
ARG API_KEY

# Setup powerdns repositories
RUN apt-get update && apt-get install curl gnupg dnsutils -y
COPY pdns.list /etc/apt/sources.list.d/pdns.list
COPY pdns /etc/apt/preferences.d/pdns

RUN bash -c 'curl https://repo.powerdns.com/CBC8B383-pub.asc | apt-key add -'

# Instal dependencies
RUN apt-get update
RUN apt-get install pdns-server pdns-recursor pdns-backend-mysql mariadb-client  -y

# Install python dependencies
WORKDIR /usr/src/app
RUN pip install --upgrade pip && pip install poetry
COPY pyproject.toml ./
RUN poetry install

# Copy files
COPY pdns.conf /etc/powerdns/pdns.conf
COPY recursor.conf /etc/powerdns/recursor.conf
COPY bind.conf /etc/powerdns/bind.conf
COPY recursor.lua /etc/powerdns/recursor.lua
RUN echo "\napi-key=$API_KEY" >> /etc/powerdns/pdns.conf
COPY start.sh ./
COPY dnsmessage_pb2.py ./dnsmessage_pb2.py
COPY main.py ./main.py

CMD bash ./start.sh

