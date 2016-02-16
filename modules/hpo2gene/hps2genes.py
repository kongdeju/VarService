import msgpack

hpofp = open("modules/hpo2gene/hp2gene.bson",'r')
hp2gene = msgpack.unpackb(hpofp.read())

def hps2genes(hps):
	mod = hps[0]
	totalgenes = set(hp2gene[hps[1]])
	for hp in hps[2:]:
		if mod == 'intersect':
			try:
				genes = set(hp2gene[hp])
				totalgenes = totalgenes & genes
			except:
				pass
		elif mod == 'join':
			try:
				genes = set(hp2gene[hp])
				totalgenes = totalgenes | genes
			except:
				pass
	return totalgenes
