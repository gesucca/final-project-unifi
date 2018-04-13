#!/bin/sh
mongo exams --eval "db.dropDatabase()"
sh import.sh

python3 main_prepr.py

yes | rm ../mining/minable.csv
yes | rm ../mining/minable_discretized.csv
mongoexport --db exams --collection minable --type=csv --fieldFile=_exp_fields.txt > ../mining/minable.csv
mongoexport --db exams --collection minable_discretized --type=csv --fieldFile=_exp_fields.txt > ../mining/minable_discretized.csv
