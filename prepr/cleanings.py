"""Preliminary filtering of the data with usefulness criteria."""

def clean_teach_eval(source, dest, year):
    """Cleaning of the teachings evaluation collections's documents.
    source: MongoDB collection
    dest:   MongoDB collection too
    year:   academic year of reference (start) """

    for doc in source.find():
        source.delete_many(doc)

        del doc['']                 # little quirk by mongoimport
        del doc['CID']              # useless as a key for this application
        del doc['Corso']            # always 'INFORMATICA' since it is the object of this study
        del doc['Tipo corso']       # as above, always 'INFORMATICA'

        # simply clearer
        doc['P<6'] = doc.pop('P1')
        doc['P>=6'] = doc.pop('P2')

        # clarify questions
        if doc['Q'] == 'D1':
            doc['Oggetto Valutazione'] = 'Carico di lavoro accettabile?'
            # ...
        del doc['Q']
        del doc['Quesito']

        # reference period for exam valuation
        doc['Inizio Periodo di Riferimento'] = str(year+1)+"-01-01"
        doc['Fine Periodo di Riferimento'] = str(year+2)+"-03-01"

        dest.insert_one(doc)
