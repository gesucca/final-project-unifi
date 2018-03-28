#!/bin/sh
mongo exams --eval "db.dropDatabase()"
sh import.sh
python3 prepr.py

# prova
# rm prova.csv
# mongoexport --db exams --collection sprod_discrete --type=csv --fieldFile=_exp_fields.txt > prova.csv
