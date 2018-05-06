from pymongo import MongoClient

from mymodules import merge

scheme = MongoClient().exams
teval = scheme['teachEval_pruned']
sprod = scheme['sprod']
dest = scheme.create_collection("minable")

mrg = merge.Merger(['Inizio Periodo di Riferimento', 'Fine Periodo di Riferimento', 'Insegnamento'],
                   True)

mrg.set_specific_keys(['N', 'Voto P>=24', 'Voto P<24', 'Voto Medio',
                       'Voto Deviazione standard', 'Ritardo Medio', 'Ritardo P>=1y',
                       'Ritardo P<1y'], None, None)

mrg.merge_collections(teval, sprod, 'Produttivita', dest)

