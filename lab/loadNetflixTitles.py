import os
import pandas as pd
from utils import Elastic, DATA_STORE_DIR

elastic = Elastic()
indexName = 'netflix_titles'

netflixTitles = os.path.join(DATA_STORE_DIR, "netflix_titles.csv")
dfRaw = pd.read_csv(netflixTitles)
df = dfRaw.copy()

csvHeaders = df.columns
# show_id,
# type,
# title,
# director,
# cast,
# country,
# date_added,
# release_year,
# rating,
# duration,
# listed_in,
# description

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
            '_index':'netflix_titles',
            '_type':'_doc',
            '_id':line.get("show_id", c),
            '_source':{
                "title":line.get("title", ""),
                "director":line.get("director", ""),
                "description":line.get("title", ""),
                "duration":line.get("duration", None),
                "cast":line.get("cast", "")
            }
        }
        doc.append(record)
    return doc
#

# Before sending a record to Elasticsearch, we have to send settings
settings = {
    "settings":{
        "number_of_shards":1,
        "number_of_replicas":0
    },
    "mappings":{
        "properties":{
            "title":{
                "type":"text"
            },
            "director":{
                "type":"text"
            },
            "description":{
                "type":"text"
            },
            "duration":{
                "type":"text"
            },
            "cast":{
                "type":"text"
            },
        }
    }
}
elastic.deleteIndex(indexName)
elastic.createIndex(indexName)
elastic.createRecord(indexName, settings)
record = generator(df)
elastic.byGenerator(record)