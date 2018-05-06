from pymongo import MongoClient

from mymodules import cleanings

cleanings.FinalCleaner(MongoClient().exams['minable']).clean([{'old': 'Dataset Provenienza',
                                                               'new': 'Anno Accademico'},
                                                              {'old': 'Deviazione standard',
                                                               'new': 'Std Dev'}],
                                                             ['_id', 'Inizio Periodo di Riferimento',
                                                              'Fine Periodo di Riferimento', 'P<6', 'P<24', 'P<1y'],
                                                             ['Insegnamento'])

