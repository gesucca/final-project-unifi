from pymongo import MongoClient

from cleanings import FinalCleaner
from merge import Merger

scheme = MongoClient().exams
teval = scheme['teachEval_pruned']
sprod = scheme['sprod']
dest = scheme.create_collection("merged")

mrg = Merger(['Inizio Periodo di Riferimento', 'Fine Periodo di Riferimento', 'Insegnamento'],
             True)

mrg.set_specific_keys(['N', 'Voto P>=24', 'Voto P<24', 'Voto Medio',
                       'Voto Deviazione standard', 'Ritardo Medio', 'Ritardo P>=1y',
                       'Ritardo P<1y'], None, None)

mrg.merge_collections(teval, sprod, 'Produttivita', dest)

FinalCleaner(dest).clean([{'old': 'Dataset Provenienza',
                           'new': 'Anno Accademico'},
                          {'old': 'Deviazione standard',
                           'new': 'Std Dev'}],
                         ['_id', 'Inizio Periodo di Riferimento',
                          'Fine Periodo di Riferimento', 'P<6', 'P<24', 'P<1y'],
                         ['Insegnamento'])

