from pymongo import MongoClient

from mymodules import merge

scheme = MongoClient().exams
teval = scheme['teachEval_aggr']
sprod = scheme['sprod']
dest = scheme.create_collection("minable")

mrg = merge.Merger(['Anno Accademico', 'Insegnamento'], False)

mrg.set_specific_keys(['N [istanze]', 'Voto >= 24 [perc]', 'Voto [media]',
                       'Voto [std dev]', 'Ritardo [semestre, media]', 'Ritardo >=1sem [percent]',
                       ], None, None)

mrg.merge_collections(teval, sprod, 'Produttivita Studenti', dest)

