import os
import sys
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
from rest import(
    es,
    PostAutocomplete,
    PostCreate,
    PostSearch
)
from utils import createDummyPosts

# -----------------------------------------------------------------------------------------------------
# Application Settings
app = Flask(__name__)
api = Api(app)
# -----------------------------------------------------------------------------------------------------


# -----------------------------------------------------------------------------------------------------
# Backend RestAPI Management
api.add_resource(PostSearch,'/search')
api.add_resource(PostAutocomplete, '/autocomplete')
api.add_resource(PostCreate, '/create')
# -----------------------------------------------------------------------------------------------------


# -----------------------------------------------------------------------------------------------------
# Frontend Management
@app.route('/')
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
    createDummyPosts()
    app.run(host="0.0.0.0", debug=True)
# -----------------------------------------------------------------------------------------------------

