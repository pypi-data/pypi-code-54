from collections import Counter,defaultdict,deque
try:
    from gurobipy import*
except:
    from mypulp import*

def unfold(c,x):
    l=[]
    d=defaultdict(deque)
    dlimit=defaultdict(int)

    for start,end,num in x:
        d[start].append([end,int(num)])
    
    while d[0]:
        tmp=[]
        i=0
        while len(d[i]):
            cargoweight=d[i][-1][0]-i
            dlimit[cargoweight]+=1
            if dlimit[cargoweight]<=c[cargoweight]:
                tmp.append(cargoweight)
            dequetmp=d[i].pop()
            if dequetmp[1]!=1:
                dequetmp[1]-=1
                d[i].append(dequetmp)
                i=dequetmp[0]            
            else:
                dequetmp[1]-=1
                i=dequetmp[0]
        l.append(sorted(tmp))
    return sorted(l,key=lambda x:sum(x),reverse=1)

def packing(cap,cargo):
    if max(cargo)>cap:
        raise ValueError("maximum value is more than cap")
    if min(cargo)<0:
        raise ValueError("minimum value is less than 0")
    if any(type(i)==float for i in cargo):
        raise ValueError("can't calculate 'float', please multiply cargo's numbers(e.g.10x)")

    num=len(cargo)
    m=Model("a")
    try:
        m.setParam('OutputFlag', 0)
    except:
        pass

    z=m.addVar(vtype="I",lb=0)
    A={}
    c=Counter(cargo)
    for i in range(cap+1):
        for j in c:
            if i+j<=cap:
                A[(i,i+j)]=m.addVar(vtype="I", lb=0)

    for i in range(cap):
        A[(i,i+1)]=m.addVar(vtype="I", lb=0, name="A"+str(i)+"-"+str(i+1))
    
    m.update()
    for k,v in c.items():
        m.addConstr( quicksum(x for (i,j),x in A.items() if j-i==k) >= v )
    
    zcost=[-z]+[0]*(cap-1)+[z]
    
    for j in range(cap+1):
        m.addConstr( quicksum( v for (ii,jj),v in A.items() if jj==j and ii<=j ) - 
                     quicksum( v for (jj,kk),v in A.items() if jj==j and j<=kk ) == zcost[j] )

    m.setObjective(z,GRB.MINIMIZE)
    m.optimize()
    if m.Status == GRB.Status.OPTIMAL:
        start_end_num=[(k[0],k[1],round(v.X)) for k,v in A.items()if round(v.X)>0]
        return unfold(c,start_end_num)