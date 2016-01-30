from mendian import GeneMode

def add_genemode(vas):
	if vas == "NA":
		return vas
	if len(vas) == 1:
		return vas
	head = vas[0]	
	try:
		gene_idx = head.index("Gene")
	except:
		return "NA"
	newvas = [head]
	for items in vas[1:]:
		newlist = []
		prelist = items[:gene_idx]
		poslist = items[gene_idx+1:]
		gene = items[gene_idx]
		if gene != '':
			genemode = GeneMode(gene)
			genestr = gene + ":" + genemode
		else:
			genestr = ''
		newlist.extend(prelist)
		newlist.append(genestr)
		newlist.extend(poslist)
		newvas.append(newlist)
	return newvas
