from pymongo import MongoClient

from mymodules import discretize

import PREPR_PARAMS as PP

scheme = MongoClient().exams
scheme.create_collection("minable_discretized")
scheme.create_collection("minable_min_discretized")

keys_substrings = ['Val [media pesata]', 'Std Dev [media pesata]', '[std dev]', 'N [istanze]',
                   '>= 6', '>= 24', 'Voto [media]', 'Ritardo [semestre, media]', '>=1sem']

ranges = [PP.VAL_SCORE, PP.STD_DEV, PP.STD_DEV, PP.STUDENTS,
          PP.PERCENT, PP.PERCENT, PP.MARKS, PP.YEARS, PP.PERCENT]

discretize.discretize(scheme.minable, scheme.minable_discretized, keys_substrings, ranges, False)
discretize.discretize(scheme.minable_min, scheme.minable_min_discretized, keys_substrings, ranges, False)
