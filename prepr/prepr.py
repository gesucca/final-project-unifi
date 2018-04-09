"""Preprocessing steps to form an unique collection ready to be data mined."""

from datetime import datetime
from pymongo import MongoClient

from cleanings import Cleaner, FinalCleaner
from cleanings import QSET_OLD, QSET_GEN

from aggregs import Aggregator

from discretize import discretize
from discretize import VAL_SCORE, STD_DEV, MARKS, ZERO_TO_HUND

from merge import Merger


def main(scheme):
    """Do the whole preprocessing step."""
    teval = scheme.create_collection("teachEval")
    sprod = scheme.create_collection("productStud")
    _pre_clean(scheme, teval)
    _aggreg(scheme.rawStudentsPr1013, sprod)

    teval_d = scheme.create_collection("teval_discrete")
    sprod_d = scheme.create_collection("sprod_discrete")

    discretize(teval, teval_d,
               ['Media', 'Deviazione standard', 'N', 'P<6', 'P>=6'],
               [VAL_SCORE, STD_DEV, ZERO_TO_HUND, ZERO_TO_HUND, ZERO_TO_HUND],
               True
              )

    discretize(sprod, sprod_d,
               ['Media', 'Deviazione standard', 'N', 'P<24', 'P>=24'],
               [MARKS, STD_DEV, ZERO_TO_HUND, ZERO_TO_HUND, ZERO_TO_HUND],
               True
              )

    _merge_attr_teach(scheme.teval_discrete)

    _gen_minable_01(scheme.teval_discrete, scheme.sprod_discrete,
                    scheme.create_collection('minable_01'))

    FinalCleaner(scheme.minable_01).clean([{'old': 'Dataset Provenienza',
                                            'new': 'Anno Accademico'},
                                           {'old': 'Deviazione standard',
                                            'new': 'Std Dev'}],
                                          ['_id', 'Inizio Periodo di Riferimento',
                                           'Fine Periodo di Riferimento'],
                                          ['Insegnamento'])


def _pre_clean(scheme, dest):
    cln = Cleaner(dest)
    cln.set_qset(QSET_OLD)
    cln.clean(scheme.rawTeachingsEv1011, 2010, True)

    cln.set_qset(QSET_GEN)
    cln.clean(scheme.rawTeachingsEv1112, 2011, True)
    cln.clean(scheme.rawTeachingsEv1213, 2012, True)
    cln.clean(scheme.rawTeachingsEv1314, 2013, True)

    cln.drop()


def _aggreg(source, dest):
    agg = Aggregator(source, dest)

    agg.aggregate(datetime(2011, 1, 1), datetime(2011, 12, 31))
    agg.aggregate(datetime(2012, 1, 1), datetime(2012, 12, 31))
    agg.aggregate(datetime(2013, 1, 1), datetime(2013, 12, 31))
    agg.aggregate(datetime(2014, 1, 1), datetime(2014, 12, 31))

    agg.drop()


def _merge_attr_teach(teach_eval):
    mrg = Merger(['Dataset Provenienza', 'Insegnamento'], True)

    mrg.set_gen_keys(['Hash Docente/i',
                      'Inizio Periodo di Riferimento',
                      'Fine Periodo di Riferimento'])
    mrg.set_specific_keys(['Media', 'Deviazione standard', 'P<6', 'P>=6', 'N'])

    mrg.merge_attributes(teach_eval)


def _gen_minable_01(teach_eval, st_prod, dest):
    mrg = Merger(['Inizio Periodo di Riferimento', 'Fine Periodo di Riferimento', 'Insegnamento'],
                 True)
    mrg.set_specific_keys(['N', 'P>=24', 'P<24', 'Media', 'Deviazione standard'])
    mrg.merge_collections(teach_eval, st_prod, 'Produttivita Studenti', dest)


main(MongoClient().exams)
