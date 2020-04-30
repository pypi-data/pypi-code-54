from collections import Counter,defaultdict,deque
try:
    from gurobipy import*
except:
    from mypulp import*

def packingCG(cap,cargo):
    if max(cargo)>cap:
        raise ValueError("maximum value is more than cap")
    if min(cargo)<0:
        raise ValueError("minimum value is less than 0")

    num=len(cargo)
    m=Model("a")
    try:
        m.setParam('OutputFlag', 0)
    except:
        pass

    cargo.sort()
    dp=defaultdict(list)
    dp[0]=[set()]

    for i,j in enumerate(cargo):
        for k,v in dp.copy().items():
            if k+j<=cap:
                for r in dp[k]:
                    if i not in r:
                        dp[k+j].append(r|{i})

    ret=tuple(itertools.chain.from_iterable(dp.values()))

    cmbidx={}
    for i in range(len(ret)):
        cmbidx[i]=m.addVar(vtype="B")
    
    m.update()
    for i in range(num):
        m.addConstr( quicksum(cmbidx[j] for j,v in enumerate(ret)if i in v) == 1 )
    
    m.setObjective( quicksum(cmbidx.values()) ,GRB.MINIMIZE)
    m.optimize()
    
    if m.Status == GRB.Status.OPTIMAL:
        return sorted([[cargo[idx]for idx in ret[k]]for k,v in cmbidx.items()if round(v.X)>0],key=lambda x:sum(x),reverse=1)

