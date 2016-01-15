import msgpack

fp = open("genemode.tsv","r")

genemodes = {}

for line in fp:
	items = line.strip("\n").split("\t")
	gene = items[0].strip()
	mod = items[1].strip()
	mtype = "UN"
	if mod == "Autosomal dominant":
		mtype = "AD"
	elif mod == "Autosomal recessive":
		mtype = "AR"
	genemodes[gene] = mtype

fp.close()
packed = msgpack.packb(genemodes)

fp = open('genemode.bson','wb')
fp.write(packed)
#print genemodes.items()
