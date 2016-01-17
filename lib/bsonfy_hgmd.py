import sys
import msgpack

fp = open(sys.argv[1],'r')
fpo = open('hgmd.bson','wb')
hgmd = {}
for line in fp:
	items = line.strip("\n").split("\t")
	chr = items[0]
	start = items[1]
	ref = items[3]
	alt = items[4]
	recs = items[5]
	id = "%s_%s_%s->%s" % (chr,start,ref,alt)
	hgmd[id] = recs

packed = msgpack.packb(hgmd)
fpo.write(packed)


