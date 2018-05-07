"""Data aggregation utility object, strongly coupled with applicative logic so beware."""

from datetime import datetime


class Aggregator:
    """Abstract factorization of common stuff."""

    def __init__(self, source, destination):
        self._source = source
        self._dest = destination

    def drop(self):
        """Drop the original collection that has been aggregated."""
        self._source.drop()

    def aggregate_stud(self, coorte):
        """Class signature function."""
        raise NotImplementedError('Abstract method!')

    def aggregate_par(self):
        """Class signature function."""
        raise NotImplementedError('Abstract method!')


class StudAggregator(Aggregator):
    """ Data aggregation object from students instances to aggregate data."""

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

    def aggregate_stud(self, coorte):
        exams = _init_exam_docs()

        for doc in self._source.find():
            for keys in self._EX_KEYS:

                if _exam_done_in_ref_period(doc, coorte):
                    new_doc = exams[keys['name']]
                    new_doc['Anno Accademico'] = coorte + '-' + str(int(coorte)+1)
                    _update_doc(doc, new_doc, keys['name'], keys['date'])

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
                del exams[i]['Sem']
                del exams[i]['upd']

                self._dest.insert_one(exams[i])

    def aggregate_par(self):
        raise NotImplementedError('Wrong class!')


def _init_exam_docs():
    exams = {'ASD': {'Insegnamento': 'Algoritmi e strutture dati', 'Anno': 1, 'Sem': 6},
             'MDL': {'Insegnamento': 'Matematica discreta e logica', 'Anno': 1, 'Sem': 6},
             'PRG': {'Insegnamento': 'Programmazione', 'Anno': 1, 'Sem': 6},
             'ANI': {'Insegnamento': 'Analisi I: calcolo differenziale ed integrale', 'Anno': 1, 'Sem': 6},
             'ARC': {'Insegnamento': 'Architetture degli elaboratori', 'Anno': 1, 'Sem': 6},
             'ALG': {'Insegnamento': 'Algebra lineare', 'Anno': 2, 'Sem': 1},
             'CPS': {'Insegnamento': 'Calcolo delle probabilita e statistica', 'Anno': 2, 'Sem': 1},
             'MP': {'Insegnamento': 'Metodologie di programmazione', 'Anno': 2, 'Sem': 1},
             'PC': {'Insegnamento': 'Programmazione concorrente', 'Anno': 2, 'Sem': 1},
             'FIS': {'Insegnamento': 'Fisica generale', 'Anno': 2, 'Sem': 6},
             'BDSI': {'Insegnamento': 'Basi di dati e sistemi informativi', 'Anno': 2, 'Sem': 6},
             'SO': {'Insegnamento': 'Sistemi operativi', 'Anno': 2, 'Sem': 6},
             'ANII': {'Insegnamento': 'Analisi 2: funzioni in piu variabili', 'Anno': 2, 'Sem': 6},
             'CAL': {'Insegnamento': 'Calcolo numerico', 'Anno': 3, 'Sem': 6},
             'IT': {'Insegnamento': 'Informatica teorica', 'Anno': 3, 'Sem': 1},
             'RETI': {'Insegnamento': 'Reti di calcolatori', 'Anno': 3, 'Sem': 1},
             'IUM': {'Insegnamento': 'Interazione uomo macchina', 'Anno': 3, 'Sem': 6}
             }

    # init other common fields
    for i in exams:
        exams[i]['N [istanze]'] = 0
        exams[i]['Voti'] = []
        exams[i]['Date'] = []
        exams[i]['Coorti'] = []
        exams[i]['Voto >= 24 [perc]'] = 0
        exams[i]['upd'] = False

    return exams


def _update_doc(old, new, field_mark, field_date):

    if int(old[field_mark]) > 0:
        new['upd'] = True

        new['N [istanze]'] = new['N [istanze]'] + 1
        new['Voti'].append(int(old[field_mark]))

        if int(old[field_mark]) >= 24:
            new['Voto >= 24 [perc]'] = new['Voto >= 24 [perc]'] + 1

        new['Date'].append(old[field_date])
        new['Coorti'].append(old['coorte'])


