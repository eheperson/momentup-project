from utils import Elastic, ROOT_DIR, DATA_STORE_DIR

ES_URL = "http://localhost:9200"
elastic = Elastic(ES_URL)
print("Elasticsearch connection status : {}".format("Succesfull" if elastic.connected else "Failed"))
#
indexName = "test-index"
elastic.createIndex(indexName)
# elastic.deleteIndex(indexName)
#
e1={
    "first_name":"Soumil",
    "last_name":"Shah",
    "age": 24,
    "about": "Full stack Software Developers ",
    "interests": ['Youtube','music'],
}
e2={
    "first_name":"nitin",
    "last_name":"Shah",
    "age": 58,
    "about": "Soumil father ",
    "interests": ['Stock','Relax'],
}
#
elastic.createRecord(indexName_=indexName, jsonData_=e1)
elastic.createRecord(indexName_=indexName, jsonData_=e2)



