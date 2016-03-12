

def hgmdserve(hgmdid,db):
	try:
		rec = db[hgmdid]
	except:
		rec = "No recond"
	return rec


