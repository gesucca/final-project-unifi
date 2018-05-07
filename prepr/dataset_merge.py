from pymongo import MongoClient

from mymodules import merge

scheme = MongoClient().exams
teval = scheme['teachEval_aggr']
sprod = scheme['sprod']
dest = scheme.create_collection("minable")

mrg = merge.Merger(['Anno Accademico', 'Insegnamento'], True)

mrg.set_specific_keys(['N', 'Voto P>=24', 'Voto Medio',
                       'Voto Std Dev', 'Ritardo Medio [sem]', 'Ritardo P>=1sem',
                       ], None, None)

mrg.merge_collections(teval, sprod, 'Prd_ ', dest)

