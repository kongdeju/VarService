import msgpack
import sys
fp = open(sys.argv[1],"r")

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
	if gene in genemodes:
		if mtype in genemodes[gene]:
			continue
		else:
			genemodes[gene].append(mtype)
	else:
		genemodes[gene] = [mtype]
for k,v in genemodes.items():
	if "UN" in v and ( "AD" in v or "AR" in v ) :
		v.remove("UN")
		genemodes[k] = v
fp.close()
packed = msgpack.packb(genemodes)

fp = open('genemode.bson','wb')
fp.write(packed)
#print genemodes.items()
