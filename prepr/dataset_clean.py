from pymongo import MongoClient

from mymodules import cleanings

coll = MongoClient().exams['minable']

for doc in coll.find():

    cleaned = False
    old_doc = doc

    for key in list(doc.keys()):
        if doc[key] == 'n.c.':
            del doc[key]
            cleaned = True

    if cleaned:
        coll.delete_one(old_doc)
        coll.insert_one(doc)

cleanings.FinalCleaner(coll).clean([], [], ['Insegnamento'])

MongoClient().exams['rawStudentsPr1013'].drop()
MongoClient().exams['teachEval_aggr'].drop()
MongoClient().exams['sprod'].drop()
