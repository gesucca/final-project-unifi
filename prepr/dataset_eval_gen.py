from pymongo import MongoClient

scheme = MongoClient().exams
eval_gen = scheme.create_collection('eval_gen')
teval = scheme['teachEval_aggr']

val = 'Valutazione Complessiva [media pesata]'
sdv = 'Deviazione Standard Complessiva [media pesata]'
prc = 'Percentuale Valutazioni Sufficienti [media pesata]'
n = 'Numero Valutazioni [media]'

for group in teval.aggregate([{"$group": {"_id": {'Anno Accademico': '$Anno Accademico'}}}]):

    aggr = {val: 0, sdv: 0, prc: 0, n: 0}

    i = 0
    for doc in teval.find(group['_id']):
        if doc['Val [media pesata]'] != 'n.c.':
            aggr[val] = aggr[val] + doc['Val [media pesata]'] * doc['N [istanze]']
            aggr[sdv] = aggr[sdv] + doc['Std Dev [media pesata]'] * doc['N [istanze]']
            aggr[prc] = aggr[prc] + doc['Val >= 6 [percent]'] * doc['N [istanze]']
            aggr[n] = aggr[n] + doc['N [istanze]']
            i = i + 1

    aggr[val] = round(aggr[val] / aggr[n], 2)
    aggr[sdv] = round(aggr[sdv] / aggr[n], 2)
    aggr[prc] = round(aggr[prc] / aggr[n], 2)
    aggr[n] = int(round(aggr[n] / i, 0))

    aggr['Anno Accademico'] = group['_id']['Anno Accademico']

    eval_gen.insert_one(aggr)
