#!/bin/sh

mongo < reset.mongosh

# students productivity csv is already well formatted, I simply import it
mongoimport -d exams -c studentsProd --type csv --file raw_data/prod_stud_10-11-12-13.csv --headerline

# didactic evaluation is a bit more tricky: those double aphex and semicolons don't fit well mongoimport
# luckly trimming them into nothing works
tr "\"" " " < raw_data/val_didattica_10-11.csv | mongoimport -d exams -c teachingsEval --type csv --headerline
tr "\"" " " < raw_data/val_didattica_11-12.csv | mongoimport -d exams -c teachingsEval --type csv --headerline
tr "\"" " " < raw_data/val_didattica_12-13.csv | mongoimport -d exams -c teachingsEval --type csv --headerline
tr "\"" " " < raw_data/val_didattica_13-14.csv | mongoimport -d exams -c teachingsEval --type csv --headerline

#db.inventory.updateMany(
#   { "qty": { $lt: 50 } }, #where
#   {
#     $set: { "size.uom": "in", status: "P" }
#   }
#)
