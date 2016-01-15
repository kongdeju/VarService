import msgpack

####load ModelianGenes as a Global Variables
fp = open('genemode.bson','r')
MendelianGenes = msgpack.unpackb(fp.read())

def GeneMode(gene):
	mode = "UN"
	try:
		mode = MendelianGenes[gene]
	except:
		pass
	return mode
