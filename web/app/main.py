from flask import (
    Flask, 
    url_for, 
    jsonify, 
    render_template,
    request
)
from flask_restful import (
    Resource, 
    Api, 
    reqparse

)
from elasticsearch import Elasticsearch
import os
import sys

# -----------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------

es_host = os.environ['ELASTICSEARCH_URL']
print('Elastic host is {}'.format(es_host))

app = Flask(__name__)
api = Api(app)

es = Elasticsearch([es_host])
NODE_NAME = 'the_gig'

# -----------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------

class PostAutocomplete(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("query", type=str, required=True, help="query parameter is Required ")
        self.query = self.parser.parse_args().get("query", None)
        self.baseQuery ={
            "_source": ["author", "content", "status", "article"],
            "query": {
                "bool": {
                    "should": [],
                    "filter": [],
                    "must": [
                        {
                            "match_phrase_prefix": {
                                "content": {
                                    "query": "{}".format(self.query)
                                }
                            }
                        }
                    ],
                    "must_not": []
                }
            },
            "aggs": {
                "auto_complete": {
                    "terms": {
                        "field": "content.keyword",
                        "order": {
                            "_count": "desc"
                        },
                        "size": 10
                    }
                }
            }
        }
    def post(self):
        res = es.search(index=NODE_NAME, size=0, body=self.baseQuery)
        return res

class PostCreate(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("index", type=str, required=True, help="index parameter is Required ")
        self.parser.add_argument("author", type=str, required=True, help="author parameter is Required ")
        self.parser.add_argument("content", type=str, required=True, help="content parameter is Required ")
        self.parser.add_argument("article", type=str, required=True, help="article parameter is Required ")
        self.parser.add_argument("status", type=str, required=True, help="status parameter is Required ")
        #
        self.index = self.parser.parse_args().get("index", None)
        self.content = self.parser.parse_args().get("content", None)
        self.article = self.parser.parse_args().get("article", None)
        self.author = self.parser.parse_args().get("author", None)
        self.status = self.parser.parse_args().get("status", None)
        #
        self.record={
            "author":self.author,
            "article":self.article,
            "content":self.content,
            "status":self.status
        }
    #
    def post(self):
        res = es.index(index=self.index, doc_type="_doc", body=self.record)
        print(res, file=sys.stderr)
#
class PostSearch(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("index", type=str)
        self.parser.add_argument("author", type=str)
        self.parser.add_argument("content", type=str)
        self.parser.add_argument("article", type=str)
        self.parser.add_argument("status", type=str)
        #
        self.index = self.parser.parse_args().get("index","")
        self.content = self.parser.parse_args().get("content", "")
        self.article = self.parser.parse_args().get("article", "")
        self.author = self.parser.parse_args().get("author", "")
        self.status = self.parser.parse_args().get("status", "")
        #
        self.searchQuery ={
            "size":20,
            "query": {
                "bool": {
                    "must":[],
                    "filter":[],
                    "should":[
                        {
                            "match":{
                                "content":{
                                    "query":self.content
                                }
                            }
                        },
                        {
                            "match":{
                                "status":{
                                    "query":self.status
                                }
                            }
                        },
                        {
                            "match":{
                                "article":{
                                    "query":self.article
                                }
                            }
                        },
                        {
                            "match_phrase":{
                                "author":{
                                    "query":self.author
                                }
                            }
                        },
                    ],
                    "must_not":[],
                }
            },

            "aggs":{
                "author":{
                    "terms":{
                        "field":"author.keyword",
                        "order":{
                            "_key":"asc"
                        }
                    }
                },
                "content":{
                    "terms":{
                        "field":"content.keyword",
                        "order":{
                            "_key":"desc"
                        }
                    }
                },
                "status":{
                    "terms":{
                        "field":"status.keyword",
                        "order":{
                            "_key":"desc"
                        }
                    }
                },
                "article":{
                    "terms":{
                        "field":"article.keyword",
                        "order":{
                            "_key":"desc"
                        }
                    }
                },

            }

        }
    def get(self):
        res = es.search(index=self.index, size=0, body=self.searchQuery)
        return res   
api.add_resource(PostSearch,'/search')
api.add_resource(PostAutocomplete, '/autocomplete')
api.add_resource(PostCreate, '/create')

# -----------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------

@app.route('/')
def hello_world():
	return 'Hello From Momentup'

@app.route('/index')
def index():
   return render_template('index.html')

@app.route('/info')
def api_info():
	return jsonify(es.info())

@app.route('/health')
def api_health():
    return jsonify(es.cluster.health())

# -----------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------

if __name__ == '__main__':
	app.run(host="0.0.0.0", debug=True)

