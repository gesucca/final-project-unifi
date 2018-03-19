"""Preliminary filtering of the data with usefulness criteria."""
from pprint import pprint

def clean_teach_eval(source, dest, year):
    """Cleaning of the teachings evaluation collections's documents.
    source: MongoDB collection
    dest:   MongoDB collection too
    year:   academic year of reference (start) """

    for doc in source.find():
        del doc['']            # little quirk by mongoimport
        del doc['CID']         # useless as a key for this application
        del doc['Corso']       # always 'INFORMATICA' since it is the object of this study
        del doc['Tipo corso']  # as above, always 'INFORMATICA'

        doc['ref_span_begin'] = str(year)+"-01-01"
        doc['ref_span_end'] = str(year+2)+"-03-01"

        pprint(doc)
