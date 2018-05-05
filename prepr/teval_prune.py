""""
Remove instances with N of students <5, since no aggregate data has been provided in these cases.

Aggregate the other Ns doing a simple mean.
""""

from pymongo import MongoClient

scheme = MongoClient().exams
collection = scheme['teachEval_aggr']
pruned = scheme.create_collection('teachEval_pruned')

delete = True

for doc in collection.find():
    n_mean = 0
    n_n = 0
    for key in list(doc.keys()):
        if '- N' in key and doc[key] != '<5' and doc[key] != 'n.c.':
            n_mean = n_mean + doc[key]
            del doc[key]
            n_n = n_n + 1
        elif doc[key] == '<5' or doc[key] == 'n.c.':
            del doc[key]

    if n_n != 0:
        doc['Val_ N'] = int(n_mean / n_n)
        if delete:
            collection.delete_one(doc)
        pruned.insert_one(doc)

if delete:
    collection.drop()

