from pymongo import MongoClient

scheme = MongoClient().exams
eval_gen = scheme.create_collection('eval_gen')
teval = scheme['teachEval_aggr']

for group in teval.aggregate([{"$group": {"_id": {'Anno Accademico': '$Anno Accademico'}}}]):

    aggr = {'Valutazione Complessiva [media pesata]': 0, 'Deviazione Standard Complessiva [media pesata]': 0,
            'Percentuale Valutazioni Sufficienti [media pesata]': 0, 'Numero Valutazioni [media]': 0}
    i = 0
    for doc in teval.find(group['_id']):
        if doc['Val [media pesata]'] != 'n.c.':
            aggr['Valutazione Complessiva [media pesata]'] = aggr['Valutazione Complessiva [media pesata]'] + doc['Val [media pesata]'] * doc['N [istanze]']
            aggr['Deviazione Standard Complessiva [media pesata]'] = aggr['Deviazione Standard Complessiva [media pesata]'] + doc['Std Dev [media pesata]'] * doc['N [istanze]']
            aggr['Percentuale Valutazioni Sufficienti [media pesata]'] = aggr['Percentuale Valutazioni Sufficienti [media pesata]'] + doc['Val >= 6 [percent]'] * doc['N [istanze]']
            aggr['Numero Valutazioni [media]'] = aggr['Numero Valutazioni [media]'] + doc['N [istanze]']
            i = i + 1

    aggr['Valutazione Complessiva [media pesata]'] = round(aggr['Valutazione Complessiva [media pesata]'] / aggr['Numero Valutazioni [media]'], 2)
    aggr['Deviazione Standard Complessiva [media pesata]'] = round(aggr['Deviazione Standard Complessiva [media pesata]'] / aggr['Numero Valutazioni [media]'], 2)
    aggr['Percentuale Valutazioni Sufficienti [media pesata]'] = round(aggr['Percentuale Valutazioni Sufficienti [media pesata]'] / aggr['Numero Valutazioni [media]'], 2)
    aggr['Numero Valutazioni [media]'] = int(round(aggr['Numero Valutazioni [media]'] / i, 0))

    aggr['Anno Accademico'] = group['_id']['Anno Accademico']

    eval_gen.insert_one(aggr)
