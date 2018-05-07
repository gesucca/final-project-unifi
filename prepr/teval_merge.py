from pymongo import MongoClient
from mymodules import merge

mrg = merge.Merger(['Anno Accademico', 'Insegnamento'], True)

mrg.set_gen_keys(['Hash Docente/i'])

mrg.set_specific_keys(['Val [media pesata]', 'Std Dev [media pesata]', 'Val >= 6 [percent]', 'N [istanze]'],
                      'Paragrafo', '')

mrg.merge_attributes(MongoClient().exams['teachEval_aggr'])
