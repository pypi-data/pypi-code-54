# Any changes to the distributions library should be reinstalled with
#  pip install --upgrade .

# For running unit tests, use
# /usr/bin/python -m unittest test

import unittest

from Describelinearmodel import DescribeLinearModel

class TestDescribeLinearModelClass(unittest.TestCase):
    def setUp(self):
        self.linmod_1 = DescribeLinearModel([1,2,3,4,5], [0.5, 1, 1.5, 2, 2.5])
        self.linmod_2 = DescribeLinearModel()
        self.linmod_2.read_file_x_data("test_set_x.txt", True)
        self.linmod_2.read_file_y_data("test_set_y.txt", True)

    def test_initialization(self):
        self.assertEqual(self.linmod_1.x_data, [1,2,3,4,5], 'incorrect x_data')
        self.assertEqual(self.linmod_1.y_data, [0.5, 1, 1.5, 2, 2.5], 'incorrect y_data')

    def test_read_file_x_data(self):
        self.assertEqual(self.linmod_2.x_data,\
         [0.4, 0.8, 2, 1.45, 4, 6.1, 0.1, 4.4, 2.05, 10], 'data not read in correctly')

    def test_read_file_y_data(self):
        self.assertEqual(self.linmod_2.y_data,\
         [1, 1.9, 3.55, 3.3, 8.5, 11.2, 0.22, 8, 3.4, 12.5], 'data not read in correctly')

    def test_calculate_r(self):
        self.assertEqual(round(self.linmod_2.calculate_r(), 2), 0.96, 'calculated r not as expected')

    def test_calculate_r_squared(self):
        self.assertEqual(round(self.linmod_2.calculate_r_squared(), 3), 0.914, 'calculated r_squared not as expected')

    def test_calculate_slope(self):
        self.assertEqual(round(self.linmod_2.calculate_slope(), 2), 1.35, 'calculated slope not as expected')

    def test_calculate_intercept(self):
        self.assertEqual(round(self.linmod_2.calculate_intercept(), 2), 1.13, 'calculated intercept not as expected')

tests = TestDescribeLinearModelClass()
tests_loaded = unittest.TestLoader().loadTestsFromModule(tests)
unittest.TextTestRunner().run(tests_loaded)
