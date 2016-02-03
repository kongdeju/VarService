
import sys
import msgpack


hpo = sys.argv[1]

fp = open(hpo,'r')

hp_dict = {}

for line in fp:
	items = line.strip("\n").split("\t")
	hpo_num = items[0].split(":")[-1]
	gene = items[-1]
	hpo_num,gene
	if hpo_num in hp_dict:
		hp_dict[hpo_num].append(gene)
	else:
		hp_dict[hpo_num] = [gene]

packed = msgpack.packb(hp_dict)


fpo = open("hp2gene.bson",'wb')
fpo.write(packed)
fpo.close()
