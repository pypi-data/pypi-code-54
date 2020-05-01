import random
from fractions import Fraction
from math import *
from operator import add,sub, mul
from copy import copy,deepcopy
from adem.tools.exprs import *
from adem.errors.exceptions import *
from adem.fundamentals.primary import Num
from adem.misc.gen import intable, whole
try:
    from numpy import array,ndarray
except ImportError:
    pass


class Matrix:
    '''
        Calling this class create a Matrix Object.
        The class will initialize a Matrix for you by just calling Matrix()
        if you want to convert arrays to Matrix Object you use the X parameter
            You convert a list to Matrix Object; this will work fine if the
                first 2 elements gives the order of the matrix

                e.g To convert [1,2,3,4,5,6,7,8], this can be a 1x8, 2x4, 4x2 or 8x1
                    so you indicate the order by adding the order to the begining
                    if the order is 2 x 4
                    Mat_A = Matrix(X = [2,4,1,2,3,4,5,6,7,8]
                    
            You can convert 2D array (in form of list)
                e.g Mat_A = Matrix([[1,2],[3,4],[5,6],[7,8]])

            You can convert numpy arrays as well
                e.g if Y is an numpy.ndarray object, then Mat_A = Matrix(X = Y)

    '''
            
    def __init__(self, X = []):
        if isinstance(X,ndarray) or X != []:
            Mat = X
            if isinstance(X,ndarray):
                Mat = list(X.shape)
                for rows in X:
                    Mat += list(rows)
            elif X and isinstance(X[0],list):
                Mat = [len(X),len(X[0])]
                for rows in X:
                    if len(rows) != Mat[1]:
                        raise DimensionError('Dimension Inconsistent')
                    Mat += rows
        else:
            Mat = []
            try:
                order = input("Matrix Order: ")
                col = int(order.split('x')[1]); row = int(order.split('x')[0])
                Mat.append(row); Mat.append(col); count = 1
                while count <= row:
                    disp = "Enter the"
                    if count == 1:
                        pos = 'First'
                    elif count ==2:
                        pos = 'Second'
                    elif count == row:
                        pos = 'Last'; disp = 'Good, Now the'
                    else: pos = 'Next'; disp = ''
                    element = input(f"{disp} {pos} row: ").split()
                    while True:
                        if len(element) == col:
                            for elements in element:
                                Mat.append(eval(elements))
                            break
                        num = "element" if len(element) == 1 else 'elements'
                        print(f"Error, You Entered {len(element)} {num} instead of {col}")
                        element = input("Try Again: ").split()
                    count += 1
                            
            except Exception:
                print("Error")
        self.Mat = Mat
        self.state = 'enabled'
    def __str__(self,pr_sr = True):
        for integers in range(self.rows()):
            line = []
            # Checking if elements are whole number and convert to fractions if not
            for integer in range(self.cols()):
                if intable(self[integers + 1,integer + 1]):
                    line.append(int(self[integers + 1,integer + 1]))
                else: 
                    frac = Fraction(self[integers + 1,integer + 1]).limit_denominator()
                    line += [frac.numerator] if frac.denominator == 1 else [f'{frac.numerator}/{frac.denominator}']
            if pr_sr:
                print(line)
        return ''
    def null(self,order):
        Mat = order
        mat = [0 for i in range(order[1]*order[0])]
        return Matrix(Mat + mat)
    def identity(self,order):
        Mat = order
        if Mat[0] != Mat[1]:
            raise OrderError
        for integer in range(order[0]):
            for integers in range(order[1]):
                Mat.append(1) if integer == integers else Mat.append(0)
        return Matrix(Mat)
    def __getitem__(self,other):
        if self.isdisable():
            raise OperationNotAllow('This Matrix is Disabled for Modification')

        if isinstance(other,int): # To get elements element-wise
            return self.Mat[other+1]
        elif len(other) == 2:# To get element located i,j
            if other[1] > self.cols() or other[0] > self.rows():
                raise OutOfRange(f"This Matrix only has {self.rows()} rows and {self.cols()} columns")
            return self.get_row(other[0])[other[1]-1]
        
    def __delitem__(self,key):
        # check if Matrix is active or immutable
        if self.isdisable():
            raise OperationNotAllow('This Matrix is Disabled for Modification')
        if self.isimut():
            raise InvalidOperation('This Matrix is Immutable')
        # if key is an integer rows is deleted else if key is a string column is deleted
        if isinstance(key,int):
            if key > self.rows():
                raise OutOfRange(f"This Matrix only has {self.rows()} rows, Hence Can't get to row {key}")
            if key < 0:
                key = self.rows() + 1 + key
            for integer in range(self.cols()):
                del self.Mat[(key-1)*self.cols()+2]
            self.Mat[0] -= 1
        elif isinstance(key,str):
            if int(key) > self.cols():
                raise OutOfRange(f"This Matrix only has {self.cols()} columns, Hence Can't get to column {key}")
            if int(key) < 0:
                key = self.cols() + 1 + int(key)
            for integer in range(self.rows()):
                del self.Mat[integer*self.cols()+2+int(key)-(integer+1)]
            self.Mat[1] -= 1
        elif len(key) == 2:
            raise InvalidOperation("Can only delete rows or columns not single item")
    def __shield__(self):
        self.state = 'shield'
    def __ishield__(self):
        self.state = 'active'
    def __disable__(self):
        self.state = 'disabled'
    def __enable__(self):
        self.state = 'enabled'
    def pop(self,key=1):
        if self.isdisable():
            raise OperationNotAllow('This Matrix is Disabled for Modification')
        if self.isimut():
            raise InvalidOperation('This Matrix is Immutable')

        # if key is an integer rows is returned else if key is a string column is returned
        if isinstance(key, int):
            if key < 0:
                key = self.rows() + 1 + key
            get = self.get_row(key)
            del self[key]
        elif isinstance(key,str):
            if int(key[1]) < 0:
                key = self.cols() + 1 + int(key)
            get = self.get_col(int(key))
            del self[str(key)]
        return get
    def __setitem__(self,key,value):
        # check if Matrix is active or immutable
        if self.isdisable():
            raise OperationNotAllow('This Matrix is Disabled for Modification')
        if self.isimut():
            raise InvalidOperation('This Matrix is Immutable')
        # row for integer, col for string, i,j for list 
        if isinstance(key,int):
            if key < 0:
                key = self.rows() + 1 + key
            if not isinstance(value,list):
                self.Mat[key+1] = eval(f'{value}')
            elif isinstance(value,list):
                if key == self.rows()+1:
                    self.add_row([value])
                elif key > 0 and key <= self.rows():
                    self.add_row([value])
                    self.perform('~',rows=[-1, key])
                    del self[-1]
        elif isinstance(key,str):
            self.__setitem__(['*',int(key)],value)
        elif len(key) == 2:
            key = list(key)
            if key[0] == '*':
                if key[1] < 0:
                    key = ['*',self.cols() + 1 + key[1]]
                if key[1] == self.cols()+1:
                    self.add_col([value])
                elif key[1] > 0 and key[1] <= self.cols():
                    self.add_col([value])
                    self.perform('~',cols=[-1, key[1]])
                    del self['-1']
            elif key[0] > self.rows() or key[1] > self.cols():
                raise OutOfRange(f"Entry {key} doesn't exist. This Matrix only has {self.rows()} rows and {self.cols()} columns")
            else:
                if key[1] < 0:
                    key[1] += self.cols() + 1
                if key[0] < 0:
                    key[0] += self.rows() + 1
                self.Mat[(key[0]-1)*self.cols()+ key[1]+1] = eval(f'{value}')
    def __eq__(self,other):
        if self.isdisable():
            raise OperationNotAllow('This Matrix is Disabled for Modification')
        return self.Mat == other.Mat
    
    def __ne__(self,other):
        if self.isdisable():
            raise OperationNotAllow('This Matrix is Disabled for Modification')
        return self.Mat != other.Mat
    
    def __lt__(self,other):
        if self.isdisable():
            raise OperationNotAllow('This Matrix is Disabled for Modification')
        if isinstance(other,Matrix):
            other = other.rank()
        return self.rank() < other
    
    def __le__(self,other):
        if self.isdisable():
            raise OperationNotAllow('This Matrix is Disabled for Modification')
        if isinstance(other,Matrix):
            other = other.rank()
        return self.rank() <= other
    
    def __gt__(self,other):
        if self.isdisable():
            raise OperationNotAllow('This Matrix is Disabled for Modification')
        if isinstance(other,Matrix):
            other = other.rank()
        return self.rank() > other
    
    def __ge__(self,other):
        if self.isdisable():
            raise OperationNotAllow('This Matrix is Disabled for Modification')
        if isinstance(other,Matrix):
            other = other.rank()
        return self.rank() >= other
    
    def __rlt__(self,other):
        return self > other
    
    def __le__(self,other):
        if self.isdisable():
            raise OperationNotAllow('This Matrix is Disabled for Modification')
        return self >= other
    
    def __gt__(self,other):
        if self.isdisable():
            raise OperationNotAllow('This Matrix is Disabled for Modification')
        return self < other
    
    def __ge__(self,other):
        if self.isdisable():
            raise OperationNotAllow('This Matrix is Disabled for Modification')
        return self <= other
    
    def __bool__(self):
        if self != mat.null(self.order()):
            return True
        return False
    
    def rank(self):
        rank_ = 0
        for rows in self.echelon():
            rank_ += 1 if rows.count(0) - len(rows) else 0
        return rank_
    
    class mat_iter:
        def __init__(self,Mat):
            self.n = 1
            self.stop = Mat.rows()
            self.step = 1
            self.Mat = Mat
            
        def __next__(self):
            if (self.n > self.stop):
                raise StopIteration
            row = self.Mat.get_row(self.n)
            self.n += self.step
            return row
        
        def __iter__(self):
            return self
        
    def __iter__(self):
        return Matrix.mat_iter(self)
    
    def __copy__(self):
        mat_ = tuple(self.Mat)
        mat_ = list(mat_)
        mat_ += [1]
        del mat_[-1]
        return Matrix(mat_)
    
    def __abs__(self):
        if self.isdisable():
            raise OperationNotAllow('This Matrix is Disabled for Modification')
        if self.rows() != self.cols(): # For Square Matrix certainty
            raise InvalidOperation('Determinats are only supported by Square Matrices')
        mat_init = tuple(self.Mat)
        res = 0
        if self.order() == [2,2]:
            return self[1]*self[4] - self[3]*self[2]
        mult = self.pop()
        mat_ = tuple(self.Mat)
        for integers in range(self.cols()):
            self.Mat = list(mat_)
            del self[f'{integers+1}']
            res += (-1)**integers * mult[integers] * abs(self)
        self.Mat = list(mat_init)
        return (res)
    
    def get_row(self,row = 1):
        if self.isdisable():
            raise OperationNotAllow('This Matrix is Disabled for Modification')
        if row > self.rows():
            raise OutOfRange(f"This Matrix only have {self.rows()}")
        if row < 0: # To support negative keys
            row = self.rows() + 1 + row
        return [self.Mat[(row-1)*self.cols()+integer+2] for integer in range(self.cols())]

    def get_col(self, col = 1):
        if self.isdisable():
            raise OperationNotAllow('This Matrix is Disabled for Modification')
        if col < 0:
            col = self.cols() + 1 + col
        return [self.Mat[(col-1)+self.Mat[1]*intger+2] for intger in range(self.rows())]

    def get_diag(self, diag = ''):
        if self.isdisable():
            raise OperationNotAllow('This Matrix is Disabled for Modification')
        Diag = []
        if not self.issq():
            raise DimensionError('Can only get Diagonal of Square Matrix')
        if not diag:
            for rows in self:
                Diag.append(rows[len(Diag)])
        else:
            for rows in self:
                Diag.append(rows[self.rows()-(len(Diag)+1)])
        return Diag
    
    def add_row(self, row):
        if self.isdisable():
            raise OperationNotAllow('This Matrix is Disabled for Modification')
        if self.isimut():
            raise InvalidOperation('This Matrix is Immutable')

        for rows in row:
            if len(rows) == self.cols():
                self.Mat += rows
                self.Mat[0] += 1

    def add_col(self, col):
        if self.isdisable():
            raise OperationNotAllow('This Matrix is Disabled for Modification')
        if self.isimut():
            raise InvalidOperation('This Matrix is Immutable')

        addded_mat = self.Mat
        addded_mat= Matrix(addded_mat).trn()
        addded_mat.add_row(col)
        self.Mat = addded_mat.trn().Mat
        
    def perform(self, operation = '',rows = [],A = 1,B = 1, cols = []):
        if self.isdisable():
            raise OperationNotAllow('This Matrix is Disabled for Modification')
        if self.isimut():
            raise InvalidOperation('This Matrix is Immutable')

        # Row Operations
        if self.isimut():
            raise InvalidOperation('This Matrix is Immutable')
        if self.isdisable():
            raise OperationNotAllow('This Matrix is Disabled for Modification')
        # To translate to Column Operations
        if not rows:
            col_mat = Matrix(self.trn().Mat)
            col_mat.perform(operation = operation,rows = cols,A = A,B = B, cols = [])
            self.Mat = col_mat.trn().Mat
            return None
        # Row multiplication with scalar rows[0],Interchanging Rows, Addition, Subtraction
        if not operation:
            row = self.get_row(rows[1])
            for integer in range(self.cols()):
                self[rows[1],integer+1] = row[integer]*rows[0]
        elif operation == '~':
            row1 = self.get_row(rows[0])
            row2 = self.get_row(rows[1])
            for integer in range(self.cols()):
                self[rows[0],integer+1] = row2[integer]
                self[rows[1],integer+1] = row1[integer]
        elif operation == '+':
            row1 = self.get_row(rows[0])
            row2 = self.get_row(rows[1])
            for integer in range(self.cols()):
                self[rows[0],integer+1] = A*row1[integer] + B*row2[integer]
        elif operation == '-':
            row1 = self.get_row(rows[0])
            row2 = self.get_row(rows[1])
            for integer in range(self.cols()):
                self[rows[0],integer+1] = A*row1[integer] - B*row2[integer]
                
    def modal(self):
        if self.isdisable():
            raise OperationNotAllow('This Matrix is Disabled for Modification')
        # Modal Matrix
        self_ = copy(self)
        mod_mat = self.order()
        zeros = [0 for zeros in range(self.rows())]
        alpha = ['a','b','c','d',
                 'f','g','h','i','j',
                 'k','l','m','n','o',
                 'p','q','r','s','t',
                 'u','v','w','x','y',
                 'z']
        for evs in self.ev():
            mod = self - evs * mat.identity(self.order())
            if self.order() == [2,2]:
                mod_mat += whole([1,-mod[1]/mod[2]]) # Scaling the eign-vectors
            else:
                num = 0;sing = [];cols = []
                for count,rows in enumerate(mod):
                    if num == self.rows() -1:# To ensure the number of eqns is not more than the Order less than 1
                        break
                    if rows.count(0) == self.cols():# To skip null rows
                        continue
                    eqn = E('0')
                    for cout,element in enumerate(rows):
                        if not cout or not element:
                            if not cout:
                                sing.append(-element)
                            continue
                        eqn += f'{element}{alpha[cout]}'
                    if not count:
                        mod_eqn = Eqn(eqn)
                    else: mod_eqn.add(eqn)
                    num += 1
                    if not eqn.simp() and not cols:
                        cols = [0]
                if not cols:
                    cols = [1]
                if not cols[0]:
                    ext = ['##']
                    sing = [0 for zeros in sing]
                else:
                    ext = [] 
                for var, values in (mod_eqn & (sing + ext)).items():
                    cols.append(values)
                mod_mat += whole(cols) # Scaling the eign-vectors
        return Matrix(mod_mat).trn()
    
    def type(self):
        attr = []
        matt = tuple(self.Mat)
        self_ = copy(self)
        if not self_:
            attr.append('Null')
        try:
            if self_ == mat.identity(self.order()):
                attr.append('Unit')
        except Exception:
            pass
        try:
            test = self_*self_.trn()
            if test == mat.identity(test.order()):
                attr.append('Orthogonal')
        except Exception:
            pass
        
        self_ = copy(self)
        try:
            if self_** 2 == self_:
                attr.append('Idempotent')
        except Exception:
            pass
        
        try:
            if not abs(self_):
                attr.append('Singular')
        except Exception:
            pass
        
        self_ = copy(self)
        if self_.order()[0] == self_.order()[1]:
            attr.append('Square')
        else: attr.append('Augmented')
        
        if self_ == self_.trn():
            attr.append('Symmetric')
            
        if self_ == (-1) * self_.trn():
            diag = self.get_diag(); num = 0
            for nums in diag:
                if nums:
                    num += 1
            if num:
                attr.append('Skew Symmetric')
        try:
            if self_**2 == mat.identity(self_.order()):
                attr.append('Involuntary')
        except Exception:
            pass
        
        self_ = copy(self)
        try:
            for i in range(2,20):
                self_ *= self
                if not self_:
                    attr.append('Nilpotent');break
        except Exception:
            pass
        
        self_ = copy(self)
        try:
            self_ *= self
            for i in range(3,20):
                self_ *= self
                if self_ == self:
                    attr.append('Periodic');break
        except Exception:
            pass
        
        self.Mat = list(matt)
        return ', '.join(attr) + ' Matrix'
    
    def random(self,order):
        S = self.null(order)
        for row in range(S.rows()):
            for col in range(S.cols()):
                S[row+1,col+1] = random.randint(-1000,1000)
        return S
    
    def unify(self):
        mart = []
        for rows in self:
            mart += rows
        return mart
    
    def export(self):
        return array([rows for rows in self])
    
    def __string__(self):
        return self.__str__(False)
    
    def issing(self):
        return 'Singular' in self.type()
    def isnull(self):
        return 'Null' in self.type()
    def isunit(self):
        return 'Unit' in self.type()
    def isorth(self):
        return 'Orthogonal' in self.type()
    def issq(self):
        return 'Square' in self.type()
    def isidemp(self):
        return 'Idempotent' in self.type()
    def isnilp(self):
        return 'Nilpotent' in self.type()
    def isperiodic(self):
        return 'Periodic' in self.type()
    def isimut(self):
        return self.state == 'shield'
    def isdisable(self):
        return self.state == 'disabled'
    def isenable(self):
        return self.state == 'enabled'
    def __len__(self):
        return self.Mat[0]*self.Mat[1]
    
    def aug(self,aug_mat = ''):
        if self.isdisable():
            raise OperationNotAllow('This Matrix is Disabled for Modification')
        if self.isimut():
            raise InvalidOperation('This Matrix is Immutable')

        if not aug_mat:
            aug_mat = mat.identity(self.order())
        aug_mat = aug_mat.trn()
        _mat_ = self.trn()
        for rows in aug_mat:
            _mat_[_mat_.rows()+1] = rows
        self.Mat = _mat_.trn().Mat
        
    def cols(self):
        return self.order()[1]
    
    def rows(self):
        return self.order()[0]
    
    def __invert__(self):
        if self.isdisable():
            raise OperationNotAllow('This Matrix is Disabled for Modification')
        
        # Ensuring Matrix is Square and not singular
        if not self.issq():
            raise InvalidOperation('Inverse Property are only supported by Square')
        if self.issing():
            raise InvalidOperation('Singular Matrix has no Inverse')
        
        self.mat_ = self.Mat
        self.aug()
        emulated = mat.identity([self.rows(),self.rows()]);count = 0
        
        for integer in range(emulated.cols()): #row
            col = self.get_col(integer+1)
            for integers in range(emulated.rows()): #col
                count_ = 0
                if self[integers+1,integer+1] != emulated[integers+1,integer+1]:# To check if the elements corresponds as in Unit Matrix
                    if emulated[integers+1,integer+1] == 1: # To try convert the element to 1
                        try:
                            self.perform(rows = [1/self[integers+1, integer+1],integers+1])
                        except ZeroDivisionError:
                            # Switching elements to a non-zero elements after Multiply the row by the inverse
                            while True:
                                if count_ > count:
                                    if col[count_] != 0:
                                        self.perform('~',[integers+1,count_+1])
                                        self.perform([1/self[integers+1, integer+1]],integers+1)
                                        break
                                count_ += 1
                    else:
                        # Try setting the element to 0
                        while True:
                            try:
                                if integers > integer:
                                    self.perform(rows = [(self[integers+1, integer+1]/self[integer+1,integer+1])**(-1),integers+1])
                                    self.perform('-',[integers+1,integer+1])
                                elif integers < integer:
                                    self.perform(rows = [(self[integers+1, integer+1]/self[integer+1,integer+1]),integer+1])
                                    self.perform('-',[integers+1,integer+1])
                                break
                            except ZeroDivisionError:
                                while True:
                                    if count_ > count:
                                        if col[count_] != 0:
                                            self.perform('~',[integer+1,count_+1])
                                            break
                                    count_ += 1
            count += 1
        for integers in range(self.rows()):
            del self['1']
        self.mat = self.Mat
        self.Mat = self.mat_
        return Matrix(self.mat)
    
    def order(self):
        return [self.Mat[0],self.Mat[1]]
    
    def spectral(self):
        if self.isdisable():
            raise OperationNotAllow('This Matrix is Disabled for Modification')
        
        ev = self.ev()
        if not self.issq():
            raise InvalidOperation('Only Square  Matrices can have Spectral Matrix')
        spec = mat.identity([self.rows(),self.cols()])
        for count,evs in enumerate(ev):
            spec[count + 1,count+1] = evs
        return spec
    
    def echelon(self):
        if self.isdisable():
            raise OperationNotAllow('This Matrix is Disabled for Modification')
        ech = copy(self.Mat)
        if self[1,1] != 1:
            col = self.get_col(1)
            if 1 in col:
                self.perform('~', rows = [1,col.index(1)+1])
            elif self[1,1] == 0:
                col.reverse()
                index = 0
                for item in col:
                    if item != 0:
                        break
                    index += 1
                self.perform('~', rows = [1,len(col)-index])
        for integers in range(self.cols()):
            for integer in range(self.rows()):
                col = self.get_col(integers+1)
                if integer > integers and self[integer+1,integers+1] != 0:
                    try:
                        lcm = Num([self[integers+1, integers+1],self[integer+1,integers+1]]).LCM()
                    except Exception:
                        try:
                            lcm = Num([int(self[integers+1, integers+1]),int(self[integer+1,integers+1])]).LCM()
                        except Exception: lcm = self[integers+1, integers+1]*self[integer+1,integers+1]
                    self.perform(rows = [lcm/self[integer+1,integers+1], integer+1])
                    self.perform(rows = [lcm/self[integers+1,integers+1], integers+1])
                    self.perform('-',[integer +1,integers+1])
                elif integer == integers and self[integer+1,integers+1] == 0:
                    index = 0
                    for item in col:
                        if index > integer and item != 0:
                            self.perform('~', rows = [integer+1,index +1])
                            break
                        index += 1
        for integers in range(self.rows()):
            for items in self.get_row(integers+1):
                if items != 0:
                    self.perform(rows = [1/items, integers+1]);break
        maat = copy(self.Mat)
        self.Mat = ech
        return Matrix(maat)
    
    def rechelon(self):
        ech = self.echelon()
        for integers in range(ech.rows()):
            for items in ech.get_row(max(range(ech.rows()))-integers+1):
                if items != 0:
                    index_ = ech.get_row(max(range(ech.rows()))-integers+1).index(items)
                    for number in range(max(range(self.rows()))-integers):
                        ech.perform('+', rows = [number +1,max(range(ech.rows()))-integers+1], B = (-1) * ech[number+1,index_+1])
                    break
        return ech
    
    def trn(self):
        if self.isdisable():
            raise OperationNotAllow('This Matrix is Disabled for Modification')

        rows = [self.cols(), self.rows()]
        for integer in range(self.cols()):
            rows += self.get_col(integer+1)
        return Matrix(rows)
    
    def minor(self,row = 1, col = 1):
        if self.isdisable():
            raise OperationNotAllow('This Matrix is Disabled for Modification')
        
        minor_ = copy(self)
        del minor_[row]
        del minor_[f'{col}']
        return minor_
    
    def cofactor(self,row = 1, col = 1):
        if self.order() == [2,2]:
            raise InvalidOperation("2x2 Matrices don't have cofactors")
        return abs(self.minor(row,col))*(-1)**(row+col)
    
    def ev(self):
        if self.isdisable():
            raise OperationNotAllow('This Matrix is Disabled for Modification')
        eigen_values = []
        if not self.issq():
            raise InvalidOperation('Determinats are only supported by Square Matrices')
        mat_init = tuple(self.Mat)
        res = E('0'); sett = 5
        try:
            self.__string__() # To check if the Matrix has its principal diagonal dopped
            for integers in range(self.rows()):
                self[integers+1,integers+1] = '' + '"' +f'{self[integers+1,integers+1]} - x' + '"' 
        except ValueError:
            sett = 0
        if self.order() == [2,2]:
            # check if called directly or indirectly
            if sett:
                roots = (E(f'{self[1]}')*self[4] - E(f'{self[3]}')*self[2]).simp() & 'x'
                self.Mat = list(mat_init)
                while True:
                    try:
                        eigen_values.append(next(roots))
                    except StopIteration:
                        break
                return eigen_values
            else:
                self.Mat = list(mat_init)
                return (E(f'{self[1]}')*self[4] - E(f'{self[3]}')*self[2]).simp()
        mult = self.pop()
        mat_ = tuple(self.Mat)
        for integers in range(self.cols()):
            self.Mat = list(mat_)
            del self[f'{integers+1}']
            res += (E(f'{mult[integers]}') * self.ev()*(-1)**integers).simp()
        self.Mat = list(mat_init)
        # check if called directly or indirectly
        if not sett:
            return res.simp()
        
        roots = res.simp() & 'x'
        while True:
            try:
                eigen_values.append(next(roots))
            except StopIteration:
                break
        return eigen_values
    
    def new(self,new_mat):
        self.Mat = new_mat
        return self
    
    def cofactors(self):
        cofactor = [self.rows(),self.cols()]
        for integer in range(self.rows()):
            for integers in range(self.cols()):
                cofactor.append(self.cofactor(integer+1,integers+1))
        return Matrix(cofactor)
    
    def property(self):
        print(self)
        try:
            print(self.type())
            try:
                print(f'Determinat is {abs(self)}')
            except InvalidOperation:
                print('Determinant Not Supported')
            print(f'Rank is {self.rank()}')
            try:
                if self.isnilp():
                    self_ = copy(self)
                    for i in range(2,20):
                        self_ *= self
                        if not self_:
                            print(f'This Matrix is Nilpotent to the index of {i+1}')
                            break;
            except Exception:
                pass
            try:
                if self.isperiodic():
                    self_ = copy(self)
                    self_ *= self_
                    for i in range(3,20):
                        self_ *= self
                        if not self_ == self:
                            print(f'This Matrix has a period of {i-1}')
                            break
            except Exception:
                pass
            self_ = copy(self)
            try:
                for i in range(2,20):
                    self_ *= self_
                    if self_ == ~self_:
                        print(f'This Matrix raised to the power of {i} gives its inverse\n Hence This Matrix raised to the power of {i+1} gives a Unit Matrix')
                        break;
            except Exception:
                pass
            print('------Transpose-------')
            print(self.trn())
            print('------Cofactors-------')
            try:
                print(self.cofactors())
            except InvalidOperation:
                print('Not Supported')
            print('------Spectral-------')
            print(self.spectral())
            print('------Modal-------')
            print(self.modal())
            print('------Inverse-------')
            try:
                print(~self)
            except InvalidOperation:
                print('Singular Matrix has no Inverse')
            print('------Echelon Form-------')
            print(self.echelon())
            print('------Reduced Echelon Form-------')
            print(self.rechelon())
        except OperationNotAllow:
            print('This Matrix is Disabled')
        
    def adj(self):
        return self.cofactors().trn()
    
    def __add__(self,other):
        if self.isdisable() or other.isdisable():
            raise OperationNotAllow('This Matrix is Disabled for Modification')

        if self.order() != other.order():
            raise DimensionError(f'Incompatible Matrices: {" x ".join(self.order())} and {" x ".join(other.order())}')
        new = self.order()
        for integer in range(self.rows()):
            new += list(map(add, self.get_row(integer+1), other.get_row(integer+1)))
        return Matrix(new)
    
    def __sub__(self,other):
        if self.isdisable() or other.isdisable():
            raise OperationNotAllow('This Matrix is Disabled for Modification')

        if self.order() != other.order():
            raise DimensionError(f'Incompatible Matrices: {" x ".join(self.order())} and {" x ".join(other.order())}')
        new = self.order()
        for integer in range(self.rows()):
            new += list(map(sub, self.get_row(integer+1), other.get_row(integer+1)))
        return Matrix(new)
    
    def __mul__(self,other):
        if self.isdisable():
            raise OperationNotAllow('This Matrix is Disabled for Modification')

        new = self.order()
        if isinstance(other, int) or isinstance(other, float):
            for integer in range(self.rows()):
                new += [other*item for item in self.get_row(integer+1)]
        else:
            if self.isdisable():
                raise OperationNotAllow('This Matrix is Disabled for Modification')

            if not self.cols() == other.rows():
                raise DimensionError(f'Incompatible Matrices: {" x ".join(self.order())} and {" x ".join(other.self.order())}')
            for integer in range(self.rows()):
                for integers in range(self.rows()):
                    new.append(sum(list(map(mul, self.get_row(integer+1), other.get_col(integers+1)))))
        return Matrix(new)
    
    def __rmul__(self,other):
        return self.__mul__(other)
    
    def __pow__(self,other):
        obj = copy(self)
        if isinstance(other, int):
            for integer in range(abs(other)-1):
                obj *= self
            if other < 0:
                return ~obj
        return obj
    
    def __truediv__(self,other):
        if isinstance(other, int) or isinstance(other, float):
            return self * (1/other)
        return self * ~other
    
    def __rtruediv__(self,other):
        return other * ~A
    
    def __truth__(self):
        get = ''
        for integer in range(self.rows()):
            for integers in range(self.cols()):
                if self[integer+1,integers+1]:
                    return True
        return False
    def __round__(self,other):
        self_ = copy(self)
        for ints in range(other):
            self_[ints + 1] = round(self[ints + 1],other)
        return self_
mat = Matrix("1 ")
