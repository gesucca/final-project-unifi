"""Preprocessing steps to form an unique collection ready to be data mined."""

from pymongo import MongoClient
from cleanings import clean_teach_eval
from aggregs import aggregate_prod
from discretize import discretize

CLIENT = MongoClient()
DB = CLIENT.exams

EVAL = clean_teach_eval(DB, 'Y')
PROD = aggregate_prod(DB, DB.rawStudentsPr1013, 'Y')
discretize(EVAL, DB.create_collection("teval_discrete"))
