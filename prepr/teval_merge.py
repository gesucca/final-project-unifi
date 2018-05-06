from pymongo import MongoClient
from mymodules import merge

mrg = merge.Merger(['Dataset Provenienza', 'Insegnamento'], True)

mrg.set_gen_keys(['Hash Docente/i',
                  'Inizio Periodo di Riferimento',
                  'Fine Periodo di Riferimento'])

mrg.set_specific_keys(['Media', 'Deviazione standard', 'P<6', 'P>=6', 'N'],
                      'Paragrafo', 'Val_ ')

mrg.merge_attributes(MongoClient().exams['teachEval_aggr'])

