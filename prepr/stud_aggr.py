from pymongo import MongoClient

from mymodules import aggregs

scheme = MongoClient().exams
sprod = scheme.create_collection("sprod")

agg = aggregs.StudAggregator(scheme.rawStudentsPr1013, sprod)

agg.aggregate_stud('2010')
agg.aggregate_stud('2011')
agg.aggregate_stud('2012')
agg.aggregate_stud('2013')

# agg.drop()
