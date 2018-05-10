DB = exams
SCHEME= MongoClient().exams
PRDIR= cd prepr &&
TDIR= cd thesis &&
PY= python3
TEX= pdflatex -shell-escape -interaction=nonstopmode -file-line-error

# useful to spot bad coded modules
TIME= /usr/bin/time --format=%e

.DEFAULT= all
all: prepr pdf


################
# LATEX THESIS #
################
pdf:
	$(TDIR) $(TEX) thesis.tex

######################
# PREPROCESSING STEP #
######################

prep: exp_eval_gen exp_stud_gen exp_full exp_min exp_d

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

teval_gen: teval_aggr
	$(PRDIR) $(TIME) $(PY) dataset_eval_gen.py

#
# students productivity recipes
#
stud: stud_aggr

stud_aggr: import
	$(PRDIR) $(TIME) $(PY) stud_aggr.py

stud_gen: stud_aggr
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
FIELDS_MIN=  --type=csv --fieldFile=prepr/_exp_fields_min.txt
FIELDS_STUD= --type=csv --fieldFile=prepr/_exp_fields_stud_gen.txt
FIELDS_EVAL= --type=csv --fieldFile=prepr/_exp_fields_eval_gen.txt

# out of recipes tree, run it manually when needed
list_fields:
	$(PRDIR) sh list_fields.sh

prep_exp:
	yes | rm -rf datasets && mkdir datasets

exp_stud_gen: stud_gen prep_exp
	$(EXP) --db $(DB) --collection stud_gen $(FIELDS_STUD) > datasets/gen_stud.csv

exp_eval_gen: teval_gen prep_exp
	$(EXP) --db $(DB) --collection eval_gen $(FIELDS_EVAL) > datasets/gen_eval.csv

exp_full: cleaned prep_exp
	$(EXP) --db $(DB) --collection minable $(FIELDS_FULL) > datasets/full.csv

exp_min: minified prep_exp
	$(EXP) --db $(DB) --collection minable_min $(FIELDS_MIN) > datasets/min.csv

exp_d: discretized prep_exp
	$(EXP) --db $(DB) --collection minable_discretized $(FIELDS_FULL) > datasets/full_d.csv
	$(EXP) --db $(DB) --collection minable_min_discretized $(FIELDS_MIN) > datasets/min_d.csv
