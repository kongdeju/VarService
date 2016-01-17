

def hgmdserve(id,db):
	try:
		rec = db[id]
	except:
		rec = "No recond"
	return rec


