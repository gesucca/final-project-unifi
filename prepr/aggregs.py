"""Data aggregation functions:
    from students instances to aggregate data;
    between teachings evaluation and students productivity."""

from datetime import datetime

def aggregate_prod(exams_db, raw_prod, drop):

    exams_db.create_collection("productivity")
    _aggregate_prod(raw_prod, exams_db.productivity, datetime(2011, 1, 1), datetime(2011, 12, 31))

    if drop == 'Y':
        exams_db.raw_prod.drop()

    return exams_db.productivity


def _aggregate_prod(source, dest, start, end):

    asd = {}
    asd['Insegnamento'] = 'Algoritmi e strutture dati'

    exams = [asd]

    # init common fields
    for exam in exams:
        exam['N'] = 0
        exam['Voti'] = []
        exam['P>=24'] = 0
        exam['P<24'] = 0
        exam['Inizio Periodo di Riferimento'] = start.strftime("%Y-%m-%d")
        exam['Fine Periodo di Riferimento'] = end.strftime("%Y-%m-%d")

    for doc in source.find():
        source.delete_one(doc)

        if _exam_done_in_ref_period(doc['data_ASD'], start, end):
            asd = _update_doc(doc, asd, 'ASD')

    for exam in exams:
        exam = _std_dev(_avg(exam))
        del exam['Voti']
        dest.insert_one(exam)


def _update_doc(old, new, field):
    new['N'] = new['N'] + 1
    new['Voti'].append(int(old[field]))

    if int(old[field]) >= 24:
        new['P>=24'] = new['P>=24'] + 1
    else:
        new['P<24'] = new['P<24'] + 1

    return new


def _avg(doc):
    doc['Media'] = 0
    for voto in doc['Voti']:
        doc['Media'] = doc['Media'] + voto

    doc['Media'] = round(doc['Media'] / doc['N'], 2)
    return doc


def _std_dev(doc):
    doc['Deviazione standard'] = 0
    for voto in doc['Voti']:
        doc['Deviazione standard'] = doc['Deviazione standard'] + pow((voto - doc['Media']), 2)

    doc['Deviazione standard'] = round(pow(doc['Deviazione standard'] / doc['N'], 0.5), 2)
    return doc


def _exam_done_in_ref_period(date_string, start, end):
    """State if an exam has been done between a certain time span."""
    if date_string == 0:
        return False

    date_spl = [date_string.split('-')[0], date_string.split('-')[1], date_string.split('-')[2]]
    date = datetime(int(date_spl[0]), int(date_spl[1]), int(date_spl[2]))

    return date >= start and date <= end
