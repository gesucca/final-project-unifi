"""Preliminary filtering of the data with usefulness criteria."""
import hashlib

QSET_OLD = {'D1': 'Carico di lavoro accettabile',
            'D2': 'Organizzazione corso',
            'D3': 'Orario consente studio individuale',
            'D4': 'Carico di studio proporzionato a credti',
            'D5': 'Materiale didattico adeguato',
            'D6': 'Attivita integrative utili',
            'D7': 'Modalita esame chiare',
            'D8': 'Orari rispettati',
            'D9': 'Docente reperibile',
            'D10': 'Docente stimola interesse',
            'D11': 'Docente chiaro',
            'D12': 'Docente disponibile ed esauriente',
            'D13': 'Aule lezioni adeguate',
            'D14': 'Strumenti e locali adeguati',
            'D15': 'Conoscenze preliminari sufficienti',
            'D16': 'Argomenti trattati nuovi o integrativi',
            'D17': 'Argomenti interessanti',
            'D18': 'Soddisfazione complessiva corso'
           }

QSET_GEN = {'D4': 'Conoscenze preliminari sufficienti',
            'D5': 'Argomenti trattati nuovi o integrativi',
            'D6': 'Carico di studio proporzionato a credti',
            'D7': 'Materiale didattico adeguato',
            'D8': 'Attivita integrative utili',
            'D9': 'Modalita esame chiare',
            'D10': 'Orari didattica rispettati',
            'D11': 'Docente stimola interesse',
            'D12': 'Docente chiaro',
            'D13': 'Docente reperibile',
            'D14': 'Docente disponibile ed esauriente',
            'D17': 'Argomenti interessanti',
            'D18': 'Soddisfazione complessiva corso',
            'D19': 'Copertura programma a lezione',
            'D20': 'Prove intermedie utili',
            'D21': 'Prove intermedie danneggiano frequenza'
           }


class Cleaner:
    """Cleaning of the teachings evaluation collections's documents."""
    _cleaned = list()

    def __init__(self, destination):
        self._dest = destination
        self._qset = None

    def set_qset(self, qset):
        """Simple setter for the questions set. """
        self._qset = qset

    def drop(self):
        """Drop the original collections that has been cleaned."""
        for coll in self._cleaned:
            coll.drop()

    def clean(self, source, year, delete):
        """Do the work and insert cleaned docs into destination collection."""
        if self._qset is None:
            raise Exception('Questions Set not set!')

        for doc in source.find():
            if delete:
                source.delete_one(doc)

            doc = _clarify_questions(doc, self._qset)
            doc = _time_ref(doc, year)
            doc = _polish(doc)

            self._dest.insert_one(doc)

        self._cleaned.append(source)


def _polish(doc):

    del doc['']                 # little quirk by mongoimport
    del doc['CID']              # useless as a key for this application
    del doc['Corso']            # always 'INFORMATICA' since it is the object of this study
    del doc['Tipo corso']       # as above, always 'INFORMATICA'

    # simply clearer
    doc['P<6'] = doc.pop('P1')
    doc['P>=6'] = doc.pop('P2')

    # hide teacher name
    teacher_hash = hashlib.sha1(doc['Docente/i'].encode('utf-8')).hexdigest()[:12]
    del doc['Docente/i']
    doc['Hash Docente/i'] = teacher_hash

    return doc


def _time_ref(doc, year):

    # reference period for exam valuation
    doc['Inizio Periodo di Riferimento'] = str(year+1)+'-01-01'
    doc['Fine Periodo di Riferimento'] = str(year+1)+'-12-31'
    doc['Dataset Provenienza'] = str(year) + '-' + str(year+1)

    return doc


def _clarify_questions(doc, qset):

    doc['Oggetto Valutazione'] = qset[doc['Q']]

    del doc['Q']
    del doc['Quesito']

    return doc
