from pymongo import MongoClient
from mymodules import merge

mrg = merge.Merger(['Anno Accademico', 'Insegnamento'], True)

mrg.set_gen_keys(['Hash Docente/i'])

mrg.set_specific_keys(['Media', 'Std Dev', 'P>=6', 'N'],
                      'Paragrafo', 'Val_ ')

mrg.merge_attributes(MongoClient().exams['teachEval_aggr'])
