"""Data aggregation functions from students instances to aggregate data."""

from datetime import datetime

def aggregate_prod(exams_db, raw_prod, drop):

    exams_db.create_collection("productStud")
    _aggr_prod(raw_prod, exams_db.productStud, datetime(2011, 1, 1), datetime(2011, 12, 31))
    _aggr_prod(raw_prod, exams_db.productStud, datetime(2012, 1, 1), datetime(2012, 12, 31))
    _aggr_prod(raw_prod, exams_db.productStud, datetime(2013, 1, 1), datetime(2013, 12, 31))
    _aggr_prod(raw_prod, exams_db.productStud, datetime(2014, 1, 1), datetime(2014, 12, 31))

    if drop == 'Y':
        raw_prod.drop()

    return exams_db.productStud


def _aggr_prod(source, dest, start, end):

    exams = _init_exam_docs()

    # init common fields
    for i in exams:
        exams[i]['N'] = 0
        exams[i]['Voti'] = []
        exams[i]['P>=24'] = 0
        exams[i]['P<24'] = 0
        exams[i]['Inizio Periodo di Riferimento'] = start.strftime("%Y-%m-%d")
        exams[i]['Fine Periodo di Riferimento'] = end.strftime("%Y-%m-%d")
        exams[i]['upd'] = False

    for doc in source.find():

        if _exam_done_in_ref_period(doc['data_ASD'], start, end):
            _update_doc(doc, exams['ASD'], 'ASD')
        if _exam_done_in_ref_period(doc['data_MDL'], start, end):
            _update_doc(doc, exams['MDL'], 'MDL')
        if _exam_done_in_ref_period(doc['data_PRG'], start, end):
            _update_doc(doc, exams['PRG'], 'PRG')
        if _exam_done_in_ref_period(doc['data_ANI'], start, end):
            _update_doc(doc, exams['ANI'], 'ANI')
        if _exam_done_in_ref_period(doc['data_ARC'], start, end):
            _update_doc(doc, exams['ARC'], 'ARC')

        if _exam_done_in_ref_period(doc['data_ALG'], start, end):
            _update_doc(doc, exams['ALG'], 'ALG')
        if _exam_done_in_ref_period(doc['data_CPS'], start, end):
            _update_doc(doc, exams['CPS'], 'CPS')
        if _exam_done_in_ref_period(doc['data_MP'], start, end):
            _update_doc(doc, exams['MP'], 'MP')
        if _exam_done_in_ref_period(doc['data_PC'], start, end):
            _update_doc(doc, exams['PC'], 'PC')

        if _exam_done_in_ref_period(doc['data_FIS'], start, end):
            _update_doc(doc, exams['FIS'], 'FIS')
        if _exam_done_in_ref_period(doc['data_BDSI'], start, end):
            _update_doc(doc, exams['BDSI'], 'BDSI')
        if _exam_done_in_ref_period(doc['data_SO'], start, end):
            _update_doc(doc, exams['SO'], 'SO')
        if _exam_done_in_ref_period(doc['data_ANII'], start, end):
            _update_doc(doc, exams['ANII'], 'ANII')

        if _exam_done_in_ref_period(doc['data_CAL'], start, end):
            _update_doc(doc, exams['CAL'], 'CAL')
        if _exam_done_in_ref_period(doc['data_IT'], start, end):
            _update_doc(doc, exams['IT'], 'IT')
        if _exam_done_in_ref_period(doc['data_RETI'], start, end):
            _update_doc(doc, exams['RETI'], 'RETI')
        if _exam_done_in_ref_period(doc['data_IUM'], start, end):
            _update_doc(doc, exams['IUM'], 'IUM')


    for i in exams:
        if exams[i]['upd']:
            _avg(exams[i])
            _std_dev(exams[i])
            _perc(exams[i])
            del exams[i]['Voti']
            del exams[i]['upd']
            dest.insert_one(exams[i])


def _init_exam_docs():
    asd = {}
    asd['Insegnamento'] = 'Algoritmi e strutture dati'
    mdl = {}
    mdl['Insegnamento'] = 'Matematica discreta e logica'
    prg = {}
    prg['Insegnamento'] = 'Programmazione'
    an1 = {}
    an1['Insegnamento'] = 'Analisi I: calcolo differenziale ed integrale'
    arc = {}
    arc['Insegnamento'] = 'Architetture degli elaboratori'

    alg = {}
    alg['Insegnamento'] = 'Algebra lineare'
    cps = {}
    cps['Insegnamento'] = 'Calcolo delle probabilita e statistica'
    mdp = {}
    mdp['Insegnamento'] = 'Metodologie di programmazione'
    p_c = {}
    p_c['Insegnamento'] = 'Programmazione concorrente'

    f_g = {}
    f_g['Insegnamento'] = 'Fisica generale'
    s_o = {}
    s_o['Insegnamento'] = 'Sistemi operativi'
    bdsi = {}
    bdsi['Insegnamento'] = 'Basi di dati e sistemi informativi'
    an2 = {}
    an2['Insegnamento'] = 'Analisi 2: funzioni in piu variabili'

    cal = {}
    cal['Insegnamento'] = 'Calcolo numerico'
    i_t = {}
    i_t['Insegnamento'] = 'Informatica teorica'
    reti = {}
    reti['Insegnamento'] = 'Reti di calcolatori'
    ium = {}
    ium['Insegnamento'] = 'Interazione uomo macchina'

    return {'ASD': asd, 'MDL': mdl, 'PRG': prg, 'ANI': an1, 'ARC': arc, 'ALG': alg, 'CPS': cps,
            'MP': mdp, 'PC': p_c, 'FIS': f_g, 'BDSI': bdsi, 'SO': s_o, 'ANII': an2, 'CAL': cal,
            'IT': i_t, 'RETI': reti, 'IUM': ium}


def _update_doc(old, new, field):
    new['upd'] = True

    new['N'] = new['N'] + 1
    new['Voti'].append(int(old[field]))

    if int(old[field]) >= 24:
        new['P>=24'] = new['P>=24'] + 1
    else:
        new['P<24'] = new['P<24'] + 1


def _avg(doc):
    doc['Media'] = 0
    for voto in doc['Voti']:
        doc['Media'] = doc['Media'] + voto

    doc['Media'] = round(doc['Media'] / doc['N'], 2)


def _std_dev(doc):
    doc['Deviazione standard'] = 0
    for voto in doc['Voti']:
        doc['Deviazione standard'] = doc['Deviazione standard'] + pow((voto - doc['Media']), 2)

    doc['Deviazione standard'] = round(pow(doc['Deviazione standard'] / doc['N'], 0.5), 2)


def _perc(doc):
    doc['P<24'] = 100 * doc['P<24'] / doc['N']
    doc['P>=24'] = 100 * doc['P>=24'] / doc['N']


def _exam_done_in_ref_period(date_string, start, end):
    """State if an exam has been done between a certain time span."""
    if date_string == 0 or date_string == '0' or date_string == '0000-00-00':
        return False

    date_spl = [date_string.split('-')[0], date_string.split('-')[1], date_string.split('-')[2]]
    date = datetime(int(date_spl[0]), int(date_spl[1]), int(date_spl[2]))

    return date >= start and date <= end
