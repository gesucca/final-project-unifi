"""Preprocessing steps to form an unique collection ready to be data mined."""

from pymongo import MongoClient
from cleanings import clean_teach_eval
from aggregs import aggregate

CLIENT = MongoClient()
DB = CLIENT.exams

aggregate(DB, clean_teach_eval(DB, 'Y'), DB.rawStudentsPr1013)
