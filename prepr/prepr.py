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

    collections = _common(scheme)

    _spec_dataset_01(scheme, collections)
    _spec_dataset_02(scheme, collections)
    _spec_dataset_03(scheme) # simple cleaning of 02

    for coll in scheme.collection_names():
        if 'minable' not in coll:
            scheme[coll].drop()


def _common(scheme):
    teval = scheme.create_collection("teachEval")
    sprod = scheme.create_collection("productStud")

    _pre_clean(scheme, teval)
    _aggreg(scheme.rawStudentsPr1013, sprod)

    sprod_d = scheme.create_collection("sprod_discrete")
    discretize(sprod, sprod_d,
               ['Media', 'Deviazione standard', 'N', 'P<24', 'P>=24'],
               [MARKS, STD_DEV, ZERO_TO_HUND, ZERO_TO_HUND, ZERO_TO_HUND],
               True
              )

    return [teval, sprod_d]


def _spec_dataset_01(scheme, collections):

    sprod_d = collections[1]
    teval_d = scheme.create_collection("teval_discrete")

    discretize(collections[0], teval_d,
               ['Media', 'Deviazione standard', 'N', 'P<6', 'P>=6'],
               [VAL_SCORE, STD_DEV, ZERO_TO_HUND, ZERO_TO_HUND, ZERO_TO_HUND],
               False # I will need it later
              )

    _merge_attr_teach(teval_d, 'Oggetto Valutazione')

    _gen_minable(teval_d, sprod_d,
                 scheme.create_collection('minable_01'), False) # as before


def _spec_dataset_02(scheme, collections):

    teach = collections[0]
    sprod_d = collections[1]

    teach_a = scheme.create_collection('teval_par_aggr')
    aggr = ParAggregator(teach, teach_a)
    aggr.aggregate_par()
    aggr.drop()

    teach_d = scheme.create_collection('teval_aggr_discrete')
    discretize(teach_a, teach_d,
               ['Media', 'Deviazione standard', 'N', 'P<6', 'P>=6'],
               [VAL_SCORE, STD_DEV, ZERO_TO_HUND, ZERO_TO_HUND, ZERO_TO_HUND],
               True
              )

    _merge_attr_teach(teach_d, 'Paragrafo')
    _gen_minable(teach_d, sprod_d, scheme.create_collection('minable_02'), True)


def _spec_dataset_03(scheme):

    minable = scheme.create_collection("minable_03")

    # so silly I simply do it here
    for doc in scheme.minable_02.find():
        # save this
        doc["N Studenti Produttivita"] = doc.pop("Produttivita Studenti - N")

        try: # Ns are all the same, but eval scheme is different...
            doc["temp"] = doc["Aspetti specifici del Corso di Studi - N"]
        except KeyError:
            doc["temp"] = doc["Organizzazione Insegnamento - N"]

        keys = list(doc.keys())
        for key in keys:
            if " - N" in key:
                del doc[key]
        doc["N Valutazioni Didattica"] = doc.pop("temp")

        # ulterior pruning: only precise matching values
        if doc["N Valutazioni Didattica"] == doc["N Studenti Produttivita"]:
            doc["Numero Studenti"] = doc["N Studenti Produttivita"]
            del doc["N Studenti Produttivita"]
            del doc["N Valutazioni Didattica"]
            minable.insert_one(doc)


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
    agg = StudAggregator(source, dest)

    agg.aggregate_stud(datetime(2011, 1, 1), datetime(2011, 12, 31))
    agg.aggregate_stud(datetime(2012, 1, 1), datetime(2012, 12, 31))
    agg.aggregate_stud(datetime(2013, 1, 1), datetime(2013, 12, 31))
    agg.aggregate_stud(datetime(2014, 1, 1), datetime(2014, 12, 31))

    agg.drop()


def _merge_attr_teach(teach_eval, discriminant):
    mrg = Merger(['Dataset Provenienza', 'Insegnamento'], True)

    mrg.set_gen_keys(['Hash Docente/i',
                      'Inizio Periodo di Riferimento',
                      'Fine Periodo di Riferimento'])
    mrg.set_specific_keys(['Media', 'Deviazione standard', 'P<6', 'P>=6', 'N'],
                          discriminant)

    mrg.merge_attributes(teach_eval)


def _gen_minable(teach_eval, st_prod, dest, delete):
    mrg = Merger(['Inizio Periodo di Riferimento', 'Fine Periodo di Riferimento', 'Insegnamento'],
                 delete)
    mrg.set_specific_keys(['N', 'P>=24', 'P<24', 'Media', 'Deviazione standard'], None)
    mrg.merge_collections(teach_eval, st_prod, 'Produttivita Studenti', dest)

    FinalCleaner(dest).clean([{'old': 'Dataset Provenienza',
                               'new': 'Anno Accademico'},
                              {'old': 'Deviazione standard',
                               'new': 'Std Dev'}],
                             ['_id', 'Inizio Periodo di Riferimento',
                              'Fine Periodo di Riferimento'],
                             ['Insegnamento'])


main(MongoClient().exams)
