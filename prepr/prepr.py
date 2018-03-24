"""Preprocessing steps to form an unique collection ready to be data mined."""

from pymongo import MongoClient
from cleanings import clean_teach_eval
from aggregs import aggregate

def _aggregate(exams_db, teach_eval, prodctivity):
    exams_db.create_collection("aa_2010_1011")
    aggregate(teach_eval, prodctivity, exams_db.aa_2010_1011)


def _clean_teach_eval(exams_db):
    exams_db.create_collection("teachEval")

    clean_teach_eval(exams_db.rawTeachingsEv1011, exams_db.teachEval, 2010)
    exams_db.rawTeachingsEv1011.drop()

    clean_teach_eval(exams_db.rawTeachingsEv1112, exams_db.teachEval, 2011)
    exams_db.rawTeachingsEv1112.drop()

    clean_teach_eval(exams_db.rawTeachingsEv1213, exams_db.teachEval, 2012)
    exams_db.rawTeachingsEv1213.drop()

    clean_teach_eval(exams_db.rawTeachingsEv1314, exams_db.teachEval, 2013)
    exams_db.rawTeachingsEv1314.drop()

    return exams_db.teachEval


CLIENT = MongoClient()
DB = CLIENT.exams

_aggregate(DB, _clean_teach_eval(DB), DB.rawStudentsPr1013)
