#!/bin/sh

mongo < mongo_scripts/reset.mongosh

# students productivity csv is already well formatted, I simply import it
mongoimport -d exams -c studentsProd --type csv --file raw_data/prod_stud_10-11-12-13.csv --headerline

# didactic evaluation is a bit more tricky
# need to manipulate a bit the cvs before feeding it to mongoimort
< raw_data/val_didattica_10-11.csv tr "\"" " " | tr "," "." | tr ";" "," | mongoimport -d exams -c teachingsEval --type csv --headerline
< raw_data/val_didattica_11-12.csv tr "\"" " " | tr "," "." | tr ";" "," | mongoimport -d exams -c teachingsEval --type csv --headerline
< raw_data/val_didattica_12-13.csv tr "\"" " " | tr "," "." | tr ";" "," | mongoimport -d exams -c teachingsEval --type csv --headerline
< raw_data/val_didattica_13-14.csv tr "\"" " " | tr "," "." | tr ";" "," | mongoimport -d exams -c teachingsEval --type csv --headerline

# update data to unify keys among them
mongo < mongo_scripts/unify.mongosh
