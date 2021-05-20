from elasticsearch import AsyncElasticsearch
from app import config

ES_HOSTS = [config.PM_ELASTIC_SEARCH_HTTP_API]

es = AsyncElasticsearch(ES_HOSTS)
