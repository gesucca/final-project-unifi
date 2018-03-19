"""Preprocessing steps to form an unique collection ready to be data mined."""

from pymongo import MongoClient
from cleanings import clean_teach_eval

CLIENT = MongoClient()
DB = CLIENT.exams

clean_teach_eval(DB.rawTeachingsEv1011, DB.rawTeachingsEv1011, 2010)
