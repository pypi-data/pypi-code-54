
from fractions import Fraction
from math import *
from copy import copy,deepcopy
from adem.fundamentals.primary import Num
from adem.misc.gen import intable, con
import adem.arrays.matrix as arm
from adem.errors.exceptions import *
try:
    from numpy import int32
except ImportError:
    pass

__all__ = ['E','Eqn']


class E:
    def __init__(self,expr,set_ = False):
        
        if not set_ and (not expr or len(expr) == expr.count(' ')):
            expr = '0'
        if set_:
            self.expr = expr
            return None
        step = 0
        var,coeff,pow_ = '','',''
        _var = {}
        _pow = []
        self.expr = {}
        expr = expr.replace('^-','#')
        expr = expr.replace('e-','%')
        expr = expr.replace('e','&')
        spec_char = {'&':'','%':'','!':''}
        if '/' in expr:
            part = expr.split('/')
            expr = E(part[0])
            for num, alg in enumerate(part):
                if not num:
                    continue
                expr /= alg
            self.expr = expr.expr
            return
        if '+' in expr:
            part = expr.split('+')
            tie = 0
            if not part[0] or part[0] == ' ':
                expr = E(part[1])
                tie = 1
            else:
                expr = E(part[0])
            for num, alg in enumerate(part):
                if num-1 < tie:
                    continue
                expr += alg
            self.expr = expr.expr
            return
        if '-' in expr:
            part = expr.split('-');tie = 0
            if not part[0] or part[0] == ' ':
                expr = E(f';{part[1]}')
                tie = 1
            else:
                expr = E(part[0])
            for num, alg in enumerate(part):
                if num-1 < tie:
                    continue
                expr -= alg
            self.expr = expr.expr
            return None
        expr = expr.replace(';','-').replace('#','^-')
        while True:
            if expr[step] == ' ':
                step += 1
                continue
            while step < len(expr) and (expr[step].isdigit() or expr[step] in ('+','-','.') or expr[step] == ' ' or expr[step] in spec_char):
                if not coeff and expr[step] == '+':
                    step += 1
                    continue
                if expr[step] == ' ':
                    step += 1
                    continue
                coeff += expr[step]
                step += 1
                
            while step < len(expr) and (expr[step].isalpha() or expr[step] in ('+','-') or expr[step] == ' '):
                if expr[step] == ' ':
                    step += 1
                    continue
                var = expr[step]
                step += 1
                try:
                    if step < len(expr) and expr[step] == '^':
                        step += 1; pow_ = ''
                        while step < len(expr) and (expr[step].isdigit()  or expr[step] in ('+','-','.')):
                            pow_ += expr[step]
                            step += 1
                    else: pow_ = 1
                except Exception:
                    pass
                if pow_ != '0':
                    _var[var] = eval(str(pow_))
                else: var = ''
            if not var:
                _var[''] = 0
            if not coeff:
                coeff = 1
            elif coeff == '-':
                coeff = '-1'
            coeff = f'{coeff}'.replace("%","e-").replace("&","e")
            coeff = factorial(int(coeff.replace('!',''))) if coeff[-1] == '!' else eval(coeff)
            if coeff not in self.expr:
                self.expr[coeff] = []
            self.expr[coeff].append(_var)
            if step >= len(expr):
                break

    def __str__(self):
        disp = '';
        for coeff in self.expr:
            if not coeff:
                continue
            if coeff < 0:
                disp += f' - {abs(coeff)}' if coeff != -1 else ' - 1' if self.expr[coeff] == [{'':0}] else ' - '
            else:
                if disp:
                   disp += ' + '
                disp += f'{coeff}' if coeff != 1 else ' 1 ' if coeff == 1 and self.expr[coeff] == [{'':0}] else ''
            for count,expr_ in enumerate(self.expr[coeff]):
                if count:
                    disp += ' - 1 ' if coeff == -1 and self.expr[coeff] == [{'':0}] else ' + 1' if coeff ==  1 and self.expr[coeff] else f' - ' if coeff == -1 else f' - {abs(coeff)}' if coeff < 0 else f' + {coeff}' if coeff > 1 else ' + '
                for var in expr_:
                    disp += f'{var}' if var else str(abs(coeff)) if not disp else ''
                    if expr_[var] != 1 and expr_[var] != 0:
                        disp += f"^{expr_[var]}"
                count += 1
        if not disp:
            return '0'
        return disp
    def __len__(self):
        elnt = 0
        for expressions in self:
            elnt += 1
        return elnt
    def str(self,dic):
        disp = ''
        for var in dic[coeff]:
            disp += f'{var}'
            if dic[coeff][var] != 1:
                disp += f"^{[coeff][var]}"
        return disp
    def __add__(self,other):
        self_ = deepcopy(self)
        sett = 0
        if isinstance(other,str) or isinstance(other,float) or isinstance(other,int):
            other = E(f'{other}')
        ## check duplicates
        if len(other) > 1:
            for expr in other:
                self_ += expr
        if len(other) == 1:
            for coeff in other.expr:
                if coeff not in self_.expr:
                    self_.expr[coeff] = []
                self_.expr[coeff].append(other.expr[coeff][0])
        return self_
    
    def __sub__(self,other):
        try:
            self_ = deepcopy(self)
            sett = 0
            if isinstance(other,str) or isinstance(other,float) or isinstance(other,int):
                other = E(f'{other}')
        ## check duplicates
            if len(other) > 1:
                for expr in other:
                    self_ -= expr
            if len(other) == 1:
                for coeff in other.expr:
                    coeff *= -1
                    if coeff not in self_.expr:
                        self_.expr[coeff] = []
                    self_.expr[coeff].append(other.expr[-1*coeff][0])
        except RuntimeError:
            self_ = E('0')
        
        return self_
    def cal(self,values = {}):
        result = 0;used={}
        for coeff in self.expr:
            for var in self.expr[coeff]:
                term = coeff
                for var_ in var:
                    if not var_:
                        continue
                    if not values:
                        if var_ not in used:
                            ex = eval(input(f'{var_}? '))
                            used.update({f'{var_}':ex})
                        else: ex = used[var_]
                    else:
                        ex = values[var_]
                    term *= ex**var[var_]
                result += term
        return result

    def lin_diff(self,var_ = 'x'):
        tmp = {}
        for expr_ in self:
            tmp_ = E(expr_)
            for coeff, var in tmp_.expr.items():
                val_=[]; pw = 0
                for var__ in var:
                    val = {}
                    for __var in var__:
                        if __var == var_:
                            pw = var__[__var]
                            if var__[__var] - 1:
                                val[var_] = var__[__var] - 1
                        else:
                            val[__var] = var__[__var]
                    val_.append(val)
                if pw *coeff:
                    if pw * coeff in tmp:
                        tmp[pw* coeff].append(val_)
                    else:
                        tmp[pw* coeff] = val_
        return E(tmp,True).simp()
                
            
    def simp(self,psort = False):
        for coeff, var in self.expr.items():
            if var == [{}]:
                self.expr[coeff] =[{'':0}]
        alpha = ['a','b','c','d',
                 'f','g','h','i','j',
                 'k','l','m','n','o',
                 'p','q','r','s','t',
                 'u','v','w','x','y',
                 'z']
        res = {}; sim = '';arr = {};arr_={};_arr_ = []
        # Arranging each term in order
        for coeff,var in self.expr.items():
            for var_ in var:
                for alpha_ in alpha:
                    if alpha_ in var_:
                        arr[alpha_] = var_[alpha_]
                if not arr:
                    arr = {'':0}
                _arr_.append(arr);arr =  {}
            arr_[coeff] = _arr_; _arr_ = []
        sort = E('0');used = []
        for coeff, var in arr_.items():
            if var == [{}]:
                arr_[coeff] =[{'':0}]
        
        # Odering the terms of the Expressions
        for alpha_ in alpha:
            for count,expre in enumerate(E(arr_,True)):
                if alpha_ in expre and not count in used:
                    if alpha_ == 'j':
                        imj =  E(expre)
                        cof = list(imj.expr)[0]
                        pw = imj.expr[cof][0]['j']
                        imj.expr[cof][0]['j']  = pw % 2
                        if pw % 2:
                            pw-=1
                            if pw >3:
                                pw = (pw % 4)
                            elif pw < 4:
                                pw = (pw % 2)
                            pw = -1 if pw else 1
                            expre = str(E(dict(zip([cof* pw],list(imj.expr.values()))),True))
                        else:
                            if pw >3:
                                pw = (pw % 4)
                            elif pw < 4:
                                pw = (pw % 2)
                            pw = -1 if pw else 1
                            expre = cof * pw
                    sort += expre
                    used.append(count)
        for count,exprs in enumerate(E(arr_,True)):
            sett = 3
            for alphas in alpha:
                if alphas in exprs:
                    sett = 0
            if sett and count not in used:
                sort += int(float(exprs)) if intable(exprs) else exprs
        arr_ = sort.expr

        # Collecting like times
        for coeff, var in arr_.items():
            if not coeff:
                continue
            for var_ in var:
                if not con(var_) in res:
                    res.update({con(var_):coeff})
                else:
                    res[con(var_)] += coeff
        # Restoring the dict structure and removing every zero coefficient
        for coeff, var in res.items():
            if not var or not coeff:
                continue
            if var > 0 and sim:
                sim += '+'
            sim += str(int(var) if intable(var) else var)
            if coeff != '^0':
                sim += coeff
        if not sim:
            sim = '0'
        return E(sim) if psort else E(sim).__psort__()
    
    def pow(self,exprs,var = ''):
        ex = 0
        exp = E(exprs)
        for coeff,_var in exp.expr.items():
            for var_ in _var[0]:
                ex += _var[0][var_] if not var else 0 if var and var_ != var else _var[0][var_]
        return ex
    
    def deg(self):
        pows = []
        for exprs in self:
            pows.append(self.pow(exprs))
        return max(pows) if pows else 0
    def __delitem__(self,other):
        new = E('0')
        for count,exprs in enumerate(self):
            if not count - other + 1:
                continue
            new += exprs
        return new.simp()
    
    def __setitem__(self,other,value):
        new = E('0')
        for count,exprs in enumerate(self):
            new += value if not count - other + 1 else exprs
        return new.simp()
    
    def islin(self):
        return True if self.deg() == 1 else False
    
    def __pop__(self,other):
        sv = self[other]
        del self[other]
        return sv
    
    def __psort__(self):
        
        if not self:
            return self
        self_ = self.simp(True)
        
        alpha = ['a','b','c','d',
                 'f','g','h','i','j',
                 'k','l','m','n','o',
                 'p','q','r','s','t',
                 'u','v','w','x','y',
                 'z']
        vars_ = E('0')
        pows = [];__vars__ = {};var_pt = []
        # Gathering powers
        for count,exprs in enumerate(self_):
            pows.append(self.pow(exprs))
            if not self.pow(exprs):
                var_pt.append(count +1)
        pows_ = list(set(pows));pows_.sort();pows_.reverse()
        used = [];

        # Reodering
        for memebers in pows_:
            for alphas in alpha:
                for count,items in enumerate(pows):
                    if items != memebers or count in used:
                        continue
                    if alphas in self_[count+1]:
                        vars_ +=  self_[count+1]
                        used.append(count)
        for var_pts in var_pt:
            sett = 6
            for alphas in alpha:
                if alphas in self_[var_pts]:
                    sett = 0
            if sett:
                vars_ += self_[var_pts]
        for coeff, var in vars_.expr.items():
            if coeff:
                __vars__[coeff] = var
        return E(__vars__,True).simp(True)
            
    class iter:
        def __init__(self,expr):
            self.expr = expr.expr
            self.it = self.get()
        def get(self):
            for coeff in self.expr:
                disp = ''
                if not coeff:
                    continue
                if coeff < 0:
                    disp = f' - {abs(coeff)}' if coeff != -1 else ' - 1 ' if self.expr[coeff] == [{'':0}] else ' - '
                else:
                    disp = f'{coeff}' if coeff != 1 else ' 1 ' if coeff == 1 and self.expr[coeff] == [{'':0}] else ''
                for count,expr_ in enumerate(self.expr[coeff]):
                    if count:
                        disp = f' - {abs(coeff)}' if coeff < 0 else f'{coeff}' if coeff > 1 else ''
                    sett = 6
                    for var in expr_:
                        disp += f'{var}' if var else str(abs(coeff)) if not disp else ''
                        if expr_[var] != 1 and expr_[var] != 0:
                            disp += f"^{expr_[var]}"
                    yield disp
                    count += 1

        def __next__(self):
            return next(self.it)
        def __iter__(self):
            return self
    def __iter__(self):
        return self.iter(self)
    def __getitem__(self,other):
        for count,expr_ in enumerate(self):
            if count + 1 == other:
                return expr_
    def __truediv__(self,other):
        self_ = deepcopy(self)
        val = {};val_ = {}
        if isinstance(other,str):
            other = E(other)
        if len(other) == 1:
            val = E('0')
            for exprs in self:
                Expr = E(exprs)
                for _coeff,_var in Expr.expr.items():
                    for coeff, var in other.expr.items():
                        for var_ in var[0]:
                            try:
                                if not Expr.expr[_coeff][0][var_] -var[0][var_]:
                                    Expr.expr[_coeff][0].pop(var_)
                                else:
                                    Expr.expr[_coeff][0][var_] -= var[0][var_]
                            except KeyError:
                                Expr.expr[_coeff][0][var_] = - var[0][var_]
                    val += str(E({_coeff/coeff:[Expr.expr[_coeff][0]]},True).simp())
            
        if len(other) > 1:
            self_ = copy(self)
            Quo = E('0')
            while True:
                factor = E(self_[1])/other[1]
                sub = factor * other
                rem = (self_ - sub).simp()
                Quo += factor
                if not rem:
                    break
                self_ = rem
            val = Quo
        return round(val.simp(),5)

    def coeff(self,other):
        for exprs in self.simp():
            if other in exprs:
                return list(E(exprs).expr)[0]
        return 0
    
    def __round__(self,other):
        coeff = [round(coeff,other) for coeff in self.expr]
        vars_ = list(self.expr.values())
        return E(dict(zip(coeff,vars_)),True)
    def __pow__(self,other):
        self_ = copy(self)
        for interger in range(other-1):
            self_ *= self
        return self_
    def __rmul__(self,other):
        return self * other
    def __and__(self,other,fix = 6):
        starter = 1
        self_ = copy(self.simp())
        while True:
            try:
                root = self_.New_Raph(self_,other)
                root = int(round(root,6)) if intable(round(root,6)) else round(root,6)
                yield root
                self_ /= E(other).simp() - root
                if not self_:
                    break
            except ZeroDivisionError:
                break

    def New_Raph(self,eq, var):
        starter = 1
        while True:
            grad = self.cal({var:starter})/self.lin_diff(var).cal({var:starter})
            starter -= grad
            if not grad:
                break
        return starter
    def __mul__(self,other):
        if isinstance(other,str) or isinstance(other,int) or isinstance(other,float) or isinstance(other, int32):# Ensuring that we are dealing with E object
            other = E(str(other))
        sef_ = {};val_ = {};_val_= []; statr = 0
        for __exprs__ in other:
            coeff = list(E(__exprs__).expr)[0]
            var = list(E(__exprs__).expr.values())[0]
            sef = {}
            coeff_ = []; var0 = []
            for coeff__, var_ in self.expr.items():
               coeff_ += [coeff__ * coeff]
               var0.append(var_)
               sef.update(dict(zip(coeff_,var0)))
            _self = deepcopy(self)
            sef_ = E(sef,True)
            _sef_ = E({},True)
            for _var in var:
                for _coeff, vars_ in sef_.expr.items():
                    for vars__ in vars_:
                        for _vars__ in vars__:
                            if _vars__ in _var:
                                pq = vars__[_vars__] + _var[_vars__]
                                if _vars__ == 'j':
                                    val_[_vars__] = pq % 2
                                    _coeff *= (-1)**pq 
                                val_[_vars__] = vars__[_vars__] + _var[_vars__]
                            else:
                                val_[_vars__] = vars__[_vars__]
                            for __vars__ in _var:
                                if __vars__ not in val_:
                                    val_[__vars__] = _var[__vars__]
                        _val_.append(val_);val_ = {}
                    _sef_.expr[int(_coeff) if intable(_coeff) else _coeff] = _val_
                    _val_ = []
            if not statr:
                add = _sef_
            else:
                add += _sef_
            statr += 1
        return add.simp() if statr else E('0')
    def __bool__(self):
        if str(self) == '0':
            return False
        return True
    def __copy__(self):
        new = {}
        for coeff,var in self.expr.items():
            new[coeff] = var
        return E(new,True)
    def parse(self):
        new_expr = {}
        for expr in self:
            expr_ = E(expr)
            for coeff, var in expr_.expr.items():
                for var_ in var[0]:
                    new_expr[var_] = coeff
        return new_expr
