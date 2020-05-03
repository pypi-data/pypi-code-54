# For running unit tests, use
# /usr/bin/python -m unittest test

import unittest

from matrix_simple import Matrix

class TestMatrixClass(unittest.TestCase):
    def setUp(self):
        values = [[0,1,2],[3,4,5],[6,7,8]]
        self.matrix = Matrix(values)

    def test_initialization(self): 
        self.assertEqual(self.matrix.height, 3, 'incorrect height')
        self.assertEqual(self.matrix.width, 3, 'incorrect width')  

    def test_add(self):
        values_1 = [[0,1,2],[3,4,5],[6,7,8]]
        values_2 = [[0,1,2],[3,4,5],[6,7,8]]
        matrix_1 = Matrix(values_1)
        matrix_2 = Matrix(values_2)
        matrix_sum = matrix_1 + matrix_2
        
        sum_values = [[0,2,4],[6,8,10],[12,14,16]]
        self.assertEqual(matrix_sum.values, sum_values)
        
    def test_add_bad_height(self):
        values_1 = [[0,1,2],[3,4,5],[6,7,8]]
        values_2 = [[0,1,2],[3,4,5]]
        matrix_1 = Matrix(values_1)
        matrix_2 = Matrix(values_2)
        with self.assertRaises(AssertionError):
            matrix_1 + matrix_2
        
    def test_add_bad_width(self):
        values_1 = [[0,1,2],[3,4,5],[6,7,8]]
        values_2 = [[0,1],[3,4],[6,7]]
        matrix_1 = Matrix(values_1)
        matrix_2 = Matrix(values_2)
        with self.assertRaises(AssertionError):
            matrix_1 + matrix_2
        
    def test_mul_const(self):
        mul_mat = self.matrix * 2
        mul_values = [[0,2,4],[6,8,10],[12,14,16]]
        self.assertEqual(mul_mat.values, mul_values)
       
    def test_rmul_const(self):
        mul_mat = 2 * self.matrix
        mul_values = [[0,2,4],[6,8,10],[12,14,16]]
        self.assertEqual(mul_mat.values, mul_values)
        
    def test_mul(self):
        values_1 = [[0,1],
                    [2,3]]
        values_2 = [[0,1],[2,3]]
        matrix_1 = Matrix(values_1)
        matrix_2 = Matrix(values_2)
        mul_mat = matrix_1 * matrix_2
        
        mul_values = [[2,3],[6,11]]
        self.assertEqual(mul_mat.values, mul_values)
        
    def test_mul_bad_dims(self):
        values_1 = [[0,1,2,3],[4,5,6,7]]
        values_2 = [[0,1],[3,4],[6,7]]
        matrix_1 = Matrix(values_1)
        matrix_2 = Matrix(values_2)
        with self.assertRaises(AssertionError):
            matrix_1 * matrix_2
            
    def test_mul_non_square(self):
        values_1 = [[0,1],
                    [1,0],
                    [1,1]]
        values_2 = [[0,1,2],
                    [3,4,5]]
        matrix_1 = Matrix(values_1)
        matrix_2 = Matrix(values_2)
        mul_mat = matrix_1 * matrix_2
        
        mul_values = [[3,4,5],[0,1,2],[3,5,7]]
        self.assertEqual(mul_mat.values, mul_values)

if __name__ == '__main__':
    unittest.main()