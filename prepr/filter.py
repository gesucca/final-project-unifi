"""Preliminary filtering of the data with usefulness criteria."""

from pymongo import MongoClient
from pprint import pprint

CLIENT = MongoClient()
DB = CLIENT.exams
COLLECTION = DB.rawTeachingsEv1011

# pprint(COLLECTION.find_one({"Insegnamento":"Algebra lineare"}))

for doc in COLLECTION.find():
    pprint(doc)
