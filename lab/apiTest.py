
import requests
import json

HOST_URL = "http://localhost:5000"
INDEX_NAME = "the_gig"

payload={
    "index": "the_gig", 
    "author": "me", 
    "article": "NO",
    "content": "We did it!asdasdasdasdasdasdasdasdasd",
    "status": "DRAFT",
}
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

# Create Post
r = requests.post(HOST_URL+"/create" , data=json.dumps(payload), headers=headers)
print(r)

# Autocomplete
payload={
    "query": "se",
}
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

# Create Post
r = requests.get(HOST_URL+"/autocomplete" , data=json.dumps(payload), headers=headers)
print(r.content)
