"""Attribute merging for producing a single binarizable collection."""

class Merger:
    """Attribute merging for producing a single binarizable collection."""

    def __init__(self, keys, delete):

        if len(keys) > 3:
            raise Exception('This is application specific: what are you trying to do?')

        self._keys = keys
        self._delete = delete

        self._bounce_gen = None
        self._bounce_spec = None


    def set_specific_keys(self, bounce_spec):
        """Self explaining method."""
        self._bounce_spec = bounce_spec


    def set_gen_keys(self, bounce_gen):
        """Self explaining method."""
        self._bounce_gen = bounce_gen


    def merge_attributes(self, coll):
        """Self explaining method."""
        for k_0 in coll.distinct(self._keys[0]):
            for k_1 in coll.distinct(self._keys[1], {self._keys[0]: k_0}):

                teach_docs = coll.find(self._get_filter(k_0, k_1))
                newdoc = self._peek_generalities(teach_docs.next(), k_0, k_1)
                teach_docs.rewind()

                for doc in teach_docs:
                    self._peek_specifics(doc, newdoc)

                if self._delete:
                    coll.delete_many(self._get_filter(k_0, k_1))
                    coll.insert_one(newdoc)

    def merge_collections(self, coll1, coll2, label2, dest):
        """Finally merge two datasets intoa single (minable) collection."""
        for teach_doc in coll1.find():
            for prod_doc in coll2.find({self._keys[0]: teach_doc[self._keys[0]],
                                        self._keys[1]: teach_doc[self._keys[1]]}):

                if prod_doc[self._keys[2]].upper() == teach_doc[self._keys[2]].upper():

                    newdoc = teach_doc
                    for key in self._bounce_spec:
                        newdoc[label2 + ' - ' + key] = prod_doc[key]

                    dest.insert_one(newdoc)

                    if self._delete:
                        coll2.delete_one(prod_doc)
                    break

            if self._delete:
                coll1.delete_one(teach_doc)

        if self._delete:
            coll1.drop()
            coll2.drop()


    def _get_filter(self, k_0, k_1):
        return {self._keys[1]: k_1, self._keys[0]: k_0}


    def _peek_generalities(self, doc, k_0, k_1):
        if self._bounce_gen is None:
            raise Exception('Please set the generic attributes to be merged!')

        newdoc = {self._keys[1]: k_1, self._keys[0]: k_0}
        for boing in self._bounce_gen:
            newdoc[boing] = doc[boing]
        return newdoc


    def _peek_specifics(self, doc, newdoc):
        if self._bounce_spec is None:
            raise Exception('Please set the specific attributes to be merged!')

        pref = doc['Oggetto Valutazione']
        for boing in self._bounce_spec:
            newdoc[pref + ' - ' + boing] = doc[boing]
