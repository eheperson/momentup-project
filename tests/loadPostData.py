import os
import pandas as pd
from utils import Elastic, DATA_STORE_DIR

elastic = Elastic()
indexName = 'the_gig'

blogPosts = os.path.join(DATA_STORE_DIR, "blog_posts.csv")
dfRaw = pd.read_csv(blogPosts)
df = dfRaw.copy()

csvHeaders = df.columns
# id,
# author,
# article,
# post_date,
# content,
# status,
# like_count,
# commnet_count

df = df.dropna()
df = df.to_dict('records')


def generator(df_):
    """
        To the purpose of the create a record in Elasticsearch,
        we have to convert our data to ELK format,
        this function helper to convert our data to ELK.
    """
    doc = []
    for c, line in enumerate(df_):
        record = {
            '_index':'the_gig',
            '_type':'_doc',
            '_id':line.get("id", c),
            '_source':{
                "author":line.get("author", ""),
                "article":line.get("article", ""),
                "content":line.get("content", ""),
                "status":line.get("status", "")
            }
        }
        doc.append(record)
    
    return doc
#

# Before sending a record to Elasticsearch, we have to send settings

settings1 = {
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
settings2 = {
    "settings":{
        "analysis": {
        "filter": {
            "autocomplete_filter": {
            "type": "edge_ngram",
            "min_gram": 1,
            "max_gram": 10
            }
        },
        "analyzer": {
            "autocomplete": { 
                "type": "custom",
                "tokenizer": "standard",
                "filter": [
                    "lowercase",
                    "autocomplete_filter"
                ]
            }
        }
        },
        "number_of_shards":1,
        "number_of_replicas":0
    },
    "mappings":{
        "properties":{
            "author":{
                "type":"text",
                "analyzer": "autocomplete", 
                "search_analyzer": "standard" 
            },
            "article":{
                "type":"text",
                "analyzer": "autocomplete", 
                "search_analyzer": "standard" 
            },
            "content":{
                "type":"text",
                "analyzer": "autocomplete", 
                "search_analyzer": "standard" 
            },
            "status":{
                "type":"text",
                "analyzer": "autocomplete", 
                "search_analyzer": "standard" 
            },
        }
    }
}
elastic.deleteIndex(indexName)
elastic.createIndex(indexName)
elastic.createRecord(indexName, settings2)
record = generator(df)
elastic.byGenerator(record)