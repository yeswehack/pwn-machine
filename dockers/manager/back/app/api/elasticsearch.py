
from elasticsearch import AsyncElasticsearch


ES_HOSTS = ["127.0.0.1:9200"]

es = AsyncElasticsearch(ES_HOSTS)