def _avg(doc):
    doc['Voto [media]'] = 0
    for voto in doc['Voti']:
        doc['Voto [media]'] = doc['Voto [media]'] + voto

    doc['Voto [media]'] = round(doc['Voto [media]'] / doc['N [istanze]'], 2)


def _std_dev(doc):
    key = 'Voto [std dev]'
    doc[key] = 0
    for voto in doc['Voti']:
        doc[key] = doc[key] + pow((voto - doc['Voto [media]']), 2)

    doc[key] = round(pow(doc[key] / doc['N [istanze]'], 0.5), 2)


def _perc(doc):
    doc['Voto >= 24 [perc]'] = round(100 * doc['Voto >= 24 [perc]'] / doc['N [istanze]'], 2)


def _exam_done_in_ref_period(doc, coorte):
    return str(doc['coorte']) == str(coorte)


def _delay(stuff):
    """Calculated on a yearly basis, no sense in detecting semester shifts."""

    avg_delay = 0
    p1year = 0
    instances = 0

    for i in range(len(stuff['Date'])):
        correct_time = datetime(stuff['Coorti'][i] + stuff['Anno'], stuff['Sem'], 1)
        exam_time = datetime.strptime(stuff['Date'][i], '%Y-%m-%d')
        delay_sem = int((exam_time - correct_time).days / (30*6))

        avg_delay = avg_delay + delay_sem
        if delay_sem >= 1:
            p1year = p1year + 1
        instances = instances + 1

    stuff['Ritardo [semestre, media]'] = round(avg_delay / instances, 2)
    stuff['Ritardo >=1sem [percent]'] = round((p1year / instances) * 100)


class ParAggregator(Aggregator):
    """Aggregate teachings evaluation per paragraph."""

    _GEN = ['Hash Docente/i', 'Anno Accademico']

    def _get_docs_to_aggregate(self):
        return self._source.aggregate(
            [
                {"$group": {"_id": {
                    'Insegnamento': "$Insegnamento",
                    'Paragrafo': "$Paragrafo",
                    'Anno Accademico': '$Anno Accademico'}
                }
                }
            ]
        )

    def aggregate_par(self):

        for group in self._get_docs_to_aggregate():

            # weighted mean for those
            mean = 0
            stdev = 0
            p6 = 0

            # standard mean for this
            n = 0
            i = 0

            last_doc_ref = None  # to avoid another db query

            for doc in self._source.find(group['_id']):
                last_doc_ref = doc
                
                if doc['N'] != '<5' and int(doc['N']) < 0:
                    print(doc)
                    raise Exception('negative stuff')

                try:
                    mean = mean + (doc['Media'] * doc['N'])
                    stdev = stdev + (doc['Deviazione standard'] * doc['N'])
                    p6 = p6 + (doc['P>=6'] * doc['N'])

                    n = n + doc['N']
                    i = i + 1

                except TypeError:  # do not count missing values for means
                    pass

            try:
                mean = round(mean / n, 2)
                stdev = round(stdev / n, 2)
                p6 = round(p6 / n, 2)
                n = int(n / i)
            except ZeroDivisionError:  # it means all values are missing
                mean = 'n.c.'
                stdev = 'n.c.'
                p6 = 'n.c.'
                n = 'n.c.'
            
            if n != 'n.c.' and n < 0:
                print('n' + str(n))
                print('i' + str(i))
                raise Exception('negative stuff')

            self._dest.insert_one(self._construct_doc(group['_id'], last_doc_ref, [mean, stdev, p6, n]))

    def aggregate_stud(self, coorte):
        raise NotImplementedError('Wrong class!')

    def _construct_doc(self, skel,  ref_lst_doc, aggr_attr):
        newdoc = skel

        for attr_gen in self._GEN:
            newdoc[attr_gen] = ref_lst_doc[attr_gen]

        newdoc['Val [media pesata]'] = aggr_attr[0]
        newdoc['Std Dev [media pesata]'] = aggr_attr[1]
        newdoc['Val >= 6 [percent]'] = aggr_attr[2]
        newdoc['N [istanze]'] = aggr_attr[3]
        
        if newdoc['N [istanze]'] != 'n.c.' and int(newdoc['N [istanze]']) < 0:
            print(newdoc)
            print(aggr_attr[3])
            raise Exception('negative stuff')

        return newdoc

