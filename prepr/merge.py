"""Attribute merging for producing a single binarizable collection."""

def merge_teach(collection):

    for year in collection.distinct('Dataset Provenienza'):

        for teach in collection.distinct('Insegnamento', {'Dataset Provenienza': year}):

            teach_docs = collection.find({'Insegnamento': teach, 'Dataset Provenienza': year})
            temp_doc = teach_docs.next()

            aggr_doc = {'Insegnamento': teach, 'Dataset Provenienza': year}

            aggr_doc['Hash Docente/i'] = temp_doc['Hash Docente/i']
            aggr_doc['Inizio Periodo di Riferimento'] = temp_doc['Inizio Periodo di Riferimento']
            aggr_doc['Fine Periodo di Riferimento'] = temp_doc['Fine Periodo di Riferimento']

            teach_docs.rewind()

            for doc in teach_docs:
                pref = doc['Oggetto Valutazione']
                aggr_doc[pref + ' - Media'] = doc['Media']
                aggr_doc[pref + ' - Std Dev'] = doc['Deviazione standard']
                aggr_doc[pref + ' - P<6'] = doc['P<6']
                aggr_doc[pref + ' - P>=6'] = doc['P>=6']

                collection.delete_one(doc)

            collection.insert_one(aggr_doc)
