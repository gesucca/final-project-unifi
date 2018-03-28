"""Preliminary filtering of the data with usefulness criteria.
WARNING: pretty bad code in this one"""

import hashlib

def clean_teach_eval(exams_db, drop):
    """Cleaning of the teachings evaluation collections's documents.
    input: MongoDB reference
    output: collection cleaned"""

    exams_db.create_collection("teachEval")

    _clean_teach_eval(exams_db.rawTeachingsEv1011, exams_db.teachEval, 2010)
    _clean_teach_eval(exams_db.rawTeachingsEv1112, exams_db.teachEval, 2011)
    _clean_teach_eval(exams_db.rawTeachingsEv1213, exams_db.teachEval, 2012)
    _clean_teach_eval(exams_db.rawTeachingsEv1314, exams_db.teachEval, 2013)

    if drop == 'Y':
        exams_db.rawTeachingsEv1011.drop()
        exams_db.rawTeachingsEv1112.drop()
        exams_db.rawTeachingsEv1213.drop()
        exams_db.rawTeachingsEv1314.drop()

    return exams_db.teachEval


def _clean_teach_eval(source, dest, year):
    for doc in source.find():
        source.delete_many(doc)

        doc = _clarify_questions(doc, year)
        doc = _time_ref(doc, year)
        doc = _clean_and_polish(doc)

        dest.insert_one(doc)


def _clean_and_polish(doc):
    del doc['']                 # little quirk by mongoimport
    del doc['CID']              # useless as a key for this application
    del doc['Corso']            # always 'INFORMATICA' since it is the object of this study
    del doc['Tipo corso']       # as above, always 'INFORMATICA'

    # simply clearer
    doc['P<6'] = doc.pop('P1')
    doc['P>=6'] = doc.pop('P2')

    # hide teacher name
    teacher_hash = hashlib.md5(doc['Docente/i'].encode('utf-8')).hexdigest()
    del doc['Docente/i']
    doc['Hash Docente/i'] = teacher_hash

    return doc


def _time_ref(doc, year):
    # reference period for exam valuation
    doc['Inizio Periodo di Riferimento'] = str(year+1)+'-01-01'
    doc['Fine Periodo di Riferimento'] = str(year+1)+'-12-31'
    doc['Dataset Provenienza'] = str(year) + '-' + str(year+1)
    return doc


def _clarify_questions(doc, year):
    if year == 2010:
        doc = _clarify_questions_2010(doc)
    else:
        doc = _clarify_questions_gen(doc)
    del doc['Q']
    del doc['Quesito']
    return doc

def _clarify_questions_gen(doc):
    if doc['Q'] == 'D4':
        doc['Oggetto Valutazione'] = 'Conoscenze preliminari sufficienti'
    if doc['Q'] == 'D5':
        doc['Oggetto Valutazione'] = 'Argomenti trattati nuovi o integrativi'
    if doc['Q'] == 'D6':
        doc['Oggetto Valutazione'] = 'Carico di studio proporzionato a credti'
    if doc['Q'] == 'D7':
        doc['Oggetto Valutazione'] = 'Materiale didattico adeguato'
    if doc['Q'] == 'D8':
        doc['Oggetto Valutazione'] = 'Attivita integrative utili'
    if doc['Q'] == 'D9':
        doc['Oggetto Valutazione'] = 'Modalita esame chiare'
    if doc['Q'] == 'D10':
        doc['Oggetto Valutazione'] = 'Orari didattica rispettati'
    if doc['Q'] == 'D11':
        doc['Oggetto Valutazione'] = 'Docente stimola interesse'
    if doc['Q'] == 'D12':
        doc['Oggetto Valutazione'] = 'Docente chiaro'
    if doc['Q'] == 'D13':
        doc['Oggetto Valutazione'] = 'Docente reperibile'
    if doc['Q'] == 'D14':
        doc['Oggetto Valutazione'] = 'Docente disponibile ed esauriente'
    if doc['Q'] == 'D17':
        doc['Oggetto Valutazione'] = 'Argomenti interessanti'
    if doc['Q'] == 'D18':
        doc['Oggetto Valutazione'] = 'Soddisfazione complessiva corso'
    if doc['Q'] == 'D19':
        doc['Oggetto Valutazione'] = 'Copertura programma a lezione'
    if doc['Q'] == 'D20':
        doc['Oggetto Valutazione'] = 'Prove intermedie utili'
    if doc['Q'] == 'D21':
        doc['Oggetto Valutazione'] = 'Prove intermedie danneggiano frequenza'
    return doc


def _clarify_questions_2010(doc):
    if doc['Q'] == 'D1':
        doc['Oggetto Valutazione'] = 'Carico di lavoro accettabile'
    if doc['Q'] == 'D2':
        doc['Oggetto Valutazione'] = 'Organizzazione corso'
    if doc['Q'] == 'D3':
        doc['Oggetto Valutazione'] = 'Orario consente studio individuale'
    if doc['Q'] == 'D4':
        doc['Oggetto Valutazione'] = 'Carico di studio proporzionato a credti'
    if doc['Q'] == 'D5':
        doc['Oggetto Valutazione'] = 'Materiale didattico adeguato'
    if doc['Q'] == 'D6':
        doc['Oggetto Valutazione'] = 'Attivita integrative utili'
    if doc['Q'] == 'D7':
        doc['Oggetto Valutazione'] = 'Modalita esame chiare'
    if doc['Q'] == 'D8':
        doc['Oggetto Valutazione'] = 'Orari rispettati'
    if doc['Q'] == 'D9':
        doc['Oggetto Valutazione'] = 'Docente reperibile'
    if doc['Q'] == 'D10':
        doc['Oggetto Valutazione'] = 'Docente stimola interesse'
    if doc['Q'] == 'D11':
        doc['Oggetto Valutazione'] = 'Docente chiaro'
    if doc['Q'] == 'D12':
        doc['Oggetto Valutazione'] = 'Docente disponibile ed esauriente'
    if doc['Q'] == 'D13':
        doc['Oggetto Valutazione'] = 'Aule lezioni adeguate'
    if doc['Q'] == 'D14':
        doc['Oggetto Valutazione'] = 'Strumenti e locali adeguati'
    if doc['Q'] == 'D15':
        doc['Oggetto Valutazione'] = 'Conoscenze preliminari sufficienti'
    if doc['Q'] == 'D16':
        doc['Oggetto Valutazione'] = 'Argomenti trattati nuovi o integrativi'
    if doc['Q'] == 'D17':
        doc['Oggetto Valutazione'] = 'Argomenti interessanti'
    if doc['Q'] == 'D18':
        doc['Oggetto Valutazione'] = 'Soddisfazione complessiva corso'
    return doc
