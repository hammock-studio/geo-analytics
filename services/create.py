import json
from elasticsearch import Elasticsearch

es = Elasticsearch(os.environ['ES_URL'])

def tweets_mapping():
    with open('./config/mappings/tweets.json') as f: # could be generic loader of configuration
        mappings = json.load(f)

    return mappings

def create(recreate=False):
    if recreate:
        print("recreating geo-analytics")
        es.indices.delete(index='geo-analytics')

    if not es.indices.exists(index='geo-analytics'):
        es.indices.create(index='geo-analytics', body=tweets_mapping())
    else:
        print("geo-analytics exists")

create() # access from webpage to run process
