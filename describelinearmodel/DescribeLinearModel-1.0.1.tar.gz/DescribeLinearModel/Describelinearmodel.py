import sys, os
import numpy as np
import matplotlib.pyplot as plt

class DescribeLinearModel:

    def __init__(self, x_data = [], y_data = []):

        """Method for calculating and visualizing a regression line from data points.

        Args:
			x_data (list of floats): x coordinates of data points
            y_data (list of floats): y coordinates of data points

    	Attributes:
            x_data (list of floats): x coordinates of data points
            y_data (list of floats): y coordinates of data points
    		slope_m (float): representing the slope of the regression line
            intercept_c (float): representing the y-intercept of the regression line
    		r (float): representing pearson's correlation coefficient of the data points
    		r_squared (float): coefficient of determination which measures the strength of the relationship between the model and the dependend variable
    	"""

        self.x_data = x_data
        self.y_data = y_data
        self.slope_m = 0
        self.intercept_c = 0
        self.r = 0
        self.r_squared = 0


    def read_file_x_data(self, file_x_data, new_list = True):

        """Method to read in x coordinates of data points from a txt file. The txt file should have one number (float) per line. The numbers are stored in the x_data attribute.

		Args:
			file_name (string): name of a file to read from
            new_list (boolean): True if data to be stored in new list
                                False if data to be stored / appedended in existing list

		Returns:
			None
		"""

        with open(os.path.join(sys.path[0], file_x_data)) as file:
            if new_list == True:
                list_x_data = []
            else:
                list_x_data = self.x_data
            line = file.readline()
            while line:
                list_x_data.append(float(line))
                line = file.readline()
        file.close()
        self.x_data = list_x_data

    def read_file_y_data(self, file_y_data, new_list = True):

        """Method to read in y coordinates of data points from a txt file. The txt file should have one number (float) per line. The numbers are stored in the y_data attribute.

		Args:
			file_name (string): name of a file to read from
            new_list (boolean): True if data to be stored in new list
                                False if data to be stored / appedended in existing list

		Returns:
			None
		"""

        with open(os.path.join(sys.path[0], file_y_data)) as file:
            if new_list == True:
                list_y_data = []
            else:
                list_y_data = self.y_data
            line = file.readline()
            while line:
                list_y_data.append(float(line))
                line = file.readline()
        file.close()
        self.y_data = list_y_data

    def set_data_point(self, new_x, new_y):

        """This method appends new data point to existing data attributes (x_data, y_data).

        Args:
            new_x (float): new x coordinate of data point
            new_y (float): new y coordinate of data point
        Returns:
            None
        """

        self.x_data.append(float(new_x))
        self.y_data.append(float(new_y))

    def change_data_point(self, index_data_point, new_x, new_y):

        """This method overwrites existing data point from existing data attributes (x_data, y_data).

        Args:
            index_data_point (int): number of index of data point to be changed in existing data attributes
            new_x (float): new x coordinate of data point
            new_y (float): new y coordinate of data point
        Returns:
            None
        """

        self.x_data[index_data_point] = new_x
        self.y_data[index_data_point] = new_y

    def calculate_slope(self):

        """Method to calculate the slope of the regression line from all data points.

		Args:
			None

		Returns:
			float: slope m of the regression line
		"""

        product_mean_x_mean_y = np.mean(self.x_data) * np.mean(self.y_data)
        mean_product_x_y = np.mean([x * y for x, y in zip(self.x_data, self.y_data)])
        mean_x_squared = pow(np.mean(self.x_data), 2)
        mean_product_x_x = np.mean([x * y for x, y in zip(self.x_data, self.x_data)])

        numerator = product_mean_x_mean_y - mean_product_x_y
        denominator = mean_x_squared - mean_product_x_x
        if denominator == 0:
            return 0
        else:
            self.slope_m = (numerator/denominator)
            return self.slope_m


    def calculate_intercept(self):

        """Method to calculate the y-intercept c of the regression line from all data points.

		Args:
			None

		Returns:
			float: y intercept c of the regression line
		"""

        self.slope_m = self.calculate_slope()
        self.intercept_c = np.mean(self.y_data) - self.slope_m * np.mean(self.x_data)
        return self.intercept_c

    def calculate_r(self):

        """Method to calculate pearson's correlation coefficient r from all data points.

		Args:
			None

		Returns:
			float: pearson's r of all data points
		"""

        assert len(self.x_data) == len(self.y_data)
        n_data_points = len(self.x_data)
        assert n_data_points > 0

        sum_x = float(sum(self.x_data))
        sum_y = float(sum(self.y_data))
        sum_x_squared = sum(map(lambda x: pow(x, 2), self.x_data))
        sum_y_squared = sum(map(lambda x: pow(x, 2), self.y_data))
        sum_product_x_y = sum(map(lambda x, y: x * y, self.x_data, self.y_data))
        numerator = sum_product_x_y - (sum_x * sum_y / n_data_points)
        denominator = pow((sum_x_squared - pow(sum_x, 2) / n_data_points) *\
                          (sum_y_squared - pow(sum_y, 2) / n_data_points), 0.5)
        if denominator == 0:
            return 0
        else:
            self.r = (numerator/denominator)
            return self.r

    def calculate_r_squared(self):

        """Method to calculate the coefficient of determination r_squared from all data points.

		Args:
			None

		Returns:
			float: coefficient of determination r_squared of all data points
		"""

        self.r = self.calculate_r()
        self.r_squared = pow(self.r, 2)
        return self.r_squared


    def plot_scatterplot(self):

        """Method to output a scatterplot including a regression line of the instance variable data using matplotlib pyplot library.

		Args:
			None

		Returns:
			None
		"""

        self.slope_m = self.calculate_slope()
        self.intercept_c = self.calculate_intercept()
        self.r = self.calculate_r()
        self.r_squared = self.calculate_r_squared()

        ### plot scatterplot
        fig, ax = plt.subplots()
        ax.scatter(self.x_data, self.y_data, s = 20, label= f'data points\n  r={"%.3f"%(self.r)}')
        ax.set_aspect(1)
        ax.set_title('Scatterplot Linear Model')
        ax.set_xlabel('x - independent variable')
        ax.set_ylabel('y - dependent variable')

        ### plot regression line
        x = np.linspace(min(self.x_data), max(self.x_data), 2)
        y = self.slope_m * x + self.intercept_c
        plt.plot(x, y, color = 'r', linewidth = 1.5, label= f'regression line\n  m={"%.3f"%(self.slope_m)}\n  c={"%.3f"%(self.intercept_c)}')
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.grid()
        plt.show()
        plt.close()

    def __repr__(self):

        """Method to output the characteristics of the Linear Model instance including slope m, intercept c, pearson's r and coefficient r_squared.

		Args:
			None

		Returns:
			string: characteristics of the Linear Model slope m, intercept c and pearson's r

		"""

        self.slope_m = self.calculate_slope()
        self.intercept_c = self.calculate_intercept()
        self.r = self.calculate_r()
        self.r_squared = self.calculate_r_squared()

        return 'linear regression line: {} (slope m), {} (intercept c)\n\
pearsons correlation coefficient r: {}'.format("%.6f" %(self.slope_m),
                                                   "%.6f" %(self.intercept_c),
                                                   "%.6f" %(self.r))
