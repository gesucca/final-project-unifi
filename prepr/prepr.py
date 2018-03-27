"""Preprocessing steps to form an unique collection ready to be data mined."""

from pymongo import MongoClient
from cleanings import clean_teach_eval
from aggregs import aggregate_prod

CLIENT = MongoClient()
DB = CLIENT.exams

clean_teach_eval(DB, 'Y')
aggregate_prod(DB, DB.rawStudentsPr1013, 'Y')
