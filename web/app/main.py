import os
import sys
from flask import (
    Flask, 
    url_for, 
    jsonify, 
    render_template,
    request,
    redirect,
    flash
)
from flask_restful import (
    Resource, 
    Api, 
    reqparse
)
from numpy import rec
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
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
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
def es_info():
	return jsonify(es.socket.info())

@app.route('/health')
def es_health():
    return jsonify(es.socket.cluster.health())

@app.route('/api_create', methods=['POST','GET'])
def api_create():
    if request.method ==  "POST":
        index = request.form["index"]
        author = request.form["author"]
        article = request.form["article"]
        content = request.form["content"]
        status = request.form["status"]
        record={
            "author":author,
            "article":article,
            "content": content,
            "status": status,
        }
        postCreated = es.createRecord(indexName_=index, jsonData_=record)
        print(index, author, article, content, status, file=sys.stderr)
        print(postCreated, file=sys.stderr)
        if postCreated:
            flash('Post Created, You can check it from autocomplete by typing : {}'.format(author))
        else :
            flash('Post Cannot Created')
            
        return render_template('create.html')
        # return redirect(request.url)
    else:
        return render_template('create.html')


# -----------------------------------------------------------------------------------------------------


# -----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    createDummyPosts()
    app.run(host="0.0.0.0", debug=True)
# -----------------------------------------------------------------------------------------------------

