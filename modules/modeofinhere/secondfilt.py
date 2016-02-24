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
		lables =[]
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
		
		if ( "D" in mod or "U" in mod or "O" in mod or "L" in mod) and ( mchr == "Norm" or ( mchr == "X" and sex == "W" )):
			modstr = "AD"
			if nhet == 1 and nhom == 0:
				degree = "Highly"
				if "D" not in mod :
					modstr = "PAD"
			if nhet  + nhom >= 2:
				degree = "Maybe"
				if "D" not in mod :
					modstr = "PAD"
			if nhet == 0 and  nhom == 1:
				degree = "Maybe"
				if "D" not in mod:
					modstr = "PAD"	
			lable = mchr + '_' + modstr + "_" + degree
			lables.append(lable)

		if ("R" in mod or "U" in mod or "O" in mod or "L" in mod ) and ( mchr == "Norm" or ( mchr == "X" and sex == "W")):
			modstr = "AR"
			if ( nhet == 2 and nhom == 0 ) or ( nhet == 0 and nhom == 1 ) :
				degree = "Highly"
				if "R" not in mod :
					modstr = "PAR"
			if nhet + nhom >2:		
				if "R" not in mod :
					modstr = "PAR"
				degree = "Maybe"
			if nhet == 1 and nhom == 0:
				if "R" not in mod:
					mod = "PAR"
				degree = "Cannot"
			lable = mchr + "_" + modstr + "_" + degree
			lables.append(lable)
#		if  mchr == "X" and sex == "M":
#			if nhet + nhom == 1:
#				degree = "Highly"
#			if nhet + nhom >=2:
#				degree = "Maybe"
#			for item in mod:
#				modstr = item
#				lable = mchr + "_" + modstr + "_" + degree	
#				lables.append(lable)
		genelable[gene] = lables
	return genelable



def secondfilt(variants,filtstr,sex="U"):

	gene_gts,gene_chrs,gene_mods = dictify(variants)	
	genelable = labelgene(gene_gts,gene_chrs,gene_mods,sex)

	filtset = set(eval(filtstr))
	head = variants[0]
	gene_idx = head.index("Gene")
	filtvars = []
	filtvars.append(head)
	for var in variants[1:]:
		gene = var[gene_idx]
		lable = set(genelable[gene])
		if lable & filtset:
			filtvars.append(var)
	return filtvars


