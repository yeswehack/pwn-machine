FROM bitk/pm_templater as build
ARG PM_DOMAINS
ARG PDNS_API_KEY
ENV PM_DOMAINS ${PM_DOMAINS}
ENV PM_PDNS_API_KEY ${PDNS_API_KEY}
COPY pdns.conf.tpl domain.sql.tpl ./
RUN python main.py pdns.conf.tpl pdns.conf
RUN python main.py domain.sql.tpl domain.sql

FROM ubuntu:latest
RUN apt-get update
RUN apt-get install pdns-server pdns-backend-mysql mariadb-client curl -y
COPY --from=build domain.sql ./
COPY --from=build pdns.conf /etc/powerdns/
COPY start.sh ./
CMD bash start.sh

