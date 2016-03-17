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

##Norm_AD_
def norm_ad(mod,mchr,nhet,nhom):
    if "AD" in mod:
        modstr = "AD"
    elif "UN" in mod or "AU" in mod  or  "AO" in mod :
        modstr = "PAD"
    else:
        return None
    if mchr == "X" or mchr == "Y":
        return None
    if nhet == 1 and nhom == 0:
        degree = "Highly"
    if nhet + nhom >= 2:
        degree = "Maybe"
    if nhet == 0 and nhom == 1:
        degree = "Cannot"
    if degree:
        lable = mchr + '_' + modstr + "_" + degree
        return lable
def norm_ar(mod,mchr,nhet,nhom):
    if "AR" in mod:
        modstr = "AR"
    elif "UN" in mod or "AU" in mod  or "AO" in mod:
        modstr = "PAR"
    else:
        return None
    if mchr == "X" or mchr == "Y":
        return None
    if ( nhet == 2 and nhom == 0 ) or ( nhom == 1 and nhet == 0 ):
        degree = "Highly"
    if nhet + nhom > 2:
        degree = "Maybe"
    if nhet == 1 and nhom == 0:
        degree = "Cannot"
    if degree:
        lable = mchr + '_' + modstr + "_" + degree
        return lable
def x_ad(mod,mchr,nhet,nhom,sex):
    if "XR" in mod:
        modstr = "AR"
    elif "UN" in mod or "XU" in mod  or "XO" in mod or "XL" in mod :
        modstr = "PAR"
    else:
        return None
    if mchr == "Norm":
        return None
    if set == "U":
        return None
    degree = None
    if sex == "W":
        if nhet == 1 and nhom == 0:
            degree = "Highly"
        if nhet + nhom >= 2 :
            degree = "Maybe"
        if nhet == 0 and nhom == 1:
            degree = "Cannot"
        if degree:
            lable = mchr + '_' + modstr + '_' + degree
            return lable
    if sex == "M":
        if nhet == 0 and nhom == 1:
            degree = "Highly"
        if nhet ==0 and nhom > 1:
            degree = "Maybe"
        if nhet >=1:
            degree = "Cannot"
        if degree:
            lable = mchr + '_' + modstr + '_' + degree
            return lable

def x_ar(mod,mchr,nhet,nhom,sex):
    if "XR" in mod:
        modstr = "AR"
    elif "UN" in mod or "XU" in mod or "XO" in mod or "XL" in mod:
        modstr = "PAR"
    else:
        return None
    if mchr == "Norm":
        return None
    if set == "U":
        return None
    degree = None
    if sex == "W":
        if (nhet == 2 and nhom == 0) or (nhom == 1 and nhet == 0):
            degree = "Highly"
        if nhet + nhom > 2 :
            degree = "Maybe"
        if nhet == 1 and nhom == 0:
            degree = "Cannot"
        if degree:
            lable = mchr + '_' + modstr + '_' + degree
            return lable
    if sex == "M":
        if  nhom == 1:
            degree = "Highly"
        if  nhom > 1:
            degree = "Maybe"
        if nhom == 0:
            degree = "Cannot"
        if degree:
            lable = mchr + '_' + modstr + '_' + degree
            return lable
    
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
        print mod,mchr,nhet,nhom,sex
        normad_lb = norm_ad(mod,mchr,nhet,nhom)
        normar_lb = norm_ad(mod,mchr,nhet,nhom)
        xad_lb = x_ad(mod,mchr,nhet,nhom,sex)
        xar_lb = x_ar(mod,mchr,nhet,nhom,sex)
        lables = [normad_lb,normar_lb,xad_lb,xar_lb]
        #print lables
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


