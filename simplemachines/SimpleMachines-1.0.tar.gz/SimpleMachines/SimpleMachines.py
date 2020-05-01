class SimpleMachine():
    
    def __init__(self, F, P):
        """
        Generic simple machine class to make basic
        processes. This is a basic class only with one force
        and one load.
        Frictionless is assumed
        
        Attributes:
            F (float) representing the force applied to the system in terms of Newton.
            P (float) representing the load that is carries by the system in terms of Newton.           
        """
        
        self.F = F
        self.P = P
        
    
    def findStrGain(self):
        """
        This function finds the strength gain of the simple machine
        
        Attributes:
            None
            
        Output:
            strength gain (float)        
        """
        return 1.0 * self.P / self.F   
         
    def calculate_load_distance(self, F_x):
        """
        This function calculates distance that load takes
        when the distance that force is applied is given.
        
        Attributes:
            F_x (float) : Distance that force is applied in any unit
            
        Output:
            load distance (float): the distance load has gone
        """
        return F_x / self.findStrGain()
    
    def calculate_force_distance(self, P_x):
        """
        This function calculates distance that force is applied
        when the distance that load has taken is given
        
        Attributes:
            P_x (float) : Distance that load has taken
            
        Output:
            force distance (float): the distance that force is applied
        """
        return P_x * self.findStrGain()
    
    def calculate_energy(self, F_x = None, P_x = None):
        """
        This function calculates the energy that is needed
        to apply force for given distance.
        If force distance is not provided. Energy conservation
        is assumed to move the load for P_x distance
        
        Attributes:
            F_x (float): the distance that force is applied
            P_x (float): the distance that load is moved
            
        Output:
            Energy (float)
        """
        
        try:
            if F_x is None:
                F_x = self.calculate_force_distance(P_x)
        except:
            print("At least one attribute should be provided")
        return self.F * F_x
        
        
    def calculate_power(self, F_x, t):
        """
        This function calculates the power that isi applied
        to the system.
        
        Attributes:
            F_x (float): the distance force is applied
            t (float): the time that passed during force application
            
        Output:
            power (float)
        """
        return self.calculate_energy(F_x) / t
        
        
    def __repr__(self):    
        """
        Function to output the characteristics of the Simple Machines

        Args:
            None

        Returns:
            string: characteristics of the Simple Machines
        """
        return("This machine carries {:.2f} Newton with {:.2f} Newton force. Strength gain: {:.2f}".format(self.P, self.F, self.findStrGain()))
    