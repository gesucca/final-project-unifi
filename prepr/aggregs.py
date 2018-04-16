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
                    _update_doc(doc, exams[keys['name']], keys['name'], keys['date'])

        for i in exams:
            if exams[i]['upd']:
                _avg(exams[i])
                _std_dev(exams[i])
                _perc(exams[i])
                _delay(exams[i])

                del exams[i]['Voti']
                del exams[i]['Date']
                del exams[i]['Coorti']
                del exams[i]['Anno']
                del exams[i]['upd']

                self._dest.insert_one(exams[i])

    def aggregate_par(self):
        raise NotImplementedError('Wrong class!')


class ParAggregator(Aggregator):
    """Aggregate teachings evaluation per paragraph."""

    _ATTRIBUTES = ['Media', 'Deviazione standard', 'N', 'P<6', 'P>=6']
    _GEN = ['Hash Docente/i', 'Inizio Periodo di Riferimento', 'Fine Periodo di Riferimento']

    def _get_docs_to_aggregate(self):
        return self._source.aggregate(
            [
                {"$group": {"_id": {
                    'Insegnamento': "$Insegnamento",
                    'Paragrafo': "$Paragrafo",
                    'Dataset Provenienza': '$Dataset Provenienza'}
                           }
                }
            ]
        )

    def aggregate_par(self):

        # is doing the mean correct?? uhm
        for group in self._get_docs_to_aggregate():
            aggr_attr = [0, 0, 0, 0, 0, 0]
            last_doc_ref = None
            for doc in self._source.find(group['_id']):
                last_doc_ref = doc # avoid another db query
                aggr_attr[0] = aggr_attr[0] + 1
                i = 1
                for attr in self._ATTRIBUTES:
                    try:
                        aggr_attr[i] = aggr_attr[i] + doc[attr]
                        i = i + 1
                    except TypeError: # do not count missing values for mean
                        aggr_attr[0] = aggr_attr[0] - 1
                        break

            self._dest.insert_one(self._construct_doc(group['_id'], last_doc_ref, aggr_attr))


    def aggregate_stud(self, start, end):
        raise NotImplementedError('Wrong class!')


    def _construct_doc(self, skel, ref_lst_doc, aggr_attr):
        newdoc = skel
        for attr_gen in self._GEN:
            newdoc[attr_gen] = ref_lst_doc[attr_gen]

        try:
            i = 1
            for attr in self._ATTRIBUTES:
                newdoc[attr] = round(aggr_attr[i] / aggr_attr[0], 2)
                i = i + 1
        except ZeroDivisionError: # it means all values are missing
            i = 1
            for attr in self._ATTRIBUTES:
                i = i + 1
                newdoc[attr] = 'n.c.'

        return newdoc


def _init_exam_docs(start, end):

    exams = {'ASD': {'Insegnamento': 'Algoritmi e strutture dati', 'Anno': 1}, #annual
             'MDL': {'Insegnamento': 'Matematica discreta e logica', 'Anno': 1},
             'PRG': {'Insegnamento': 'Programmazione', 'Anno': 1},
             'ANI': {'Insegnamento': 'Analisi I: calcolo differenziale ed integrale', 'Anno': 1,
                     'Sem': 6},
             'ARC': {'Insegnamento': 'Architetture degli elaboratori', 'Anno': 1},
             'ALG': {'Insegnamento': 'Algebra lineare', 'Anno': 2},
             'CPS': {'Insegnamento': 'Calcolo delle probabilita e statistica', 'Anno': 2},
             'MP': {'Insegnamento': 'Metodologie di programmazione', 'Anno': 2},
             'PC': {'Insegnamento': 'Programmazione concorrente', 'Anno': 2},
             'FIS': {'Insegnamento': 'Fisica generale', 'Anno': 2},
             'BDSI': {'Insegnamento': 'Basi di dati e sistemi informativi', 'Anno': 2},
             'SO': {'Insegnamento': 'Sistemi operativi', 'Anno': 2},
             'ANII': {'Insegnamento': 'Analisi 2: funzioni in piu variabili', 'Anno': 2},
             'CAL': {'Insegnamento': 'Calcolo numerico', 'Anno': 3}, #annual
             'IT': {'Insegnamento': 'Informatica teorica', 'Anno': 3},
             'RETI': {'Insegnamento': 'Reti di calcolatori', 'Anno': 3},
             'IUM': {'Insegnamento': 'Interazione uomo macchina', 'Anno': 3}
            }

    # init other common fields
    for i in exams:
        exams[i]['N'] = 0
        exams[i]['Voti'] = []
        exams[i]['Date'] = []
        exams[i]['Coorti'] = []
        exams[i]['Voto P>=24'] = 0
        exams[i]['Voto P<24'] = 0
        exams[i]['Inizio Periodo di Riferimento'] = start.strftime("%Y-%m-%d")
        exams[i]['Fine Periodo di Riferimento'] = end.strftime("%Y-%m-%d")
        exams[i]['upd'] = False

    return exams


def _update_doc(old, new, field_mark, field_date):
    new['upd'] = True

    new['N'] = new['N'] + 1
    new['Voti'].append(int(old[field_mark]))

    if int(old[field_mark]) >= 24:
        new['Voto P>=24'] = new['Voto P>=24'] + 1
    else:
        new['Voto P<24'] = new['Voto P<24'] + 1

    new['Date'].append(old[field_date])
    new['Coorti'].append(old['coorte'])


def _avg(doc):
    doc['Voto Medio'] = 0
    for voto in doc['Voti']:
        doc['Voto Medio'] = doc['Voto Medio'] + voto

    doc['Voto Medio'] = round(doc['Voto Medio'] / doc['N'], 2)


def _std_dev(doc):
    key = 'Voto Deviazione standard'
    doc[key] = 0
    for voto in doc['Voti']:
        doc[key] = doc[key] + pow((voto - doc['Voto Medio']), 2)

    doc[key] = round(pow(doc[key] / doc['N'], 0.5), 2)


def _perc(doc):
    doc['Voto P<24'] = round(100 * doc['Voto P<24'] / doc['N'], 2)
    doc['Voto P>=24'] = round(100 * doc['Voto P>=24'] / doc['N'], 2)


def _exam_done_in_ref_period(date_string, start, end):
    if date_string == 0 or date_string == '0' or date_string == '0000-00-00':
        return False

    date_spl = [date_string.split('-')[0], date_string.split('-')[1], date_string.split('-')[2]]
    date = datetime(int(date_spl[0]), int(date_spl[1]), int(date_spl[2]))

    return date >= start and date <= end

def _delay(stuff):
    """Calculated on a yearly basis, no sense in detecting semester shifts."""

    avg_delay = 0
    p1year = 0
    instances = 0

    for i in range(len(stuff['Date'])):
        correct_time = stuff['Coorti'][i] + stuff['Anno']
        exam_time = stuff['Date'][i].split('-')[0]
        avg_delay = avg_delay + (int(exam_time) - int(correct_time))
        if (int(exam_time) - int(correct_time)) >= 1:
            p1year = p1year + 1
        instances = instances + 1

    stuff['Ritardo Medio'] = round(avg_delay / instances, 2)
    stuff['Ritardo P>=1y'] = round((p1year / instances) * 100)
    stuff['Ritardo P<1y'] = round(100 - stuff['Ritardo P>=1y'])
