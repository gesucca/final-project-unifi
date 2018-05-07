#!/bin/sh

mongo < list_attr.mongosh > _exp_fields.txt
sed -i -e 's/	"//g' _exp_fields.txt
sed -i -e 's/"//g' _exp_fields.txt
sed -i -e 's/,//g' _exp_fields.txt
sed -i -e '1,16d' _exp_fields.txt # mongo client echoed stuff
sed -i -e 's/_id//g' _exp_fields.txt
sed -i -e 's/]//g' _exp_fields.txt
sed -i -e 's/bye//g' _exp_fields.txt
sed -i -e '/^\s*$/d' _exp_fields.txt # empty lines

yes | rm -rf datasets
mkdir datasets

mongoexport --db exams --collection minable --type=csv --fieldFile=_exp_fields.txt > datasets/teachings.csv
mongoexport --db exams --collection minable_discretized --type=csv --fieldFile=_exp_fields.txt > datasets/teachings_disc.csv
mongoexport --db exams --collection minable_gen --type=csv --fieldFile=_exp_fields_gen.txt > datasets/gen.csv