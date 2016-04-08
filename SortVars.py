def Int(x):
    try:
        i = int(x)
    except:
        i = -1
    return i

def SortVars(vs):
    head = vs[0]
    vss = vs[1:] 
    sv = sorted(vss,key=lambda x:(Int(x[0]),Int(x[1])))   
    sv.insert(0,head)
    return sv



