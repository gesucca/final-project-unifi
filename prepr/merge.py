"""Attribute merging for producing a single binarizable collection."""

class Merger:
    """Attribute merging for producing a single binarizable collection."""
    def __init__(self, keys, bounce_gen, bounce_spec):
        if len(keys) > 2:
            raise Exception('This is application specific: what are you trying to do?')
        self._keys = keys
        self._bounce_gen = bounce_gen
        self._bounce_spec = bounce_spec

    def merge(self, collection):
        """aaa """
        for k_0 in collection.distinct(self._keys[0]):
            for k_1 in collection.distinct(self._keys[1], {self._keys[0]: k_0}):
                teach_docs = collection.find({self._keys[1]: k_1, self._keys[0]: k_0})
                newdoc = self._peek_generalities(teach_docs.next(), k_0, k_1)
                teach_docs.rewind()

                for doc in teach_docs:
                    self._peek_specifics(doc, newdoc)

            collection.delete_many(teach_docs)
            collection.insert_one(newdoc)

    def _peek_generalities(self, doc, k_0, k_1):
        newdoc = {self._keys[1]: k_1, self._keys[0]: k_0}
        for boing in self._bounce_gen:
            newdoc[boing] = doc[boing]
        return newdoc

    def _peek_specifics(self, doc, newdoc):
        pref = doc['Oggetto Valutazione']
        for boing in self._bounce_spec:
            newdoc[pref + ' - ' + boing] = doc[boing]
        # newdoc[pref + ' - Media'] = doc['Media']
        # newdoc[pref + ' - Std Dev'] = doc['Deviazione standard']
        # newdoc[pref + ' - P<6'] = doc['P<6']
        # newdoc[pref + ' - P>=6'] = doc['P>=6']
        # newdoc[pref + ' - N'] = doc['N']

def merge_teach(collection, key1, key2):
    """Merge the teaching evaluations instances as attributes."""

    for year in collection.distinct(key1):
        for teaching in collection.distinct(key2, {'Dataset Provenienza': year}):

            teach_docs = collection.find({'Insegnamento': teaching, 'Dataset Provenienza': year})
            newdoc = _peek_generalities(teach_docs.next(), year, teaching)
            teach_docs.rewind()

            for doc in teach_docs:
                _peek_specifics(doc, newdoc)

            collection.delete_many(teach_docs)
            collection.insert_one(newdoc)


def gen_minable_01(eteach, sprod, merged, drop):
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

                mrg['Anno Accademico'] = mrg['Dataset Provenienza']
                del mrg['Dataset Provenienza']

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
