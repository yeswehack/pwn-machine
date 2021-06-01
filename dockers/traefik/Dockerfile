FROM traefik:latest
COPY traefik.toml /etc/traefik/traefik.toml
COPY dynamic_conf.toml /etc/traefik/dynamic_conf.toml
CMD sh -c "echo 'set traefik 1' | nc redis 6379 && traefik"
