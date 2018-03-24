from pprint import pprint

def aggregate(teach_eval, productivity, dest):
	for doc in productivity.find():
		pprint(doc)
