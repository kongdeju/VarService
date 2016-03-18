import json
import sys
import re
import os
import msgpack
import glob
from multiprocessing import Process,Manager
from modules.modeofinhere  import secondfilt
from modules.hpo2gene.hps2genes import hps2genes
Path = 'data/'

gene_pat = re.compile('Gene in (\[.+?\])')
path_pat = re.compile('Path in (\[.+?\])')
mengdel_pat1 = re.compile('^Inheritary in (\[.+?\])')
mengdel_pat2 = re.compile('and Inheritary in (\[.+?\])')
sex_pat1 = re.compile('and Sex == (\w)')
sex_pat2 = re.compile('Sex == (\w) and')
pheo_pat = re.compile('Phenotype in (\[.+?\])')

def load_bson(filename):
    fp = open(filename,'rb')
    vas = msgpack.unpackb(fp.read())
    return vas

def path2genes(paths):
    fp = open("lib/path2genes.bson",'rb')
    p2g_dict = msgpack.unpackb(fp.read())
    Genes = []
    for path in paths:
        try:
            genes = p2g_dict[path]
            Genes.extend(genes)
        except:
            pass
    return Genes

def make_cmd(head_items,filt_str):
    sex = "U"
    if filt_str == "All":
        mengdel_filt = None
        filt_cmd = '1'
        return filt_cmd,mengdel_filt,sex

    mat1 = gene_pat.search(filt_str)
    mat2 = path_pat.search(filt_str)
    mat3_1 = mengdel_pat1.search(filt_str)
    mat3_2 = mengdel_pat2.search(filt_str)
    mat4 = sex_pat1.search(filt_str)
    mat4_1 = sex_pat2.search(filt_str)
    mat5 = pheo_pat.search(filt_str)

    if mat1:
        gene_list = eval(mat1.group(1))
        global Genes1
        Genes1 = set(gene_list)
        filt_str,n1 = gene_pat.subn("Gene in Genes1",filt_str)
    if mat2:
        path_list = eval(mat2.group(1))
        gene_list = path2genes(path_list)
        global Genes2
        Genes2 = set(gene_list)
        filt_str,n2 = path_pat.subn("Gene in Genes2",filt_str)
    if mat5:
        pheno_list = eval(mat5.group(1))
        gene_set = hps2genes(pheno_list)
        global Genes3
        Genes3 = gene_set
        filt_str = pheo_pat.sub("Gene in Genes3",filt_str)
    if mat3_1:
        mengdel_filt = mat3_1.group(1)
        filt_str = '1'
    else:
        if mat3_2:    
            mengdel_filt = mat3_2.group(1)
            filt_str = mengdel_pat2.sub('',filt_str)
        else:
            mengdel_filt = None

    if mat4:
        sex = mat4.group(1)
        filt_str = sex_pat1.sub('',filt_str)
    if mat4_1:
        sex = mat4_1.group(1)
        filt_str = sex_pat2.sub('',filt_str)

    print sex
    filt_items = filt_str.split()
    if not filt_items:
        filt_cmd = '1'
        mengdel_filt = None
        sex = "U"
        return filt_cmd,mengdel_filt,sex
    i = -1
    for item in filt_items:
        i = i + 1
        if item == "==" or item == "!=" :
            key_idx1 = head_items.index(filt_items[i-1])
            filt_items[i-1] = "item%d" % key_idx1
            if filt_items[i+1] == "null":
                filt_items[i+1] = "''"
            else:
                filt_items[i+1] = "'%s'" % filt_items[i+1]
        if item == "has":
            key_idx1 = head_items.index(filt_items[i-1])
            filt_items[i-1] = "'%s'" % filt_items[i+1]
            filt_items[i+1] = "item%d" % key_idx1
            filt_items[i] = "in"
        if item == "in":
            key_idx1 = head_items.index(filt_items[i-1])
            filt_items[i-1] = "item%d" % key_idx1
        if  ">" in item or "<" in item:
            key_idx1 = head_items.index(filt_items[i-1])
            filt_items[i-1] = "Float(item%d)" % key_idx1
            filt_items[i+1] = "%s" % filt_items[i+1]
    filt_cmd = " ".join(filt_items)
    return filt_cmd,mengdel_filt,sex
            
def Float(str):
    try:
        fnum = float(str)
    except:
        fnum =''
    return fnum

def filt_vars(vas,filt_str):
    head_items = vas[0]
    filt_cmd,mengdel,sex = make_cmd(head_items,filt_str)
    filtvars = []
    cmd = "for items in vas[1:]:\n "
    for i in range(len(head_items)):
        cmd = cmd  + "\titem%s = items[%s]\n" % (i,i)
    cmd = cmd + "\tif %s :\n" %  filt_cmd
    cmd = cmd + "\t\tfiltvars.append(items)\n"
    cmd = cmd + "filtvars.insert(0,head_items)"
    exec(cmd)
    return filtvars,mengdel,sex

def mengdel_vars(vars,filt_str,sex):
    if filt_str :
        vars = secondfilt.secondfilt(vars,filt_str,sex)
        return vars
    else:
        return vars

def FiltVars(sample_no,filt_str):
    filename = sample_no + '.bson'
    file_path = os.path.join(Path,filename)
    try: 
        vas = load_bson(file_path)
        try:
            filts,mengdel,sex = filt_vars(vas,filt_str)
            filts = mengdel_vars(filts,mengdel,sex)
            status = "Success"
            return status,filts
        except:
            
            status = "Internal Error,check your submit %s:%s" % (sys.exc_info()[0],sys.exc_info()[1])
            filts = "NA"
            return status,filts
    except:
        status =  "%s is not annotated" % sample_no
        filts = "NA"
        return status,filts

def HeadVars(sample_no):
    filename = sample_no + '-top.bson'
    file_path = os.path.join(Path,filename)
    try:
        vas = load_bson(file_path)
        status = "Success"
        return status,vas
    except:
        status =  "%s is not annotated" % sample_no
        vas = "NA"
        return status,vas

def LoadVars(sample_no):
    filename = sample_no + '.bson'
    file_path = os.path.join(Path,filename)
    try:
        vas = load_bson(file_path)
        status = "Success"
        return status,vas
    except:
        status =  "%s is not annotated" % sample_no
        vas = "NA"
        return status,vas

#if __name__ == "__main__":
#    LoadVars('WGC050803D')    
