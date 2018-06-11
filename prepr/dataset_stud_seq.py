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

# BEWARE: bad code follows (and bad code preceeded, but whatever)

os.chdir('../datasets')

with open('seq_stud_2010_liceo.arff', 'w') as the_file:
    the_file.write('@relation students_career\n')
    the_file.write('\n')
    the_file.write('@attribute StudentID {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}\n')
    the_file.write('@attribute ExamID {1_ASD, 1_ADE, 1_AN1, 1_PRG, 1_MDL, 1_ENG, 2_1_ALG, 2_1_MDP, 2_1_CPS, 2_1_PRC, 2_2_AN2, 2_2_FIG, 2_2_BDS, 2_2_SOP, 3_1_REC, 3_1_INC, 3_1_CAZ, 3_2_CAN, 3_2_ITE, 3_2_CES}\n')
    the_file.write('\n')
    the_file.write('@data\n')

with open('seq_stud_2010_ist_tecn.arff', 'w') as the_file:
    the_file.write('@relation students_career\n')
    the_file.write('\n')
    the_file.write('@attribute StudentID {1, 2, 3, 4, 5, 6, 7, 8, 9}\n')
    the_file.write('@attribute ExamID {1_ASD, 1_ADE, 1_AN1, 1_PRG, 1_MDL, 1_ENG, 2_1_ALG, 2_1_MDP, 2_1_CPS, 2_1_PRC, 2_2_AN2, 2_2_FIG, 2_2_BDS, 2_2_SOP, 3_1_REC, 3_1_INC, 3_1_CAZ, 3_2_CAN, 3_2_ITE, 3_2_CES}\n')
    the_file.write('\n')
    the_file.write('@data\n')

with open('seq_stud_2011_liceo.arff', 'w') as the_file:
    the_file.write('@relation students_career\n')
    the_file.write('\n')
    the_file.write('@attribute StudentID {1, 2, 3, 4, 5, 6, 7, 8}\n')
    the_file.write('@attribute ExamID {1_ASD, 1_ADE, 1_AN1, 1_PRG, 1_MDL, 1_ENG, 2_1_ALG, 2_1_MDP, 2_1_CPS, 2_1_PRC, 2_2_AN2, 2_2_FIG, 2_2_BDS, 2_2_SOP, 3_1_REC, 3_1_INC, 3_1_CAZ, 3_2_CAN, 3_2_ITE, 3_2_CES}\n')
    the_file.write('\n')
    the_file.write('@data\n')

with open('seq_stud_2011_ist_tecn.arff', 'w') as the_file:
    the_file.write('@relation students_career\n')
    the_file.write('\n')
    the_file.write('@attribute StudentID {1, 2, 3}\n')
    the_file.write('@attribute ExamID {1_ASD, 1_ADE, 1_AN1, 1_PRG, 1_MDL, 1_ENG, 2_1_ALG, 2_1_MDP, 2_1_CPS, 2_1_PRC, 2_2_AN2, 2_2_FIG, 2_2_BDS, 2_2_SOP, 3_1_REC, 3_1_INC, 3_1_CAZ, 3_2_CAN, 3_2_ITE, 3_2_CES}\n')
    the_file.write('\n')
    the_file.write('@data\n')

with open('seq_stud_2012_liceo.arff', 'w') as the_file:
    the_file.write('@relation students_career\n')
    the_file.write('\n')
    the_file.write('@attribute StudentID {1, 2}\n')
    the_file.write('@attribute ExamID {1_ASD, 1_ADE, 1_AN1, 1_PRG, 1_MDL, 1_ENG, 2_1_ALG, 2_1_MDP, 2_1_CPS, 2_1_PRC, 2_2_AN2, 2_2_FIG, 2_2_BDS, 2_2_SOP, 3_1_REC, 3_1_INC, 3_1_CAZ, 3_2_CAN, 3_2_ITE, 3_2_CES}\n')
    the_file.write('\n')
    the_file.write('@data\n')

with open('seq_stud_2012_ist_tecn.arff', 'w') as the_file:
    the_file.write('@relation students_career\n')
    the_file.write('\n')
    the_file.write('@attribute StudentID {1, 2, 3, 4, 5, 6, 7}\n')
    the_file.write('@attribute ExamID {1_ASD, 1_ADE, 1_AN1, 1_PRG, 1_MDL, 1_ENG, 2_1_ALG, 2_1_MDP, 2_1_CPS, 2_1_PRC, 2_2_AN2, 2_2_FIG, 2_2_BDS, 2_2_SOP, 3_1_REC, 3_1_INC, 3_1_CAZ, 3_2_CAN, 3_2_ITE, 3_2_CES}\n')
    the_file.write('\n')
    the_file.write('@data\n')

