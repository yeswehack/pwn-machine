from .utils import slugify



def get_traefik_rules(service_name, http_config, ssl=False):
    labels = {}
    port = http_config["port"]
    labels["traefik.enable"] = "true"
    labels["traefik.docker.network"] = "traefik"

    r = "traefik.http.routers"
    s = "traefik.http.services"
    m = "traefik.http.middlewares"
    for domain_name, domain in http_config["domains"].items():
        router_name = f"{service_name}-{slugify(domain_name)}"
        if domain_name.startswith("*."):
            # for wildcard, set minimal priority and ask for *.name certificate
            top_domain = domain_name[2:]
            labels[f"{r}.{router_name}.priority"] = "1"
            labels[
                f"{r}.{router_name}.rule"
            ] = f"HostRegexp(`{top_domain}`, `{{subdomain:.*}}.{top_domain}`)"
            if ssl:
                labels[f"{r}.{router_name}.tls.domains[0].main"] = top_domain
                labels[f"{r}.{router_name}.tls.domains[0].sans"] = domain_name
        else:
            labels[f"{r}.{router_name}.rule"] = f"Host(`{domain_name}`)"

        if ssl:
            labels[f"{r}.{router_name}.entrypoints"] = "https"
            labels[f"{r}.{router_name}.tls.certresolver"] = "letsencrypt"
        else:
            labels[f"{r}.{router_name}.entrypoints"] = "http"

        labels[f"{r}.{router_name}.service"] = router_name
        labels[f"{s}.{router_name}.loadbalancer.server.port"] = str(port)

        # middleware
        middlewares = []
        md_name = f"chain-{service_name}-{slugify(domain_name)}"
        

        # IP allow
        md_ial_name = f"al-{service_name}-{slugify(domain_name)}"
        allow_list = ",".join(str(ip) for ip in domain["ip-allow-list"])
        if allow_list:
            labels[f"{m}.{md_ial_name}.ipwhitelist.sourcerange"] = allow_list
            middlewares.append(md_ial_name)

        # BasicAuth
        md_ba_name = f"ba-{service_name}-{slugify(domain_name)}"
        auth_list = ",".join(str(ip) for ip in domain["basic-auth"])
        if auth_list:
            labels[f"{m}.{md_ba_name}.basicauth.users"] = auth_list
            middlewares.append(md_ba_name)

        if middlewares:
            labels[f"{m}.{md_name}.chain.middlewares"] = ",".join(middlewares)
            labels[f"{r}.{router_name}.middlewares"] = f"{md_name}@docker"
    return labels
