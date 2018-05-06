from pymongo import MongoClient

from mymodules import discretize

import PREPR_PARAMS as pp

scheme = MongoClient().exams
minable = scheme['minable']
minable_discretized = scheme.create_collection("minable_discretized")

discretize.discretize(minable, minable_discretized,
                      ['Media', 'Std Dev', 'N', 'P>=6', 'P>=24',
                      'Voto Medio', 'Ritardo Medio', 'P>=1y'],
                      [pp.VAL_SCORE, pp.STD_DEV, pp.STUDENTS, pp.PERCENT, pp.PERCENT,
                       pp.MARKS, pp.YEARS, pp.PERCENT],
                      False)

