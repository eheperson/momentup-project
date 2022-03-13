# MOMENTUP Project
Project repo for momentup company

**NOTE**: *The purpose of the `./lab` directory is to testing new updates before applying to the web app and it is totaly seperated form `./web` which is the main directory of this project.*

> **API endpoints are  and there are some extra works including Frontend. Web APP GUI is developed optionally to the purpose of the testing implementation procedure.**

> **You do not need to interact with Frontend, all requested endpoints for this task works fine**

---
## Setup Steps :
```
# clone the repository 
git clone git@github.com:eheperson/momentup-project.git

# change access right of the build.sh file
chmod +x builder.sh

# run the docker
./builder.sh
```

---

## Endpoint Map

### General
* Elasticsearch Endpoint - `http://localhost:9200` : [Click !](http://localhost:9200) 
* Kibana Endpoint - `http://localhost:5601` : [Click !](http://localhost:5601) 
* Web App Endpoint - `http://localhost:5000` : [Click !](http://localhost:5000) 

### Web APP

#### Autocomplete
* Endpoint : `http://localhost:5000/autocomplete`
  * Must Parameters :
    * query     : `'?query='`
    * index     : `'?index='`
  * Allowed Request Methods:
    * POST
  * Example : `http://localhost:5000/autocomplete?index="the_gig"?query="se"`


#### Create
* Endpoint : `http://localhost:5000/create`
  * Must Parameters :
    * index : `'?index='`
    * author : `'?author='`
    * content : `'?content='`
    * status : `'?status='`
    * article : `'?article='`
  * Allowed Request Methods:
    * POST
  * Example : `http://localhost:5000/autocomplete?index="the_gig"?author="me"?content="lorem.."?"status="DRAFT"?article="enivicivokki"`

#### Search
* Endpoint : `http://localhost:5000/search`
  * Must Parameters :
    * index : `'?index='`
  * Optional Parameters :
    * author : `'?author='`
    * content : `'?content='`
    * status : `'?status='`
    * article : `'?article='`
  * Allowed Request Methods:
    * GET
  * Example : `http://localhost:5000/autocomplete?index="the_gig"?author="me"?content="lorem.."?"status="DRAFT"?article="enivicivokki"`
---

## Testing Web App Endpoints

Via Python :
```
    # importing required modules
    import requests
    import json

    HOST_URL = "http://localhost:5000"
    INDEX_NAME = "the_gig"

    # Testing /autocomplete endpoint
    payload={
        "query": "se",
    }
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(HOST_URL+"/autocomplete" , data=json.dumps(payload), headers=headers)
    print(r)
    # print(r.content)


    # Testing /create endpoint
    payload={
        "index": "the_gig", 
        "author": "me", 
        "article": "NO",
        "content": "We did it!asdasdasdasdasdasdasdasdasd",
        "status": "DRAFT",
    }
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(HOST_URL+"/create" , data=json.dumps(payload), headers=headers)
    print(r)
    # print(r.content)


    # Testing /search endpoint
    payload={
        "index": "the_gig", 
        "author": "me", 
        "article": "",
        "content": "",
        "status": "",
    }
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.get(HOST_URL+"/search" , data=json.dumps(payload), headers=headers)
    print(r)
    # print(r.content)

```

## Testing Via Web APP UI

### Autocomplete

* Go to the : localhost:5000/
* type random strign to the search bar

### Create 
* Fill the fields(do not change the_gig, it is default Elasticsearch index name)
* If record creation succeed, there will be alert on the page, you can copy the specified text from the alert and paste it to the `autocomplete` page to check if the record is created by success.



