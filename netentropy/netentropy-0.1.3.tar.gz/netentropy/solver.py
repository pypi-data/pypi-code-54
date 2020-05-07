from ortools.sat.python import cp_model
import math
from collections import Counter
from sklearn import metrics


class CpModelSolutionCallback(cp_model.CpSolverSolutionCallback):
    def __init__(self, limit=math.inf):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__solution_count = 0
        self.__solution_limit = limit

    def on_solution_callback(self):
        self.__solution_count += 1
        
        if self.__solution_count >= self.__solution_limit:
            print('Stop search after %i solutions' % self.__solution_limit)
            self.StopSearch()

    def solution_count(self):
        return self.__solution_count
        

class Solver():
    
    def __init__(self, community_dist_1=None, community_dist_2=None, verbose=False, max_solutions=math.inf):
        self.comm_1 = community_dist_1
        self.comm_2 = community_dist_2
        self.a = list(Counter(community_dist_1).values())
        self.b = list(Counter(community_dist_2).values())
        self.verbose = verbose
        self.solution_callback = CpModelSolutionCallback(limit=max_solutions)
        
    def entropy_a(self):
        probs = list(map(lambda x: x / sum(self.a), self.a))
        weighted_info_content = list(map(lambda x: x * math.log(x, 2), probs))
        return sum(weighted_info_content)*(-1)
        
    def entropy_b(self):
        probs = list(map(lambda x: x / sum(self.b), self.b))
        weighted_info_content = list(map(lambda x: x * math.log(x, 2), probs))
        return sum(weighted_info_content)*(-1)
    
    def mutual_info(self):
        return metrics.mutual_info_score(self.comm_1, self.comm_2) / math.log(2)
    
    def corrected_mutual_info(self):
        if self.solution_count() == 0:
            raise Exception('No solutions for the corrected term. To get the corrected MI value, first solve for the correction term using Solver.solve_correction_term().')
        return self.mutual_info() - math.log(self.solution_count(), 2) / len(self.comm_1)

    def solve_correction_term(self):
        if len(self.a) == 0:
            raise Exception('First array of community/group numbers is empty! Please set it as')
        if len(self.b) == 0:
            raise Exception('Second array of community/group numbers is empty! Please set it as')
        if sum(self.a) is not sum(self.b):
            raise Exception('The two arrays represent networks with different amount of nodes. Their sums is not equal.')
        
        #Constant declaration
        self.inform('Problem constants:')
        n = sum(self.a)
        R = len(self.a)
        S = len(self.b)
        self.inform(f'n = {n}, R = {R}, S = {S}')
        for i in range(R):
            exec(f'a{i+1} = self.a[i]')
        for i in range(S):
            exec(f'b{i+1} = self.b[i]')
        
        model = cp_model.CpModel()
        
        #Variable declaration
        self.inform('Declaring variables:')
        for i in range(R):
            exp = ''
            for j in range(S):
                exec(f'c{i+1}{j+1} = model.NewIntVar(0, n, \'c{i+1}{j+1}\')')
                exp += f'c{i+1}{j+1}  '
            self.inform(exp)
                
        #Overlooping for code clarity
        self.inform('First set of constraints:')
        for i in range(R):
            exp = ''
            for j in range(S):
                exp += f'+ c{i+1}{j+1} ' if j>0 else f'c{i+1}1 '
            exp += f'== a{i+1}'
            self.inform(exp)
            model.Add(eval(exp))
            
        #Overlooping for code clarity
        self.inform('Second set of constraints:')
        for j in range(S):
            exp = ''
            for i in range(R):
                exp += f'+ c{i+1}{j+1} ' if i>0 else f'c1{j+1} '
            exp += f'== b{j+1}'
            self.inform(exp)
            model.Add(eval(exp))
        
        solver = cp_model.CpSolver()
        self.inform('Starting to solve...')
        status = solver.SearchForAllSolutions(model, self.solution_callback)
        
        self.inform('Found %i solutions' % self.solution_count())
        self.inform('All solutions found: ', status == cp_model.OPTIMAL)
        self.inform('-'*50)
        
        return self.solution_count()
        
    def solution_count(self):
        return self.solution_callback.solution_count()
        
    def correction_term(self):
        if self.solution_count() == 0:
            raise Exception('No solutions for the corrected term. To get the corrected MI value, first solve for the correction term using Solver.solve_correction_term().')
        return math.log(self.solution_count(), 2) / sum(self.a)
        
    def inform(self, *args):
        if self.verbose:
            print(*args)
    