from pymongo import MongoClient

scheme = MongoClient().exams
scheme.create_collection('minable_gen')
minable_gen = scheme['minable_gen']

prod = scheme.rawStudentsPr1013
stud = scheme.sprod

for group in prod.aggregate([{"$group": {"_id": {'coorte': '$coorte'}}}]):

    aggr = {'Valutazione Test Ingresso': 0, 'P Laureati': 0, 'N': 0, 'Coorte Immatricolazione': group['_id']['coorte']}

    for doc in prod.find(group['_id']):
        aggr['N'] = aggr['N'] + 1
        aggr['Valutazione Test Ingresso'] = aggr['Valutazione Test Ingresso'] + doc['test']
        if doc['crediti_totali'] == 180:
            aggr['P Laureati'] = aggr['P Laureati'] + 1

    aggr['Valutazione Test Ingresso'] = round(aggr['Valutazione Test Ingresso'] / aggr['N'], 2)
    aggr['P Laureati'] = round((aggr['P Laureati'] / aggr['N']) * 100, 2)

    # media pesata
    aggr['Media Pesata Voti'] = 0
    aggr['Media Pesata Ritardo'] = 0
    n = 0

    a_a = str(group['_id']['coorte']) + '-' + str(group['_id']['coorte'] + 1)
    for doc in stud.find({'Anno Accademico': a_a}):
        aggr['Media Pesata Voti'] = aggr['Media Pesata Voti'] + doc['Voto Medio'] * doc['N']
        aggr['Media Pesata Ritardo'] = aggr['Media Pesata Ritardo'] + doc['Ritardo Medio [sem]'] * doc['N']
        n = n + doc['N']

    aggr['Media Pesata Voti'] = round(aggr['Media Pesata Voti'] / n, 2)
    aggr['Media Pesata Ritardo'] = round(aggr['Media Pesata Ritardo'] / n, 2)

    minable_gen.insert_one(aggr)
