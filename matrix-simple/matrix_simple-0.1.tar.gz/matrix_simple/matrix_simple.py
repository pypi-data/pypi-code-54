class Matrix:
    """ Matrix class for creating matricies and handling matrix operations.
    
    Attributes:
        height (int) number of rows in the matrix
        width (int) number of columns in the matrix
        values (obj[][]) nested list of objects with the same type
            outer level is rows, inner is columns
          
    """
    def __init__(self, values):
                
        self.values = values
        self.height = len(values)
        self.width = len(values[0])
        
    def get_val(self, row, col):
        return self.values[row][col]
    
    def set_val(self, row, col, val):
        self.values[row][col] = val
        
    def pretty_print(self):
        for row in self.values:
            row_str = ''
            for val in row:
                row_str += str(val) + ' | '
            print(row_str[:-2], '\n')
            
    def __add__(self, other):
        try:
            assert self.height == other.height, 'number of rows does not match'
            assert self.width == other.width, 'number of columns does not match'
        except AssertionError as error:
            raise
        
        sum_values = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(self.get_val(i, j) + other.get_val(i, j))
            sum_values.append(row)
        return Matrix(sum_values)
    
    def mul_const(self, other):
        mul_values = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(self.get_val(i, j) * other)
            mul_values.append(row)
        return Matrix(mul_values)
    
    def __mul__(self, other):
        if not isinstance(other, Matrix):
            return self.mul_const(other)
        try:
            assert self.width == other.height, 'inner dimension does not match'
        except AssertionError as error:
            raise
            
        mul_values = []
        for i in range(self.height):
            row = []
            for j in range(other.width):
                val = 0
                for k in range(self.width):
                    val += self.get_val(i, k) * other.get_val(k, j)
                row.append(val)
            mul_values.append(row)
        return Matrix(mul_values)
            
    def __rmul__(self, other):
        if not isinstance(other, Matrix):
            return self.mul_const(other)
        
    