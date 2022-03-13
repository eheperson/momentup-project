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
from datetime import datetime
import os
import sys
import requests


es_host = os.environ['ELASTICSEARCH_URL']
print('Elastic host is {}'.format(es_host))

app = Flask(__name__)
api = Api(app)

es = Elasticsearch([es_host])
NODE_NAME = 'the_gig'

class PostSearch(Resource):
    def __init__(self):
        self.query = parser.parse_args().get("query", None)
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
    def get(self):
        res = es.search(index=NODE_NAME, size=0, body=self.baseQuery)
        return res
parser = reqparse.RequestParser()
parser.add_argument("query", type=str, required=True, help="query parameter is Required ")
api.add_resource(PostSearch, '/autocomplete')
#
@app.route('/pipe', methods=["GET", "POST"])
def pipe():
    data = request.form.get("data")
    payload = {}
    headers= {}
    url = "http://localhost:5000/autocomplete?query="+str(data)
    response = requests.request("GET", url, headers=headers, data = payload)
    return response.json()


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

if __name__ == '__main__':
	app.run(host="0.0.0.0", debug=True)

