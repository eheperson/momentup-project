from elasticsearch import Elasticsearch, helpers
from datetime import datetime
import os
import sys
import pandas as pd
import requests
from faker import Faker
import os
import random
os.system("clear")

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
DATA_STORE_DIR = os.path.join(ROOT_DIR, 'datastore')

ES_HOST = os.environ['ELASTICSEARCH_URL']
print('Elastic host is {}'.format(ES_HOST))

class Elastic:
    def __init__(self, hostURL_="http://localhost:9200"):
        self._elastic = None
        self._connected = None
        #
        self.connect(hostURL_)

    def connect(self,hostURL_):
        es = Elasticsearch([hostURL_])
        # es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        if es.ping():
            # print("Connection Succesfull !")
            self._elastic = es
            self._connected = True
        else:
            # print("Connection Failed !")
            self._elastic = None
            self._connected = False

    @property
    def socket(self):
        return self._elastic
    
    @property
    def connected(self):
        return self._connected
    
    def createIndex(self, indexName_):
        """
            Method to create an index on Elasticsearch
            Check the : GET _cat/indices (from kibana dev-tools)
            Check the : GET <index_name>/_search (from kibana dev-tools)
        """
        if self.connect:
            self._elastic.indices.create(index=indexName_, ignore=[400,404])
        else:
            print("Cannot Create an index !")

    def deleteIndex(self, indexName_):
        """
            Method to delete an index on Elasticsearch
            Check the : GET _cat/indices (from kibana dev-tools)
        """
        if self.connect:
            self._elastic.indices.create(index=indexName_, ignore=[400, 404])
        else :
            print("Cannot delete an index !")

    def allIndices(self):
        """
            It returns  all indices in elasticsearch
        """
        names = []
        if self.connect:
            res = self._elastic.indices.get_alias("*")
            for name in res:
                names.append(name)
            #
            # indices=self.elastic.indices.get_alias().keys()
            # for name in indices:
                # print(name)
            #
            return names
        else:
            print("There are some errors ...... :(")
            return False

    def deleteAll(self):
        """
            Method to delete all indices in elasticsearch
        """
        indices=self._elastic.indices.get_alias().keys()
        for name in indices:
            print("Deleted {} ".format(name))
            self._elastic.indices.delete(index=name, ignore=[400, 404])

    def checkIndex(self, indexName_):
        """
            Method to check if the index given is created
            returns true if index exists
        """
        indexExists = True
        allIndices = self.allIndices()
        if indexName_ not in allIndices:
            indexExists = False
        return indexExists

    def createRecord(self, indexName_, jsonData_, docType_="_doc"):
        #TODO add the code to handle  this: "the index you gicen does not exist, do you want to create it?"
        """
            Method to create data on Elasticsearch DB
        """
        indexStatus = self.checkIndex(indexName_)
        dataStored = True
        #
        try:
            if indexStatus:
                res = self._elastic.index(index=indexName_, doc_type=docType_, body=jsonData_)
                print("RES1 : {}".format(res))
        except Exception as e:
            print('Cannot indexing data')
            print(str(e))
            dataStored = False
        finally:
            return dataStored
    
    def byGenerator(self, generator_):
        """
            Method to create records on the Elasticsearch by generators or dict type data structures
        """
        try:
            res = helpers.bulk(self._elastic, generator_)
            print(res)
            print("Great Job !")
        except Exception as e:
            print(e)

    def search(self, indexName_, jsonData_):
        """
            Method to handle search queries on Elasticsearch
        """
        if self.connected:
            res = self._elastic.search(index=indexName_, size=0, body=jsonData_)
            return res

def createDummyPosts():
    """
        This method is combination of ./lab/createPostData.py and ./lab/loadPostData.py
        It helps to create and load some dummy blog post data to the elastic search
        when the container system builds up.
    """
    elastic = Elastic(ES_HOST)
    fake = Faker()
    indexName = "the_gig"
    docs = []
    #
    elastic.deleteIndex(indexName)
    elastic.createIndex(indexName)
    #
    postCount = 100
    postStatus = [
        "Posted", 
        "Draft", 
        "Deleted"
    ]
    headerColumns = [
        'id', 
        'author', 
        'article', 
        'post_date', 
        'content', 
        'status', 
        'like_count', 
        'commnet_count' 
    ]
    #
    settings = {
        "settings":{
            "number_of_shards":1,
            "number_of_replicas":0
        },
        "mappings":{
            "properties":{
                "author":{
                    "type":"text"
                },
                "article":{
                    "type":"text"
                },
                "content":{
                    "type":"text"
                },
                "status":{
                    "type":"text"
                },
            }
        }
    }
    #
    for i in range(postCount):
        id = "p"+str(i+1)
        author = fake.name()
        article = fake.word() + " " + fake.word() + " " + fake.word()
        post_date = fake.date()
        content = fake.text().split("\n")
        content = ''.join(content)
        # print(content)
        # input()
        status = random.choice(postStatus)
        like_count = random.randint(1,100)
        comment_count = random.randint(1,100)
        #
        record = {
            '_index':indexName,
            '_type':'_doc',
            '_id':str(id),
            '_source':{
                "author":str(author),
                "article":str(article),
                "content":str(content),
                "status":str(status)
            }
        }
        docs.append(record)
    #
    elastic.createRecord(indexName, settings)
    elastic.byGenerator(docs)