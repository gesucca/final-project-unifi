import operator
import os

from datetime import datetime
from pymongo import MongoClient

def only_the_dates(doc):
    keys_to_delete = [];

    for key in doc.keys():
        if "data_" not in key:
            keys_to_delete.append(key)

    for key in keys_to_delete:
        del doc[key]

    return doc

def datetime_sorted(doc):
    keys_to_delete = [];

    for key in doc.keys():
        if doc[key] != 0 and doc[key] != '0000-00-00':
            doc[key] = datetime.strptime(doc[key], '%Y-%m-%d')
        else:
            keys_to_delete.append(key)

    for key in keys_to_delete:
        del doc[key]

    sorted_list = sorted(doc, key=doc.get)

    return sorted_list

os.chdir('../datasets')

with open('seq_stud.arff', 'w') as the_file:
    the_file.write('@relation students_career\n')
    the_file.write('\n')
    the_file.write('@attribute StudentID {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207}\n')
    the_file.write('@attribute ExamID {1_ASD, 1_ADE, 1_AN1, 1_PRG, 1_MDL, 1_ENG, 2_1_ALG, 2_1_MDP, 2_1_CPS, 2_1_PRC, 2_2_AN2, 2_2_FIG, 2_2_BDS, 2_2_SOP, 3_1_REC, 3_1_INC, 3_1_CAZ, 3_2_CAN, 3_2_ITE, 3_2_CES}\n')
    the_file.write('\n')
    the_file.write('@data\n')

scheme = MongoClient().exams
coll = scheme['rawStudentsPr1013']
studentID = 1

for doc in coll.find():

    doc = only_the_dates(doc)
    lst = datetime_sorted(doc)

    for exam in lst:
        with open('seq_stud.arff', 'a') as the_file:
            the_file.write(str(studentID) + ',' + exam + '\n')

    studentID = studentID + 1

# fix those names
with open('seq_stud.arff', 'r') as file :
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

with open('seq_stud.arff', 'w') as file:
    file.write(filedata)
