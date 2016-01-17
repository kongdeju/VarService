import msgpack
import sys
import os
####load ModelianGenes as a Global Variables

script_path = sys.path[0]
genemode = os.path.join(script_path,'modules/modeofinhere/genemode.bson')

fp = open(genemode,'r')
MendelianGenes = msgpack.unpackb(fp.read())

def GeneMode(gene):
	mode = "UN"
	try:
		mode = MendelianGenes[gene]
	except:
		pass
	return mode
