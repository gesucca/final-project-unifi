from datetime import datetime
from pymongo import MongoClient

from mymodules import aggregs

scheme = MongoClient().exams
sprod = scheme.create_collection("sprod")

agg = aggregs.StudAggregator(scheme.rawStudentsPr1013, sprod)

agg.aggregate_stud(datetime(2011, 1, 1), datetime(2011, 12, 31))
agg.aggregate_stud(datetime(2012, 1, 1), datetime(2012, 12, 31))
agg.aggregate_stud(datetime(2013, 1, 1), datetime(2013, 12, 31))
agg.aggregate_stud(datetime(2014, 1, 1), datetime(2014, 12, 31))

agg.drop()

