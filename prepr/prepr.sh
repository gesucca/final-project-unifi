#!/bin/sh
mongo exams --eval "db.dropDatabase()"
sh import.sh
python3 prepr.py

rm ..prepr_out/*.csv
mongoexport --db exams --collection minable_01 --type=csv --fieldFile=_exp_fields_01.txt > ../prepr_out/01.csv
