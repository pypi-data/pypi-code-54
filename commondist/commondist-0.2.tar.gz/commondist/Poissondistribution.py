import math
import matplotlib.pyplot as plt
from .Generaldistribution import Distribution

class Poisson(Distribution):
    
    """ Poisson distribution class for calculating and visualizing a Poisson 
    distribution.
    
    Attributes:
        mean (float) representing the mean value of the distribution
        stdev (float) representing the standard deviation of the distribution
        data_list (list of floats) a list of floats to be extracted from the 
        data file.
               
    """

    def __init__(self, lam=1):

        self.lam = lam
        Distribution.__init__(self, self.calculate_mean(),
                              self.calculate_stdev(), self.calculate_skew(),
                              self.calculate_kurt())
    
                        
    def calculate_mean(self):
    
        """Function to calculate the mean of the data set.
        
        Args: 
            None
        
        Returns: 
            float: mean of the data set
    
        """
        
        self.mean = 1.0 * self.lam

        return self.mean


    def calculate_stdev(self):
    
        """Function to calculate the standard deviation of the data set.
        
        Args: 
            None
        
        Returns: 
            float: standard deviation of the data set
    
        """
        
        self.stdev = math.sqrt(self.lam)
        
        return self.stdev
    

    def calculate_skew(self):
    
        """Function to calculate the skewness of the data set.
        
        Args: 
            None
        
        Returns: 
            float: skewness of the data set
    
        """

        self.skew = self.lam ** -0.5
                
        return self.skew


    def calculate_kurt(self):
    
        """Function to calculate the excess kurtosis of the data set.
        
        Args: 
            None
        
        Returns: 
            float: excess kurtosis of the data set
    
        """

        self.kurt = self.lam ** -1
                
        return self.kurt
    

    def replace_stats_with_data(self):
    
        """Function to calculate p and n from the data set
        
        Args: 
            None
        
        Returns: 
            float: the p value
            float: the n value
    
        """
    
        self.mean = self.calculate_mean()
        self.stdev = self.calculate_stdev()
        self.skew = self.calculate_skew()
        self.kurt = self.calculate_kurt()
        
        return self.p, self.n


    def pdf(self, x):
	    """Probability density function calculator for the lognormal 
	    distribution.
	    
	    Args:
		    x (int): point for calculating the probability density 
		    function
		    
	    
	    Returns:
		    float: probability density function output
	    """
	    
	    return ((lam ** x) * (e ** -self.lam)) / math.factorial(x)

	
    def plot_histogram_pdf(self, n_spaces=50):
    
	    """Function to plot the normalized histogram of the data and a 
	    plot of the probability density function along the same range.
	    
	    Args:
		    n_spaces (int): number of data points 
	    
	    Returns:
		    list: x values for the pdf plot
		    list: y values for the pdf plot
		    
	    """
	    
	    mu = self.mean
	    sigma = self.stdev
    
	    min_range = min(self.data)
	    max_range = max(self.data)
	    
	    # calculates the interval between x values
	    interval = 1.0 * (max_range - min_range) / n_spaces
    
	    x = []
	    y = []
	    
	    # calculate the x values to visualize
	    for i in range(n_spaces):
		    tmp = min_range + interval*i
		    x.append(tmp)
		    y.append(self.pdf(tmp))
    
	    # make the plots
	    fig, axes = plt.subplots(2,sharex=True)
	    fig.subplots_adjust(hspace=.5)

	    axes[0].hist(self.data, density=True)
	    axes[0].set_title('Normed Histogram of Data')
	    axes[0].set_ylabel('Density')
    
	    axes[1].plot(x, y)
	    axes[1].set_title('Poisson Distribution for \n \
	    Sample Mean and Sample Standard Deviation')
	    axes[1].set_ylabel('Density')
	    plt.show()

	    return x, y


    def __add__(self, other):
        
        """Function to add together two Poisson distributions.
        
        Args:
            other (Poisson): Poisson instance
            
        Returns:
            Poisson: Poisson distribution
            
        """
        
        result = Poisson()
        result.lam = self.lam + other.lam
        result.calculate_mean()
        result.calculate_stdev()
        result.calculate_skew()
        result.calculate_kurt()
        
        return result
    

    def __repr__(self):
    
        """Function to output the characteristics of the Lognormal instance.
        
        Args:
            None
        
        Returns:
            string: characteristics of the Lognormal
        
        """
        
        return "mean {} \n standard deviation {} \n skewness {} \n\
        kurtosis {}".format(self.mean, self.stdev, self.skew, self.kurt)
