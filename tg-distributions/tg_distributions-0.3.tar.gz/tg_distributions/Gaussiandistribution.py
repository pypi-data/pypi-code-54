import math
import matplotlib.pyplot as plt
from .Generaldistribution import Distribution

class Gaussian(Distribution):
	""" 
	Gaussian distribution class for calculating and visualizing a Gaussian distribution.
	
	Attributes:
		mean (float) representing the mean value of the distribution
		stdev (float) representing the standard deviation of the distribution
		data_list (list of floats) a list of floats extracted from the data file
			
	"""
	def __init__(self, mu=0, sigma=1):
		
		Distribution.__init__(self, mu, sigma)
	
		
	
	def calculate_mean(self):
	
		"""
		Function to calculate the mean of the data set.
		
		Args: 
			None
		
		Returns: 
			float: mean of the data set
	
		"""
					
		
		self.mean = sum(self.data) / len(self.data)
		
		return self.mean



	def calculate_stdev(self, sample=True):


		"""
		Function to calculate the standard deviation of the data set.
		
		Args: 
			sample (bool): whether the data represents a sample or population
		
		Returns: 
			float: standard deviation of the data set

	
		"""
		variance_numerator = 0
		for indi_data in self.data:
			variance_numerator += (indi_data - self.mean)**2
		if sample==True:
			variance_denominator = len(self.data) - 1 
		else:
			variance_denominator = len(self.data)
		self.stdev = math.sqrt(variance_numerator / variance_denominator)
		return self.stdev

		
	def plot_histogram(self):
		"""Function to output a histogram of the instance variable data using matplotlib pyplot library.
		
		Args:
			None
			
		Returns:
			None
		"""
		plt.hist(self.data)
		plt.title('Histogram of Data')
		plt.xlabel('data')
		plt.ylabel('count')
		
		
	def __add__(self, other):
		
		"""Function to add together two Gaussian distributions
		
		Args:
			other (Gaussian): Gaussian instance
			
		Returns:
			Gaussian: Gaussian distribution
			
		"""
		
		result = Gaussian()
		result.mean = self.mean + other.mean
		result.stdev = math.sqrt(self.stdev ** 2 + other.stdev ** 2)
		
		return result
		
		
	def __repr__(self):
	
		"""Function to output the characteristics of the Gaussian instance
		
		Args:
			None
		
		Returns:
			string: characteristics of the Gaussian
		
		"""
		
		return "mean {}, standard deviation {}".format(self.mean, self.stdev)