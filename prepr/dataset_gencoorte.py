from pymongo import MongoClient

scheme = MongoClient().exams
scheme.create_collection('minable_gen')
minable_gen = scheme['minable_gen']

prod = scheme.rawStudentsPr1013
stud = scheme.sprod

for group in prod.aggregate([{"$group": {"_id": {'coorte': '$coorte'}}}]):

    aggr = {'Valutazione Test Incresso [media]': 0, 'Studenti Laureati [percent]': 0, 'N [istanze]': 0, 'Coorte Immatricolazione': group['_id']['coorte']}

    for doc in prod.find(group['_id']):
        aggr['N [istanze]'] = aggr['N [istanze]'] + 1
        aggr['Valutazione Test Incresso [media]'] = aggr['Valutazione Test Incresso [media]'] + doc['test']
        if doc['crediti_totali'] == 180:
            aggr['Studenti Laureati [percent]'] = aggr['Studenti Laureati [percent]'] + 1

    aggr['Valutazione Test Incresso [media]'] = round(aggr['Valutazione Test Incresso [media]'] / aggr['N [istanze]'], 2)
    aggr['Studenti Laureati [percent]'] = round((aggr['Studenti Laureati [percent]'] / aggr['N [istanze]']) * 100, 2)

    # media pesata
    aggr['Voto [media pesata]'] = 0
    aggr['Ritardo [semestre, media pesata]'] = 0
    n = 0

    a_a = str(group['_id']['coorte']) + '-' + str(group['_id']['coorte'] + 1)
    for doc in stud.find({'Anno Accademico': a_a}):
        aggr['Voto [media pesata]'] = aggr['Voto [media pesata]'] + doc['Voto [media]'] * doc['N [istanze]']
        aggr['Ritardo [semestre, media pesata]'] = aggr['Ritardo [semestre, media pesata]'] + doc['Ritardo [semestre, media]'] * doc['N [istanze]']
        n = n + doc['N [istanze]']

    aggr['Voto [media pesata]'] = round(aggr['Voto [media pesata]'] / n, 2)
    aggr['Ritardo [semestre, media pesata]'] = round(aggr['Ritardo [semestre, media pesata]'] / n, 2)

    minable_gen.insert_one(aggr)
