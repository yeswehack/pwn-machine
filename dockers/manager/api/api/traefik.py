import requests


class Traefik:
    def __init__(self):
        pass

    def get(self, path):
        path = path.lstrip("/")
        r = requests.get(f"{self.root}/{path}")
        print(r)
        return r.json()

    def init_app(self, app):
        self.root = app.config["TRAEFIK_API_URL"].rstrip("/")

    def get_all(self, key):
        all_entries = []
        for typ in ["http", "tcp", "udp"]:
            entries = self.get(f"/api/{typ}/{key}")
            entries = list(map(lambda entry: {**entry, "type": typ}, entries))
            all_entries += entries
        return all_entries

    def services(self):
        return self.get_all("services")

    def routers(self):
        return self.get_all("routers")

    def entrypoints(self):
        entrypoints = self.get("/api/entrypoints")
        return entrypoints

    def middlewares(self):
        return self.get("/api/http/middlewares")