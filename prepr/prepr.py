"""Preprocessing steps to form an unique collection ready to be data mined."""

from pymongo import MongoClient
from cleanings import clean_teach_eval
from aggregs import aggregate_prod
from discretize import discretize
from discretize import VAL_SCORE, STD_DEV, MARKS, ZERO_TO_HUND

CLIENT = MongoClient()
DB = CLIENT.exams

EVAL = clean_teach_eval(DB, 'Y')
PROD = aggregate_prod(DB, DB.rawStudentsPr1013, 'Y')

discretize(EVAL, DB.create_collection("teval_discrete"),
           ['Media', 'Deviazione standard', 'N', 'P<6', 'P>=6'],
           [VAL_SCORE, STD_DEV, ZERO_TO_HUND, ZERO_TO_HUND, ZERO_TO_HUND],
           'Y')

discretize(PROD, DB.create_collection("sprod_discrete"),
           ['Media', 'Deviazione standard', 'N', 'P<24', 'P>=24'],
           [MARKS, STD_DEV, ZERO_TO_HUND, ZERO_TO_HUND, ZERO_TO_HUND],
           'Y')
