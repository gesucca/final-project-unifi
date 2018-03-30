#!/bin/sh
mongo exams --eval "db.dropDatabase()"
sh import.sh
python3 prepr.py

mongoexport --db exams --collection minable --type=csv --fieldFile=_exp_fields.txt > ../PREPROCESSED.csv
