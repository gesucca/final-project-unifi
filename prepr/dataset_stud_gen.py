from pymongo import MongoClient

scheme = MongoClient().exams
stud_gen = scheme.create_collection('stud_gen')

prod = scheme.rawStudentsPr1013
stud = scheme.sprod

# aggr doc keys
val = 'Valutazione Test Ingresso [media]'
pl = 'Studenti Laureati [percent]'
ni = 'N [istanze]'
mark = 'Voto [media pesata]'
delay = 'Ritardo [semestre, media pesata]'

for group in prod.aggregate([{"$group": {"_id": {'coorte': '$coorte'}}}]):

    aggr = {val: 0, pl: 0, ni: 0, 'Coorte Immatricolazione': group['_id']['coorte']}

    for doc in prod.find(group['_id']):
        aggr[ni] = aggr[ni] + 1
        aggr[val] = aggr[val] + doc['test']
        if doc['crediti_totali'] == 180:
            aggr[pl] = aggr[pl] + 1

    aggr[val] = round(aggr[val] / aggr[ni], 2)
    aggr[pl] = round((aggr[pl] / aggr[ni]) * 100, 2)

    # weighted mean
    aggr[mark] = 0
    aggr[delay] = 0
    n = 0

    a_a = str(group['_id']['coorte']) + '-' + str(group['_id']['coorte'] + 1)
    for doc in stud.find({'Anno Accademico': a_a}):
        aggr[mark] = aggr[mark] + doc['Voto [media]'] * doc[ni]
        aggr[delay] = aggr[delay] + doc['Ritardo [semestre, media]'] * doc[ni]
        n = n + doc[ni]

    aggr[mark] = round(aggr[mark] / n, 2)
    aggr[delay] = round(aggr[delay] / n, 2)

    stud_gen.insert_one(aggr)
