"""Data aggregation from students instances to aggregate data."""
from datetime import datetime

_EX_KEYS = [{'date': 'data_ASD', 'name': 'ASD'},
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
    """Abstract factorization of common stuff."""

    def __init__(self, source, destination):
        self._source = source
        self._dest = destination

    def drop(self):
        """Drop the original collection that has been aggregated."""
        self._source.drop()

    def aggregate_stud(self, start, end):
        """Class signature function."""
        raise NotImplementedError('Abstract method!')

    def aggregate_par(self):
        """Class signature function."""
        raise NotImplementedError('Abstract method!')


class StudAggregator(Aggregator):
    """ Data aggregation object from students instances to aggregate data."""

    def aggregate_stud(self, start, end):
        exams = _init_exam_docs(start, end)

        for doc in self._source.find():
            for keys in _EX_KEYS:

                if _exam_done_in_ref_period(doc[keys['date']], start, end):
                    _update_doc(doc, exams[keys['name']], keys['name'])

        for i in exams:
            if exams[i]['upd']:
                _avg(exams[i])
                _std_dev(exams[i])
                _perc(exams[i])

                del exams[i]['Voti']
                del exams[i]['upd']

                self._dest.insert_one(exams[i])

    def aggregate_par(self):
        raise NotImplementedError('Wrong class!')


# TODO: this is particularly ugly, refactor!
class ParAggregator(Aggregator):
    """Aggregate teachings evaluation per paragraph."""

    def aggregate_par(self):

        docs_to_aggregate = self._source.aggregate(
            [
                {"$group": {"_id": {
                    'Insegnamento': "$Insegnamento",
                    'Paragrafo': "$Paragrafo",
                    'Dataset Provenienza': '$Dataset Provenienza'}
                           }
                }
            ]
        )

        # is doing the mean correct?? uhm
        for group in docs_to_aggregate:
            aggr_attr = [0, 0, 0, 0, 0, 0]
            ref_lst_doc = None # avoid another db query
            for doc in self._source.find(group['_id']):

                aggr_attr[0] = aggr_attr[0] + 1

                try:
                    aggr_attr[1] = aggr_attr[1] + doc['Media']
                    aggr_attr[2] = aggr_attr[2] + doc['Deviazione standard']
                    aggr_attr[3] = aggr_attr[3] + doc['N']
                    aggr_attr[4] = aggr_attr[4] + doc['P<6']
                    aggr_attr[5] = aggr_attr[5] + doc['P>=6']
                except TypeError: # do not count missing values for mean
                    aggr_attr[0] = aggr_attr[0] - 1
                    # print(doc)

                ref_lst_doc = doc

            newdoc = group['_id']
            newdoc['Hash Docente/i'] = ref_lst_doc['Hash Docente/i']
            newdoc['Inizio Periodo di Riferimento'] = ref_lst_doc['Inizio Periodo di Riferimento']
            newdoc['Fine Periodo di Riferimento'] = ref_lst_doc['Fine Periodo di Riferimento']

            try:
                newdoc['Media'] = round(aggr_attr[1] / aggr_attr[0], 2)
                newdoc['Deviazione standard'] = round(aggr_attr[2] / aggr_attr[0], 2)
                newdoc['N'] = round(aggr_attr[3] / aggr_attr[0], 2)
                newdoc['P<6'] = round(aggr_attr[4] / aggr_attr[0], 2)
                newdoc['P>=6'] = round(aggr_attr[5] / aggr_attr[0], 2)

            except ZeroDivisionError: # it means all values are missing
                newdoc['Media'] = 'n.c.'
                newdoc['Deviazione standard'] = 'n.c.'
                newdoc['N'] = '<5'
                newdoc['P<6'] = 'n.c.'
                newdoc['P>=6'] = 'n.c.'

            self._dest.insert_one(newdoc)

    def aggregate_stud(self, start, end):
        raise NotImplementedError('Wrong class!')


def _init_exam_docs(start, end):

    exams = {'ASD': {'Insegnamento': 'Algoritmi e strutture dati'},
             'MDL': {'Insegnamento': 'Matematica discreta e logica'},
             'PRG': {'Insegnamento': 'Programmazione'},
             'ANI': {'Insegnamento': 'Analisi I: calcolo differenziale ed integrale'},
             'ARC': {'Insegnamento': 'Architetture degli elaboratori'},
             'ALG': {'Insegnamento': 'Algebra lineare'},
             'CPS': {'Insegnamento': 'Calcolo delle probabilita e statistica'},
             'MP': {'Insegnamento': 'Metodologie di programmazione'},
             'PC': {'Insegnamento': 'Programmazione concorrente'},
             'FIS': {'Insegnamento': 'Fisica generale'},
             'BDSI': {'Insegnamento': 'Basi di dati e sistemi informativi'},
             'SO': {'Insegnamento': 'Sistemi operativi'},
             'ANII': {'Insegnamento': 'Analisi 2: funzioni in piu variabili'},
             'CAL': {'Insegnamento': 'Calcolo numerico'},
             'IT': {'Insegnamento': 'Informatica teorica'},
             'RETI': {'Insegnamento': 'Reti di calcolatori'},
             'IUM': {'Insegnamento': 'Interazione uomo macchina'}
            }

    # init other common fields
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
    doc['Voto Medio'] = 0
    for voto in doc['Voti']:
        doc['Voto Medio'] = doc['Voto Medio'] + voto

    doc['Voto Medio'] = round(doc['Voto Medio'] / doc['N'], 2)


def _std_dev(doc):
    doc['Deviazione standard'] = 0
    for voto in doc['Voti']:
        doc['Deviazione standard'] = doc['Deviazione standard'] + pow((voto - doc['Voto Medio']), 2)

    doc['Deviazione standard'] = round(pow(doc['Deviazione standard'] / doc['N'], 0.5), 2)


def _perc(doc):
    doc['P<24'] = round(100 * doc['P<24'] / doc['N'], 2)
    doc['P>=24'] = round(100 * doc['P>=24'] / doc['N'], 2)


def _exam_done_in_ref_period(date_string, start, end):
    if date_string == 0 or date_string == '0' or date_string == '0000-00-00':
        return False

    date_spl = [date_string.split('-')[0], date_string.split('-')[1], date_string.split('-')[2]]
    date = datetime(int(date_spl[0]), int(date_spl[1]), int(date_spl[2]))

    return date >= start and date <= end
