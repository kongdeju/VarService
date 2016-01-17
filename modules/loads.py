import msgpack

hgmd = 'lib/hgmd.bson'
fp = open(hgmd,'r')

hgmd_dict = msgpack.unpackb(fp.read())
