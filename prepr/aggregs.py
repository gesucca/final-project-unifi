"""Data aggregation between teachings evaluation and students productivity."""

from datetime import datetime

def aggregate_prod(exams_db, raw_prod, drop):
    exams_db.create_collection("productivity")

    # a.a. 2010-2011, maybe fetch it from eval dataset??
    _aggregate_prod(raw_prod, exams_db.productivity, datetime(2011, 1, 1), datetime(2011, 12, 31))

    if drop == 'Y':
        exams_db.raw_prod.drop()

    return exams_db.productivity


def _aggregate_prod(source, dest, start, end):
    for doc in source.find():
        # for now I throw them in
        if _exam_done_in_ref_period(doc['data_ASD'], start, end):
            source.delete_many(doc)
            dest.insert_one(doc)



def _exam_done_in_ref_period(date_string, start, end):
    """State if an exam has been done between a certain time span."""
    if date_string == 0:
        return False

    date_spl = [date_string.split('-')[0], date_string.split('-')[1], date_string.split('-')[2]]
    date = datetime(int(date_spl[0]), int(date_spl[1]), int(date_spl[2]))

    return date >= start and date <= end
