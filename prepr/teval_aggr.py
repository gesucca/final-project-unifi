from pymongo import MongoClient

from aggregs import ParAggregator

scheme = MongoClient().exams
teval = scheme["teachEval"]

teval_aggr = scheme.create_collection('teachEval_aggr')
aggr = ParAggregator(teval, teval_aggr)
aggr.aggregate_par()
aggr.drop()

