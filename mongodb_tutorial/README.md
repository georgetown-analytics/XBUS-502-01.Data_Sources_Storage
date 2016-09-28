# tiamat
Pymongo tutorial with NOAA metadata records

In this lab, we will use Pymongo to store [NOAA metadata](https://data.noaa.gov/data.json) records to a database.

![Tiamat](https://github.com/rebeccabilbro/tiamat/blob/master/images/tiamat.jpg)  

_By Internet Archive Book Images [No restrictions], via Wikimedia Commons_

**Please verify you have all installations listed in the 
[Install](https://github.com/nd1/tiamat/blob/master/Install.md) file before proceeding.**

## Install MongoDB
First, install [MongoDB](https://docs.mongodb.org/manual/administration/install-community/).

[__OSX__](https://docs.mongodb.org/manual/tutorial/install-mongodb-on-os-x/)    
```bash
$ brew install mongodb
```

[__Linux__](https://docs.mongodb.org/manual/administration/install-on-linux/)    

[__Windows__](https://docs.mongodb.org/manual/tutorial/install-mongodb-on-windows/)    

## Install Pymongo
Next, make sure you have `pymongo` [installed](https://api.mongodb.org/python/current/installation.html). Type this into your terminal:

```bash
$ python -m pip install pymongo
```

## Clone this repo  

```bash
$ git clone https://github.com/nd1/tiamat.git
$ cd tiamat
```

## Install Jupyter if you don't already have it

```bash
$ pip install jupyter
```

## Launch the Jupyter Notebook

```bash
$ jupyter notebook MongoDBTutorial.ipynb
```


## Basic Commands
```python
import json
import pymongo
from pprint import pprint

conn=pymongo.MongoClient()
db = conn.earthwindfire
records = db.records

with open("data_sample.json") as data_file:    
    noaa = json.load(data_file)

def insert(metadata):
    for dataset in metadata:
        data ={}
        data["title"] = dataset["title"]
        data["description"] = dataset["description"]
        data["keywords"] = dataset["keyword"]
        data["accessLevel"] = dataset["accessLevel"]
        data["lang"] = dataset["language"]
        # choose your own
        # choose your own
        # choose your own
        # choose your own

        records.insert_one(data)

insert(noaa)
# Check to make sure they're all in there
records.count()

# Find
records.find_one()

for rec in records.find()[:2]:
    pprint(rec)

records.find({"keywords": "NESDIS"}).count()

records.find({"keywords": "NESDIS","keywords": "Russia","accessLevel":"public"}).count()

for r in records.find({"keywords": "NESDIS","keywords": "Russia","accessLevel":"public"}):
    pprint(r)

# Limit
cursor = db.records.find({"$where": "this.keywords.length > 100"}).limit(2);
for rec in cursor:
    pprint(rec)

# Full text search
db.records.create_index([('description', 'text')])

cursor = db.records.find({'$text': {'$search': 'precipitation'}})
for rec in cursor:
    print rec

cursor = db.records.find({'$text': {'$search': 'fire'}})
cursor.count()

# Drop text index to create a new one
db.records.drop_index("description_text")

# Create a wildcard index
db.records.create_index([("$**","text")])

cursor = db.records.find({'$text': {'$search': "Russia"}})
for rec in cursor:
    pprint(rec)

# Projections
cursor = db.records.find({'$text': {'$search': "Russia"}}, {"title": 1,"_id":0 })
for rec in cursor:
    print rec

# Limit
cursor = db.records.find({'$text': {'$search': "Russia"}}, {"title": 1,"_id":0 }).limit(2)
for rec in cursor:
    print rec

# Aggregate
cursor = db.records.aggregate(
    [
        {"$group": {"_id": "$lang", "count": {"$sum": 1}}}
    ]
)
for document in cursor:
    pprint(document)

cursor = db.records.aggregate(
    [
        {"$match": {'$text': {'$search': "Russia"}, "accessLevel": "public"}},
        {"$group": {"_id": "$title"}}
    ]
)

for document in cursor:
    pprint(document)

# Remove data
conn.earthwindfire.collection_names()
conn.earthwindfire.drop_collection("records")
conn.earthwindfire.collection_names()

conn.database_names()
conn.drop_database("earthwindfire")
conn.database_names()
```


### If you already know SQL...

The following table provides an overview of common SQL aggregation terms, functions, and concepts and the corresponding MongoDB aggregation operators:    

| SQL Terms, Functions, and Concepts  | MongoDB Aggregation Operators  |
| ----------------------------------  |:-------------------------------|
| WHERE                               | $match                         |
| GROUP BY                            | $group                         |
| HAVING                              | $match                         |
| SELECT	                            | $project                       |
| ORDER BY	                          | $sort                          |
| LIMIT                               | $limit                         |
| SUM()   	                          | $sum                           |
| COUNT()	                            | $sum                           |
| join	                              | $lookup                        |