with open('seq_stud_2013_liceo.arff', 'w') as the_file:
    the_file.write('@relation students_career\n')
    the_file.write('\n')
    the_file.write('@attribute StudentID {1, 2, 3, 4, 5}\n')
    the_file.write('@attribute ExamID {1_ASD, 1_ADE, 1_AN1, 1_PRG, 1_MDL, 1_ENG, 2_1_ALG, 2_1_MDP, 2_1_CPS, 2_1_PRC, 2_2_AN2, 2_2_FIG, 2_2_BDS, 2_2_SOP, 3_1_REC, 3_1_INC, 3_1_CAZ, 3_2_CAN, 3_2_ITE, 3_2_CES}\n')
    the_file.write('\n')
    the_file.write('@data\n')

with open('seq_stud_2013_ist_tecn.arff', 'w') as the_file:
    the_file.write('@relation students_career\n')
    the_file.write('\n')
    the_file.write('@attribute StudentID {1, 2, 3, 4, 5, 6}\n')
    the_file.write('@attribute ExamID {1_ASD, 1_ADE, 1_AN1, 1_PRG, 1_MDL, 1_ENG, 2_1_ALG, 2_1_MDP, 2_1_CPS, 2_1_PRC, 2_2_AN2, 2_2_FIG, 2_2_BDS, 2_2_SOP, 3_1_REC, 3_1_INC, 3_1_CAZ, 3_2_CAN, 3_2_ITE, 3_2_CES}\n')
    the_file.write('\n')
    the_file.write('@data\n')

scheme = MongoClient().exams
coll = scheme['rawStudentsPr1013']
studentID = {'2010_L': 1, '2010_I': 1, '2011_L': 1, '2011_I': 1, '2012_L': 1, '2012_I': 1, '2013_L': 1, '2013_I': 1}

for doc in coll.find():

    # beware of the pruning criterias
    coorte = doc['coorte']
    scuola = doc['tipo_scuola']
    crediti = doc['crediti_totali']
    voto = doc['voto_medio']

    lst = datetime_sorted(only_the_dates(doc))

    if crediti >= 60 and coorte == 2010 and 'L' in scuola:
        for exam in lst:
            with open('seq_stud_2010_liceo.arff', 'a') as the_file:
                the_file.write(str(studentID['2010_L']) + ',' + exam + '\n')

        studentID['2010_L'] = studentID['2010_L'] + 1

    if crediti >= 60 and coorte == 2010 and 'T' in scuola:
        for exam in lst:
            with open('seq_stud_2010_ist_tecn.arff', 'a') as the_file:
                the_file.write(str(studentID['2010_I']) + ',' + exam + '\n')

        studentID['2010_I'] = studentID['2010_I'] + 1

    if crediti >= 120 and coorte == 2011 and 'L' in scuola:
        for exam in lst:
            with open('seq_stud_2011_liceo.arff', 'a') as the_file:
                the_file.write(str(studentID['2011_L']) + ',' + exam + '\n')

        studentID['2011_L'] = studentID['2011_L'] + 1

    if crediti >= 120 and coorte == 2011 and 'T' in scuola:
        for exam in lst:
            with open('seq_stud_2011_ist_tecn.arff', 'a') as the_file:
                the_file.write(str(studentID['2011_I']) + ',' + exam + '\n')

        studentID['2011_I'] = studentID['2011_I'] + 1

    if crediti >= 180 and voto >= 26 and coorte == 2012 and 'L' in scuola:
        for exam in lst:
            with open('seq_stud_2012_liceo.arff', 'a') as the_file:
                the_file.write(str(studentID['2012_L']) + ',' + exam + '\n')

        studentID['2012_L'] = studentID['2012_L'] + 1

    if crediti >= 180 and voto >= 26 and coorte == 2012 and 'T' in scuola:
        for exam in lst:
            with open('seq_stud_2012_ist_tecn.arff', 'a') as the_file:
                the_file.write(str(studentID['2012_I']) + ',' + exam + '\n')

        studentID['2012_I'] = studentID['2012_I'] + 1

    if crediti >= 160 and coorte == 2013 and 'L' in scuola:
        for exam in lst:
            with open('seq_stud_2013_liceo.arff', 'a') as the_file:
                the_file.write(str(studentID['2013_L']) + ',' + exam + '\n')

        studentID['2013_L'] = studentID['2013_L'] + 1

    if crediti >= 160 and coorte == 2013 and 'T' in scuola:
        for exam in lst:
            with open('seq_stud_2013_ist_tecn.arff', 'a') as the_file:
                the_file.write(str(studentID['2013_I']) + ',' + exam + '\n')

        studentID['2013_I'] = studentID['2013_I'] + 1

fix_names('seq_stud_2010_liceo.arff')
fix_names('seq_stud_2010_ist_tecn.arff')
fix_names('seq_stud_2011_liceo.arff')
fix_names('seq_stud_2011_ist_tecn.arff')
fix_names('seq_stud_2012_liceo.arff')
fix_names('seq_stud_2012_ist_tecn.arff')
fix_names('seq_stud_2013_liceo.arff')
fix_names('seq_stud_2013_ist_tecn.arff')
