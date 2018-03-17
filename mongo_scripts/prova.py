from pymongo import MongoClient
from pprint import pprint

client = MongoClient()
db = client.exams
collection = db.rawTeachingsEv1011

pprint(collection.find_one({"Insegnamento":"Algebra lineare"}))

for doc in collection.find():
	pprint(doc)
