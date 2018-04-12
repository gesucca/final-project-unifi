#!/bin/sh
mongo exams --eval "db.dropDatabase()"
sh import.sh

python3 prepr.py

yes | rm -rf ../prepr_out
mkdir ../prepr_out
mongoexport --db exams --collection minable_01 --type=csv --fieldFile=_exp_fields_01.txt > ../prepr_out/01.csv
mongoexport --db exams --collection minable_02 --type=csv --fieldFile=_exp_fields_02.txt > ../prepr_out/02.csv
mongoexport --db exams --collection minable_03 --type=csv --fieldFile=_exp_fields_03.txt > ../prepr_out/03.csv
