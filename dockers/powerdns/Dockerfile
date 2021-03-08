FROM python:3.9-slim-buster
ARG API_KEY


# Setup powerdns repositories
RUN apt-get update && apt-get install curl gnupg -y
COPY pdns.list /etc/apt/sources.list.d/pdns.list
COPY pdns /etc/apt/preferences.d/pdns

RUN bash -c 'curl https://repo.powerdns.com/CBC8B383-pub.asc | apt-key add -'

# Instal dependencies
RUN apt-get update
RUN apt-get install pdns-server pdns-backend-mysql mariadb-client  -y

# Install python dependencies
WORKDIR /usr/src/app
RUN pip install --upgrade pip && pip install poetry
COPY pyproject.toml ./
RUN poetry install

# Copy files
COPY pdns.conf /etc/powerdns/pdns.conf
RUN echo "api-key=$API_KEY" >> /etc/powerdns/pdns.conf
COPY start.sh ./
COPY cleanup.lua ./cleanup.lua
COPY main.py ./main.py

CMD bash ./start.sh

