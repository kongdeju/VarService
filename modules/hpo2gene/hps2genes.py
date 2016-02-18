import msgpack

hpofp = open("modules/hpo2gene/hp2gene.bson",'r')
genesfp = open("modules/hpo2gene/genenames.bson",'r')
hp2gene = msgpack.unpackb(hpofp.read())
Genes = msgpack.unpackb(genesfp.read())
Genes = set(Genes)

def hps2genes(hps):
	mod = hps[0]
	try:
		totalgenes = set(hp2gene[hps[1]])
	except:
		totalgenes = Genes

	for hp in hps[2:]:
		if mod == 'intersect':
			try:
				genes = set(hp2gene[hp])
				totalgenes = totalgenes & genes
			except:
				genes = Genes
				totalgenes = totalgenes & genes
		elif mod == 'join':
			try:
				genes = set(hp2gene[hp])
				totalgenes = totalgenes | genes
			except:
				genes = Genes
				totalgenes = totalgenes | genes
	return totalgenes
