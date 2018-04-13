"""Preprocessing steps to form an unique collection ready to be data mined."""

from datetime import datetime
from pymongo import MongoClient

from cleanings import Cleaner, FinalCleaner
from cleanings import QSET_OLD, QSET_GEN

from aggregs import StudAggregator, ParAggregator

from discretize import discretize
from discretize import VAL_SCORE, STD_DEV, MARKS, ZERO_TO_HUND

from merge import Merger


def main(scheme):
    """Do the whole preprocessing step."""

    teval = _teaching_evaluation(scheme)
    sprod = _students_productivity(scheme)

    minable = scheme.create_collection("minable")
    _final_merge(minable, teval, sprod)

    _number_instance_pruning(minable)

    minable_discretized = scheme.create_collection("minable_discretized")
    discretize(minable, minable_discretized,
               ["Media", 'Std dev', 'N', 'P<6', 'P>=6', 'P<24', 'P>=24', 'Voto Medio'],
               [VAL_SCORE, STD_DEV, ZERO_TO_HUND, ZERO_TO_HUND, ZERO_TO_HUND,
                ZERO_TO_HUND, ZERO_TO_HUND, MARKS],
               False
              )


def _teaching_evaluation(scheme):

    teval = scheme.create_collection("teachEval")

    cln = Cleaner(teval)
    cln.set_qset(QSET_OLD)
    cln.clean(scheme.rawTeachingsEv1011, 2010, True)
    cln.set_qset(QSET_GEN)
    cln.clean(scheme.rawTeachingsEv1112, 2011, True)
    cln.clean(scheme.rawTeachingsEv1213, 2012, True)
    cln.clean(scheme.rawTeachingsEv1314, 2013, True)
    cln.drop()

    teval_aggr = scheme.create_collection('teachEval_aggr')
    aggr = ParAggregator(teval, teval_aggr)
    aggr.aggregate_par()
    aggr.drop()

    mrg = Merger(['Dataset Provenienza', 'Insegnamento'], True)
    mrg.set_gen_keys(['Hash Docente/i',
                      'Inizio Periodo di Riferimento',
                      'Fine Periodo di Riferimento'])
    mrg.set_specific_keys(['Media', 'Deviazione standard', 'P<6', 'P>=6', 'N'],
                          'Paragrafo', 'Val_ ')
    mrg.merge_attributes(teval_aggr)

    teval_aggr = _teach_attribute_pruning(scheme, teval_aggr, True)

    return teval_aggr


def _teach_attribute_pruning(scheme, collection, delete):

    pruned = scheme.create_collection(collection.name + '_pruned')

    for doc in collection.find():

        n_mean = 0
        n_n = 0
        for key in list(doc.keys()):
            if '- N' in key and doc[key] != '<5':
                n_mean = n_mean + doc[key]
                del doc[key]
                n_n = n_n + 1

        if n_n != 0:
            doc['Val_ N'] = int(n_mean / n_n)
            if delete:
                collection.delete_one(doc)
            pruned.insert_one(doc)

    if delete:
        collection.drop()

    return pruned


def _students_productivity(scheme):
    sprod = scheme.create_collection("sprod")
    agg = StudAggregator(scheme.rawStudentsPr1013, sprod)
    agg.aggregate_stud(datetime(2011, 1, 1), datetime(2011, 12, 31))
    agg.aggregate_stud(datetime(2012, 1, 1), datetime(2012, 12, 31))
    agg.aggregate_stud(datetime(2013, 1, 1), datetime(2013, 12, 31))
    agg.aggregate_stud(datetime(2014, 1, 1), datetime(2014, 12, 31))
    agg.drop()

    return sprod


def _final_merge(dest, teval, sprod):

    mrg = Merger(['Inizio Periodo di Riferimento', 'Fine Periodo di Riferimento', 'Insegnamento'],
                 True)
    mrg.set_specific_keys(['N', 'P>=24', 'P<24', 'Voto Medio', 'Deviazione standard'], None, None)
    mrg.merge_collections(teval, sprod, 'Prd_ Studenti', dest)

    FinalCleaner(dest).clean([{'old': 'Dataset Provenienza',
                               'new': 'Anno Accademico'},
                              {'old': 'Deviazione standard',
                               'new': 'Std Dev'}],
                             ['_id', 'Inizio Periodo di Riferimento',
                              'Fine Periodo di Riferimento'],
                             ['Insegnamento'])


def _number_instance_pruning(minable_coll):

    for doc in minable_coll.find():
        try:
            if abs(doc['Prd_ Studenti - N'] - doc['Val_ N']) > 20:
                minable_coll.delete_one(doc)
        except TypeError:
            if doc['Prd_ Studenti - N'] != doc['Val_ N']:
                minable_coll.delete_one(doc)


# launch this on the global scope
main(MongoClient().exams)
