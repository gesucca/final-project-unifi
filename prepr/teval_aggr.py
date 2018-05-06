from pymongo import MongoClient

from mymodules import aggregs

scheme = MongoClient().exams
teval = scheme["teachEval"]

teval_aggr = scheme.create_collection('teachEval_aggr')
aggr = aggregs.ParAggregator(teval, teval_aggr)
aggr.aggregate_par()
aggr.drop()

