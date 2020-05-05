
def MatTranspose(m):
    return [list(i) for i in zip(*m)]

def getMatrixMinor(m,i,j):
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

def MatDet(m):
    #base case for 2x2 matrix
    if len(m) == 2:
        return m[0][0]*m[1][1]-m[0][1]*m[1][0]

    determinant = 0
    for c in range(len(m)):
        determinant += ((-1)**c)*m[0][c]*MatDet(getMatrixMinor(m,0,c))
    return determinant

def MatInverse(m):
    determinant = MatDet(m)
    #special case for 2x2 matrix:
    if len(m) == 2:
        return [[m[1][1]/determinant, -1*m[0][1]/determinant],
                [-1*m[1][0]/determinant, m[0][0]/determinant]]

    #find matrix of cofactors
    cofactors = []
    for r in range(len(m)):
        cofactorRow = []
        for c in range(len(m)):
            minor = getMatrixMinor(m,r,c)
          
            cofactorRow.append(((-1)**(r+c)) * MatDet(minor))
            
        cofactors.append(cofactorRow)
    
    cofactors = MatTranspose(cofactors)
    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = cofactors[r][c]/determinant
    return cofactors
def MatProduct(a,b):
  result=[]
  result1=[]

  while len(a)>0:     
    
    d=0    
    a1=a[:1:]    
    #print(a1)
    c=True

    while d<len(a1):
      for x in b:
        for x1 in x:
          #print("x1 is", x1)
              #print("y1 is",y1)
          result.append(x1*a1[0][d])
        d=d+1
    
    a.pop(0)    
    
  result=[result[i:i+len(b[0])] for i in range(0, len(result), len(b[0]))]     
      
  #print(result)      
  sum=0      
  #mi basta fare append per avere tutto in una lista e sommare tutto con ultima funzione che ho fatto  
  while len(result)>0:
  
    for X in range(len(result[0])):
      for Y in range(len(b)):
        sum=sum+result[Y][X]
      result1.append(sum)
      
      #print(result1)
      sum=0 
    for s in range(len(b)):
      result.pop(0)  
    
  result1=[result1[i:i+len(b[0])] for i in range(0, len(result1), len(b[0]))] 
  return (result1)
     

