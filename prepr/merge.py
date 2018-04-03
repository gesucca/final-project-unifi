"""Attribute merging for producing a single binarizable collection."""

def merge_teach(collection):
    """Merge the teaching evaluations instances as attributes."""
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
                aggr_doc[pref + ' - N'] = doc['N']

                collection.delete_one(doc)

            collection.insert_one(aggr_doc)


def the_big_merge(eteach, sprod, merged, drop):
    """Finally merge the two dataset intoa single minable collection."""

    key1 = 'Inizio Periodo di Riferimento'
    key2 = 'Fine Periodo di Riferimento'
    key3 = 'Insegnamento'

    for tdoc in eteach.find():
        for doc in sprod.find({key1: tdoc[key1], key2: tdoc[key2]}):

            if doc[key3].upper() == tdoc[key3].upper():

                mrg = tdoc

                del mrg['_id'] # I want it to be regenerated
                del mrg['Inizio Periodo di Riferimento']
                del mrg['Fine Periodo di Riferimento']

                mrg['Insegnamento'] = mrg['Insegnamento'].upper()
                mrg['Produttivita Studenti - N'] = doc['N']
                mrg['Produttivita Studenti - P>=24'] = doc['P>=24']
                mrg['Produttivita Studenti - P<24'] = doc['P<24']
                mrg['Produttivita Studenti - Media'] = doc['Media']
                mrg['Produttivita Studenti - Std Dev'] = doc['Deviazione standard']

                merged.insert_one(mrg)

                if drop:
                    sprod.delete_one(doc)
                break

        if drop:
            eteach.delete_one(tdoc)

    if drop:
        eteach.drop()
        sprod.drop()
