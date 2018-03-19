#!/bin/sh
mongo exams --eval "db.dropDatabase()"
sh import.sh
python3 prepr.py
