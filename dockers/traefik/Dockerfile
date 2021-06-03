FROM traefik:latest
ARG LETS_ENCRYPT_EMAIL
COPY traefik.toml /etc/traefik/traefik.toml
RUN sed -i -e "s/__EMAIL__/${LETS_ENCRYPT_EMAIL}/g"  /etc/traefik/traefik.toml
CMD sh -c "echo 'set traefik 1' | nc redis 6379 && traefik"
