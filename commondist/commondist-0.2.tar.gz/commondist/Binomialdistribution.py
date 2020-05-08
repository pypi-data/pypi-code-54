import math
import matplotlib.pyplot as plt
from .Generaldistribution import Distribution

class Binomial(Distribution):
    
    """ Binomial distribution class for calculating and visualizing a Binomial 
    distribution.
    
    Attributes:
        mean (float) representing the mean value of the distribution
        stdev (float) representing the standard deviation of the distribution
        data_list (list of floats) a list of floats to be extracted from the 
        data file.
        
        p (float) representing the probability of an event occurring
        n (int) number of trials
               
    """

    def __init__(self, prob=0.5, size=20):
                
        self.n = size
        self.p = prob
        Distribution.__init__(self, self.calculate_mean(),
                              self.calculate_stdev(), self.calculate_skew(),
                              self.calculate_kurt())
    

    def calculate_mean(self):
    
        """Function to calculate the mean from p and n.
        
        Args: 
            None
        
        Returns: 
            float: mean of the data set
    
        """

        self.mean = self.p * self.n
                
        return self.mean
    

    def calculate_stdev(self):
    
        """Function to calculate the standard deviation from p and n.
        
        Args: 
            None
        
        Returns: 
            float: standard deviation of the data set
    
        """
        
        self.stdev = math.sqrt(self.n * self.p * (1 - self.p))
        
        return self.stdev
    

    def calculate_skew(self):
    
        """Function to calculate the skewness from p and n.
        
        Args: 
            None
        
        Returns: 
            float: skewness of the data set
    
        """

        self.skew = ((1 - self.p) - self.p) / math.sqrt(self.n * self.p *
                                                        (1 - self.p))
                
        return self.skew


    def calculate_kurt(self):
    
        """Function to calculate the excess kurtosis from p and n.
        
        Args: 
            None
        
        Returns: 
            float: excess kurtosis of the data set
    
        """

        self.kurt = (1 - 6 * self.p * (1 - self.p)) / \
            (self.n * self.p * (1 - self.p))
                
        return self.kurt
    

    def replace_stats_with_data(self):
    
        """Function to calculate p and n from the data set
        
        Args: 
            None
        
        Returns: 
            float: the p value
            float: the n value
    
        """
    
        self.n = len(self.data)
        self.p = 1.0 * sum(self.data) / len(self.data)
        self.mean = self.calculate_mean()
        self.stdev = self.calculate_stdev()
        self.skew = self.calculate_skew()
        self.kurt = self.calculate_kurt()
        
        return self.p, self.n


    def pdf(self, k):
        """Probability density function calculator for the gaussian 
        distribution.
        
        Args:
            x (int): point for calculating the probability density function
            
        
        Returns:
            float: probability density function output
        """

        a = math.factorial(self.n) / (math.factorial(k) *
                                      (math.factorial(self.n - k)))
        b = (self.p ** k) * (1 - self.p) ** (self.n - k)
        
        return a * b
        
    
    def plot_pdf(self):
    
        """Function to plot the pdf of the binomial distribution.
        
        Args:
            None
        
        Returns:
            list: x values for the pdf plot
            list: y values for the pdf plot
            
        """
        
        x = []
        y = []
        
        # calculate the x values to visualize
        for i in range(self.n + 1):
            x.append(i)
            y.append(self.pdf(i))
    
        # make the plots
        plt.bar(x, y)
        plt.title('Distribution of Outcomes')
        plt.ylabel('Probability')
        plt.xlabel('Outcome')
    
        plt.show()
    
        return x, y

        
    def __add__(self, other):
        
        """Function to add together two Binomial distributions with equal p.
        
        Args:
            other (Binomial): Binomial instance
            
        Returns:
            Binomial: Binomial distribution
            
        """
        
        try:
            assert self.p == other.p, 'p values are not equal'
        except AssertionError as error:
            raise
        
        result = Binomial()
        result.n = self.n + other.n
        result.p = self.p
        result.calculate_mean()
        result.calculate_stdev()
        result.calculate_skew()
        result.calculate_kurt()
        
        return result
        
        
    def __repr__(self):
    
        """Function to output the characteristics of the Binomial instance.
        
        Args:
            None
        
        Returns:
            string: characteristics of the Binomial
        
        """
        
        return "mean {} \n standard deviation {} \n skewness {} \n\
        kurtosis {} \n p {} \n n {}".format(self.mean, self.stdev, self.skew,
                                            self.kurt, self.p, self.n)
