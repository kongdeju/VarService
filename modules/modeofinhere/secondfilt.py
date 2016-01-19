from mendian import GeneMode
from collections import defaultdict



def dictify(variants):
	head = variants[0]
	gene_idx = head.index("Gene")
	gt_idx = head.index("GenoType")
	chr_idx = head.index("Chr")
	gene_gts = defaultdict(list)
	gene_chrs = defaultdict(list)
	gene_mods = defaultdict(list)
	for var in variants[1:]:
		gene = var[gene_idx]
		gt = var[gt_idx]
		chr = var[chr_idx]
		mod = GeneMode(gene)
		gene_gts[gene].append(gt)
		gene_chrs[gene].append(chr)
		gene_mods[gene].append(mod)
	return gene_gts,gene_chrs,gene_mods	

def labelgene(gene_gts,gene_chrs,gene_mods,sex):
	genelable = {}
	for gene in gene_gts.keys():
		nhet = 0
		nhom = 0
		mchr = ''
		for gt in gene_gts[gene]:
			if gt == "0|0" or gt == "0/0" or gt == "1/1" or gt == "1|1":
				nhom = nhom + 1
			else:
				nhet = nhet + 1
		nvar = len(gene_gts[gene])
		mod = gene_mods[gene][0]
		chr = gene_chrs[gene][0]
		degree = ''

		if chr != 'X' and chr != 'Y':
			mchr = "Norm"
		else:
			mchr = chr
		
		if (mod == "AD" or mod == "UN") and ( mchr == "Norm" or ( mchr == "X" and sex == "W" )):

			if nhet == 1 and nhom == 0:
				degree = "Highly"
				if mod == "UN":
					mod = "PAD"
			if nhet  + nhom == 2:
				degree = "Maybe"
				if mod == "UN":
					mod = "PAD"
			if nhet + nhom >2:
				degree = "Cannot"
				if mod == "UN":
					mod = "PAD"	
		
		if (mod == "AR" or mod == "UN") and ( mchr == "Norm" or ( mchr == "X" and sex == "W")):
			if ( nhet == 2 and nhom == 0 ) or ( nhet == 0 and nhom == 1 ) :
				degree = "Highly"
				if mod == "UN":
					mod = "PAR"
			if nhet + nhom >2:		
				if mod == "UN":
					mod = "PAR"
				degree = "Maybe"
			if nhet == 1 and nhom == 0:
				if mod == "UN":
					mod = "PAR"
				degree = "Cannot"

		if (mod == "AD" or mod == "AR" or mod == "UN" or mod == "UN") and mchr == "X" and sex == "M":
			if nhet + nhom == 1:
				degree = "Highly"
			if nhet + nhom >=2:
				degree = "Maybe"

		lable = mchr + "_" + mod + "_" + degree	
		genelable[gene] = lable
	return genelable



def secondfilt(variants,filtstr,sex="U"):

	gene_gts,gene_chrs,gene_mods = dictify(variants)	
	genelable = labelgene(gene_gts,gene_chrs,gene_mods,sex)

	filtset = set(eval(filtstr))
	head = variants[0]
	gene_idx = head.index("Gene")
	filtvars = []
	for var in variants[1:]:
		gene = var[gene_idx]
		lable = genelable[gene]
		if lable in filtset:
			filtvars.append(var)
	return filtvars