Es = E('1',True)



class Eqn(E):
    def __init__(self,expr):
        self.eqn1 = expr.simp() if isinstance(expr,E) else E(expr).simp()
        self.num = 1
        self.expr = self.eqn1.expr
    def add(self,eqn):
        exec(f'self.eqn{self.num +1} = eqn.simp() if isinstance(eqn,E) else Eqn("{eqn}").simp()')
        self.num += 1
    def __str__(self):
        for nomb in range(1,self.num+1):
            exec(f'print(self.eqn{nomb})')
        return ''
    def count(self):
        cont = 0
        for eqns in self:
            if eqns:
                cont += 1
        return cont
    def __and__(self,other):
        self_ = copy(self)
        Force = False; deg = []
        exc = {'#': 1, '##':2}
        try:
            if other[-1] in exc:
                Force = exc[other[-1]]
                del other[-1]
        except Exception:
            pass
        if self.num != len(other):
            raise InvalidOperation('Equations')
        for nomb in range(1,self.num+1):
            exec(f'deg.append(self.eqn{nomb}.deg())')
        
        if max(deg) == 1:
            
            alpha = ['a','b','c','d',
                 'f','g','h','i','j',
                 'k','l','m','n','o',
                 'p','q','r','s','t',
                 'u','v','w','x','y',
                 'z']
            var_list = []
            for alpha_ in alpha:
                for eqns in self:
                    if alpha_ in eqns.parse():
                        var_list.append(alpha_)
                    if alpha_ in var_list:
                        break
            if len(var_list) > self.num and not Force:
                raise DimensionError
            res = {}
            while len(var_list) != self_.count():
                for i in range(self_.num):
                    if not eval(f'self_.eqn{i+1}.__bool__()'):
                        del self_[i+1]
                        del other[i]
                self__ = copy(self_)
                for count,eqns in enumerate(self__):
                    eqns_ = eqns
                    for exprs in eqns:
                        if var_list[0] in exprs:
                            other[count] -= eqns_.coeff(var_list[0]) * (Force - 1)
                            del eqns_[count+1]
                    exec(f'self_[{count+1}] = eqns_')
                
                res[var_list[0]] = Force - 1
                del var_list[0]
            if not len(var_list) -1:
                for count,eqns in enumerate(self__):
                    if var_list[0] in str(eqns):
                        res[var_list[0]] = other[0] / eqns.coeff(var_list[0])
                        return res
            delta = []
            mat = [len(var_list),len(var_list)]
            for eqns in self:
                for var in var_list:
                    try:
                        mat.append(eqns.parse()[var])
                    except Exception:
                        mat.append(0)
                    
            delta.append(mat)
            for vars_ in var_list:
                mat = [len(var_list),len(var_list)]
                for count,eqns in enumerate(self):
                    for var in var_list:
                        try:
                            mat.append(other[count]) if vars_ == var else mat.append(eqns.parse()[var])
                        except Exception:
                            mat.append(0)
                delta.append(mat)
            det = abs(arm.Matrix(delta[0]))
            for count,var in enumerate(var_list,1):
                value = abs(arm.Matrix(delta[count]))/det
                res[var] = int(value) if intable(value) else value
            return res
    def __delitem__(self,other):
        for numbers in range(other, self.num):
            exec(f'self.eqn{numbers} = self.eqn{numbers+1}')
        exec(f'del self.eqn{self.num};self.num -= 1')
    def pop(self,other):
        item = eval(f'self[{other}]')
        del self[other]
        return item
    def __getitem__(self,other):
        return eval(f'self.eqn{other}')
    def __setitem__(self,other,value):
        exec(f'self.eqn{other} = Eqn("{value}").simp()')
    class Eqn_iter:
        def __init__(self,eqn):
            self.eqn = eqn
            self.it = self.get()
        def get(self):
            for nomb in range(1,self.eqn.num+1):
                yield eval(f'self.eqn.eqn{nomb}')
        def __next__(self):
            return next(self.it)
        def __iter__(self):
            return self
    def __iter__(self):
        return self.Eqn_iter(self)
    def __copy__(self):
        for count,eqns in enumerate(self):
            if not count:
                alt = Eqn(eqns)
            else: alt.add(eqns)
        return alt
    
call = False

def main():
    global call
    call = True

if __name__ == '__name__':
    main()
