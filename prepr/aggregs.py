"""Data aggregation between teachings evaluation and students productivity."""

from datetime import datetime

from pprint import pprint

# going OOP here

def aggregate(exams_db, teach_eval, prodctivity):
    exams_db.create_collection("aa_2010_1011")
    _aggregate(teach_eval, prodctivity, exams_db.aa_2010_1011)


def _aggregate(teach_eval, productivity, dest):
    for doc in productivity.find():
        if exam_done_in_ref_period(doc['data_ASD'], datetime(2010, 1, 1), datetime(2011, 7, 1)):
            pprint(doc)

def exam_done_in_ref_period(date_string, start, end):
    """State if an exam has been done between a certain time span."""
    if date_string == 0:
        return False

    date_spl = [date_string.split('-')[0], date_string.split('-')[1], date_string.split('-')[2]]
    date = datetime(int(date_spl[0]), int(date_spl[1]), int(date_spl[2]))

    return date >= start and date <= end
