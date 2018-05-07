from pymongo import MongoClient

from mymodules import discretize

import PREPR_PARAMS as pp

scheme = MongoClient().exams
minable = scheme['minable']
minable_discretized = scheme.create_collection("minable_discretized")

discretize.discretize(minable, minable_discretized,
                      ['Val [media pesata]', 'Std Dev [media pesata]', 'N [istanze]', '>= 6', '>= 24',
                       'Voto [media]', 'Ritardo [semestre, media]', '>=1sem'],
                      [pp.VAL_SCORE, pp.STD_DEV, pp.STUDENTS, pp.PERCENT, pp.PERCENT,
                       pp.MARKS, pp.YEARS, pp.PERCENT],
                      False)

