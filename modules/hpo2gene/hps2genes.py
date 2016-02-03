import msgpack

hpofp = open("modules/hpo2gene/hp2gene.bson",'r')
hp2gene = msgpack.unpackb(hpofp.read())

def hps2genes(hps):
	totalgenes = []
	for hp in hps:
		try:
			genes = hp2gene[hp]
			totalgenes.extend(genes)
		except:
			pass
	totalgenes = set(totalgenes)
	return totalgenes
