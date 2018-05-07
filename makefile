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

#
# students productivity recipes
#
stud: stud_aggr

stud_aggr: import 
	$(PRDIR) $(TIME) $(PY) stud_aggr.py

#
# general students performances
#
gen: stud
	$(PRDIR) $(TIME) $(PY) dataset_gencoorte.py

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

export: gen cleaned discretized
	$(PRDIR) sh export.sh

