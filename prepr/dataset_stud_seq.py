import operator
import os

from datetime import datetime
from pymongo import MongoClient

def only_the_dates(doc):
    keys_to_delete = []

    for key in doc.keys():
        if "data_" not in key:
            keys_to_delete.append(key)

    for key in keys_to_delete:
        del doc[key]

    return doc


def datetime_sorted(doc):
    keys_to_delete = []

    for key in doc.keys():
        if doc[key] != 0 and doc[key] != '0000-00-00':
            doc[key] = datetime.strptime(doc[key], '%Y-%m-%d')
        else:
            keys_to_delete.append(key)

    for key in keys_to_delete:
        del doc[key]

    sorted_list = sorted(doc, key=doc.get)

    return sorted_list


def fix_names(filename):
    with open(filename, 'r') as file :
        filedata = file.read()

    filedata = filedata.replace('data_ANII', '2_2_AN2')
    filedata = filedata.replace('data_FIS', '2_2_FIG')
    filedata = filedata.replace('data_BDSI', '2_2_BDS')
    filedata = filedata.replace('data_SO', '2_2_SOP')

    filedata = filedata.replace('data_ASD', '1_ASD')
    filedata = filedata.replace('data_ARC', '1_ADE')
    filedata = filedata.replace('data_ANI', '1_AN1')
    filedata = filedata.replace('data_PRG', '1_PRG')
    filedata = filedata.replace('data_MDL', '1_MDL')
    filedata = filedata.replace('data_INGLESE', '1_ENG')

    filedata = filedata.replace('data_ALG', '2_1_ALG')
    filedata = filedata.replace('data_MP', '2_1_MDP')
    filedata = filedata.replace('data_CPS', '2_1_CPS')
    filedata = filedata.replace('data_PC', '2_1_PRC')

    filedata = filedata.replace('data_RETI', '3_1_REC')
    filedata = filedata.replace('data_IntC', '3_1_INC')
    filedata = filedata.replace('data_CAz', '3_1_CAZ')

    filedata = filedata.replace('data_CAL', '3_2_CAN')
    filedata = filedata.replace('data_IT', '3_2_ITE')
    filedata = filedata.replace('data_CS', '3_2_CES')

    with open(filename, 'w') as file:
        file.write(filedata)

def add_ids(filename, id):
    with open(filename, 'r') as file :
        filedata = file.read()

    id_string = '{'

    for i in range(1, id):
        id_string = id_string + str(i) + ', '

    id_string = id_string[:-2] # remove last comma
    id_string = id_string + '}'

    filedata = filedata.replace('{--ADD IDs--}', id_string)

    with open(filename, 'w') as file:
        file.write(filedata)


def init_file(filename):
    with open(filename, 'w') as the_file:
        the_file.write('@relation students_career\n')
        the_file.write('\n')
        the_file.write('@attribute StudentID {--ADD IDs--}\n')
        the_file.write('@attribute ExamID {1_ASD, 1_ADE, 1_AN1, 1_PRG, 1_MDL, 1_ENG, 2_1_ALG, 2_1_MDP, 2_1_CPS, 2_1_PRC, 2_2_AN2, 2_2_FIG, 2_2_BDS, 2_2_SOP, 3_1_REC, 3_1_INC, 3_1_CAZ, 3_2_CAN, 3_2_ITE, 3_2_CES}\n')
        the_file.write('\n')
        the_file.write('@data\n')


os.chdir('../datasets')

init_file('seq_stud_all.arff')
init_file('seq_stud_2010.arff')
init_file('seq_stud_2011.arff')
init_file('seq_stud_2012.arff')
init_file('seq_stud_2013.arff')

scheme = MongoClient().exams
coll = scheme['rawStudentsPr1013']
studentID = {'ALL': 1, '2010': 1, '2011': 1, '2012': 1, '2013': 1}

for doc in coll.find():

    coorte = doc['coorte']

    lst = datetime_sorted(only_the_dates(doc))

    for exam in lst:
            with open('seq_stud_all.arff', 'a') as the_file:
                the_file.write(str(studentID['ALL']) + ',' + exam + '\n')
    studentID['ALL'] = studentID['ALL'] +1

    if coorte == 2010:
        for exam in lst:
            with open('seq_stud_2010.arff', 'a') as the_file:
                the_file.write(str(studentID['2010']) + ',' + exam + '\n')
        studentID['2010'] = studentID['2010'] + 1

    if coorte == 2011:
        for exam in lst:
            with open('seq_stud_2011.arff', 'a') as the_file:
                the_file.write(str(studentID['2011']) + ',' + exam + '\n')
        studentID['2011'] = studentID['2011'] + 1

    if coorte == 2012:
        for exam in lst:
            with open('seq_stud_2012.arff', 'a') as the_file:
                the_file.write(str(studentID['2012']) + ',' + exam + '\n')
        studentID['2012'] = studentID['2012'] + 1

    if coorte == 2013:
        for exam in lst:
            with open('seq_stud_2013.arff', 'a') as the_file:
                the_file.write(str(studentID['2013']) + ',' + exam + '\n')
        studentID['2013'] = studentID['2013'] + 1

fix_names('seq_stud_all.arff')
add_ids('seq_stud_all.arff', studentID['ALL'])
fix_names('seq_stud_2010.arff')
add_ids('seq_stud_2010.arff', studentID['2010'])
fix_names('seq_stud_2011.arff')
add_ids('seq_stud_2011.arff', studentID['2011'])
fix_names('seq_stud_2012.arff')
add_ids('seq_stud_2012.arff', studentID['2012'])
fix_names('seq_stud_2013.arff')
add_ids('seq_stud_2013.arff', studentID['2013'])
