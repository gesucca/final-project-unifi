DB = exams
SCHEME= MongoClient().exams
PRDIR= cd prepr &&
PY= python3

# useful to spot bad coded modules
TIME= /usr/bin/time --format=%e

all: export

reset_db:
	mongo $(DB) --eval "db.dropDatabase()"

import: reset_db
	$(PRDIR) sh import.sh

#
# teaching evaluation recipes
#
teval: teval_merge

teval_clean: import
	$(PRDIR) $(TIME) $(PY) teval_clean.py

teval_aggr: teval_clean
	$(PRDIR) $(TIME) $(PY) teval_aggr.py	

teval_merge: teval_aggr
	$(PRDIR) $(TIME) $(PY) teval_merge.py

teval_gen: teval
	$(PRDIR) $(TIME) $(PY) dataset_eval_gen.py

#
# students productivity recipes
#
stud: stud_aggr

stud_aggr: import 
	$(PRDIR) $(TIME) $(PY) stud_aggr.py

stud_gen: stud
	$(PRDIR) $(TIME) $(PY) dataset_stud_gen.py

#
# finalize
#
merged: stud teval
	$(PRDIR) $(TIME) $(PY) dataset_merge.py

cleaned: merged
	$(PRDIR) $(TIME) $(PY) dataset_clean.py

minified: cleaned
	$(PRDIR) $(TIME) $(PY) dataset_min.py

discretized: minified
	$(PRDIR) $(TIME) $(PY) dataset_discretize.py

#
# export
#
EXP= mongoexport
FIELDS_FULL= --type=csv --fieldFile=prepr/_exp_fields.txt
FIELDS_STUD= --type=csv --fieldFile=prepr/_exp_fields_stud_gen.txt
FIELDS_EVAL= --type=csv --fieldFile=prepr/_exp_fields_eval_gen.txt

export: exp_stud_gen exp_merged_full exp_merged_full_d

prep_exp: cleaned
	$(PRDIR) sh export.sh

exp_stud_gen: stud_gen prep_exp
	$(EXP) --db $(DB) --collection stud_gen $(FIELDS_STUD) > datasets/stud_gen.csv

exp_merged_full: cleaned prep_exp
	$(EXP) --db $(DB) --collection minable $(FIELDS_FULL) > datasets/full.csv

exp_merged_full_d: discretized prep_exp
	$(EXP) --db $(DB) --collection minable_discretized $(FIELDS_FULL) > datasets/full_d.csv
