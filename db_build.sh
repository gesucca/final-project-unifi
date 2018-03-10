#!/bin/sh

mongo < reset.mongosh

mongoimport -d exams -c product --type csv --file raw_data/prod_stud_10-11-12-13.csv --headerline
