#!/bin/sh
mongo exams --eval "db.dropDatabase()"
sh import.sh

python3 main_prepr.py

sh export.sh
