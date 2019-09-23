import json
import os
from elasticsearch import Elasticsearch

es = Elasticsearch()

print ("Deleting all existing elasticsearch data")
es.indices.delete("articles", ignore=404)

mapping = '''
{  
  "settings": {
    "number_of_replicas": 0,
    "number_of_shards": 1
  },
  "mappings": {  
    "properties": {
      "author": {
        "type": "text",
        "index": false
      },
      "body": {
        "type": "text"
      },
      "description": {
        "type": "text"
      },
      "id": {
        "type": "text"
      },
      "imgurl": {
        "type": "text",
        "index": false
      },
      "score": {
        "type": "long",
        "index": false
      },
      "tags": {
        "type": "keyword"
      },
      "timestamp": {  
        "type":"date"
      },
      "title": {
        "type":"text"
      },
      "url": {
        "type":"text",
        "index": false
      }
    }
  }
}'''
print ("Creating Indices")
es.indices.create(index="articles", body=mapping)