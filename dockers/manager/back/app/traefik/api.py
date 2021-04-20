import requests


ROOT = "http://127.0.0.1:8080/api"


def get_from_api(path):
    return requests.get(f"{ROOT}{path}").json()