from flask import (
    Flask, 
    url_for, 
    jsonify, 
    render_template
)
from elasticsearch import Elasticsearch
from datetime import datetime
import os
import sys

if sys.version_info.major < 3:
    reload(sys)


es_host = os.environ['ELASTICSEARCH_URL']
print('Elastic host is {}'.format(es_host))
es = Elasticsearch([es_host])

app = Flask(__name__)

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

