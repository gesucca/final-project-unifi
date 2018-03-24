"""Preprocessing steps to form an unique collection ready to be data mined."""

from pymongo import MongoClient
from cleanings import clean_teach_eval

CLIENT = MongoClient()
DB = CLIENT.exams

DB.create_collection("teachEval")
clean_teach_eval(DB.rawTeachingsEv1011, DB.teachEval, 2010)
DB.rawTeachingsEv1011.drop()

clean_teach_eval(DB.rawTeachingsEv1112, DB.teachEval, 2011)
DB.rawTeachingsEv1112.drop()
