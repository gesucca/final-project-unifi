DB = exams

all: export

reset_db:
	mongo $(DB) --eval "db.dropDatabase()"

import: reset_db
	cd prepr && sh import.sh

# here I can do fancy things...
prepr: import
	cd prepr && python3 main_prepr.py

export: prepr
	cd prepr && sh export.sh

