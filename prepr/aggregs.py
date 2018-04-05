"""Data aggregation from students instances to aggregate data."""
from datetime import datetime

_EXAMS = [{'date': 'data_ASD', 'name': 'ASD'},
          {'date': 'data_MDL', 'name': 'MDL'},
          {'date': 'data_PRG', 'name': 'PRG'},
          {'date': 'data_ANI', 'name': 'ANI'},
          {'date': 'data_ARC', 'name': 'ARC'},
          {'date': 'data_ALG', 'name': 'ALG'},
          {'date': 'data_CPS', 'name': 'CPS'},
          {'date': 'data_MP', 'name': 'MP'},
          {'date': 'data_PC', 'name': 'PC'},
          {'date': 'data_FIS', 'name': 'FIS'},
          {'date': 'data_BDSI', 'name': 'BDSI'},
          {'date': 'data_SO', 'name': 'SO'},
          {'date': 'data_ANII', 'name': 'ANII'},
          {'date': 'data_CAL', 'name': 'CAL'},
          {'date': 'data_IT', 'name': 'IT'},
          {'date': 'data_RETI', 'name': 'RETI'},
          {'date': 'data_IUM', 'name': 'IUM'}
         ]


class Aggregator:
    """Data aggregation object from students instances to aggregate data."""

    def __init__(self, source, destination):
        self._source = source
        self._dest = destination

    def drop(self):
        """Drop the original collection that has been aggregated."""
        self._source.drop()

    def aggregate(self, start, end, delete):
        """Class signature function."""
        exams = _init_exam_docs(start, end)

        for doc in self._source.find():
            for keys in _EXAMS:
                if _exam_done_in_ref_period(doc[keys['date']], start, end):
                    _update_doc(doc, exams[keys['name']], keys['name'])
                    if delete:
                        self._source.delete_one(doc)

        for i in exams:
            if exams[i]['upd']:
                _avg(exams[i])
                _std_dev(exams[i])
                _perc(exams[i])
                del exams[i]['Voti']
                del exams[i]['upd']
                self._dest.insert_one(exams[i])


def _init_exam_docs(start, end):
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

    exams = {'ASD': asd, 'MDL': mdl, 'PRG': prg, 'ANI': an1, 'ARC': arc, 'ALG': alg, 'CPS': cps,
             'MP': mdp, 'PC': p_c, 'FIS': f_g, 'BDSI': bdsi, 'SO': s_o, 'ANII': an2, 'CAL': cal,
             'IT': i_t, 'RETI': reti, 'IUM': ium}

    # init common fields
    for i in exams:
        exams[i]['N'] = 0
        exams[i]['Voti'] = []
        exams[i]['P>=24'] = 0
        exams[i]['P<24'] = 0
        exams[i]['Inizio Periodo di Riferimento'] = start.strftime("%Y-%m-%d")
        exams[i]['Fine Periodo di Riferimento'] = end.strftime("%Y-%m-%d")
        exams[i]['upd'] = False

    return exams


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
