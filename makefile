DB = exams
SCHEME= MongoClient().exams
PRDIR= cd prepr &&

all: export

reset_db:
	mongo $(DB) --eval "db.dropDatabase()"

import: reset_db
	$(PRDIR) sh import.sh

#
# teaching evaluation recipes
#
teval_clean: import
	$(PRDIR) python3 teval_clean.py

teval_aggr: teval_clean
	$(PRDIR) python3 teval_aggr.py	


export: prepr
	$(PRDIR) sh export.sh

