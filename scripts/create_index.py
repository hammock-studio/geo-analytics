import os
from elasticsearch import Elasticsearch

# index data from twitter, design the mapping/setting
 es = Elasticsearch(os.environ['ES_URL'])
