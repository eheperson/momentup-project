#  T H I S  # # # # # # # # # # # # # # # # # # # # # 
# # # # F I L E # # # # # # # # # # # # # # # 
#  I S   N O T # # # # # # # # # # # # # # # 
# # # # R U N A B L E # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # #  D O   N O T   R U N   I T # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # 
#   O N L Y   F O R   T A K I N G   N O T E S # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 


hostURL = "http//:localhost:9200"
es = Elasticsearch(timeout=60, host=hostUrl)



for f in os.listdir():
    print(f)
csvFile = ""
df = pd.read_csv(csvFile)
print(df.head(10))
print(df.columns)
print(df.shape)
df.isna()
df.isna().sum()
df.dropna()



### Cold be useful for autocomplete:
res =  es.indices.get_alias("*")
for Name in res:
    print(Name)
#
query={"query" : {
    "match_all" : {}
}}
res = es.search(index="person", body=query, size=1000)