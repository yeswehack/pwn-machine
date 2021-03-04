from flask import Flask, Blueprint, jsonify, send_from_directory
import docker
from api import Traefik, DNS
import auth
from flask_redis import FlaskRedis
from flask_cors import CORS
from flask_socketio import SocketIO
import os


docker_client = docker.from_env()
redis_client = FlaskRedis()
traefik_client = Traefik()
dns_client = DNS()
socketio = SocketIO(cors_allowed_origins="*")



def create_app():
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config["SECRET_KEY"] = "test"
    app.config["TRAEFIK_REDIS_ROOK_KEY"] = "traefik"
    app.config["TRAEFIK_API_URL"] = os.environ.get("TRAEFIK_API_URL", "http://traefik:8080")
    app.config["REDIS_URL"] = os.environ.get("REDIS_URL", "redis://redis:6379/0")
    app.config["DNS_API_URL"] = os.environ.get("DNS_API_URL", "http://powerdns:8081")
    app.config["DNS_API_TOKEN"] = os.environ.get("DNS_API_TOKEN", "test")
    app.config["CORS_EXPOSE_HEADERS"] = "*"
    redis_client.init_app(app)
    traefik_client.init_app(app)
    dns_client.init_app(app)
    socketio.init_app(app)
    auth.init_app(app)
    CORS(app)

    @app.route("/<path:path>")
    def static_front(path):
        return send_from_directory("static", path)

    from blueprints import blueprints

    for prefix, bp in blueprints.items():
        app.register_blueprint(bp, url_prefix=f"/api{prefix}")

    return app
