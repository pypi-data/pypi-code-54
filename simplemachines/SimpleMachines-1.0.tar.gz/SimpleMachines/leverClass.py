from SimpleMachines import SimpleMachine

class lever(SimpleMachine):
    
    def __init__(self, F = None, P = None, F_length = None, P_length = None):
        """
        a lever simple machine class that holds basic calculations.
        The lever is assummed without weight.
        The lever can be created with 3 of 4 attributes. Otherwise an
        error occurs
        
        Attributes:
           F (float): representing the force applied to the system in terms of Newton.
           P (float): representing the load that is carries by the system in terms of Newton.
           F_length (float): distance of force from the fulcrum
           P (float): distance of load from the fulcrum
        """
        try:
            self.F = F
            self.P = P
            self.F_length = F_length
            self.P_length = P_length
            
            if F is None:
                F = self.calculate_F()
            if P is None:
                P = self.calculate_P()
            if F_length is None:
                self.F_length = self.calculate_Flength()
            if P_length is None:
                self.P_length = self.calculate_Plength()
        except:
            print("At least 3 value is required to create a lever")
          
        SimpleMachine.__init__(self, F, P)
        
        
    def calculate_F(self):
        """
        This function helps to calculate F. Other 3 variables
        of the lever class must exist.
        
        Attributes:
            None
        
        Output:
            string with the updated F value
        """
        F = self.P * self.P_length / self.F_length
        print("F value is calculated as {:.2f} Newton".format(F))
        return(F)
        
    def calculate_P(self):
        """
        This function helps to calculate P. Other 3 variables
        of the lever class must exist.
        
        Attributes:
            None
        
        Output:
            string with the updated P value
        """
        P = self.F * self.F_length / self.P_length
        print("P value is calculated as {:.2f} Newton".format(P))
        return(P)
       
    def calculate_Flength(self):
        """
        This function helps to calculate F length. Other 3 variables
        of the lever class must exist.
        
        Attributes:
            None
        
        Output:
            string with the updated F_length value
        """
        F_length = self.P * self.P_length / self.F
        print("Force arm value is calculated as {:.2f} units".format(F_length))
        return(F_length)
       
    def calculate_Plength(self):
        """
        This function helps to calculate P length. Other 3 variables
        of the lever class must exist.
        
        Attributes:
            None
        
        Output:
            string with the updated P_length value
        """
        P_length = self.F * self.F_length / self.P
        print("Load arm value is calculated as {:.2f} units".format(P_length))
        return(P_length) 
            
    
    def update_Flength(self, F_length):
        """
        This function helps to update distance of F to the fulcrum.
        Other 3 variables of the lever class must exist.
        
        Attributes:
            F_length: new value of force arm
        
        Output:
            None
        """
        self.F_length = F_length
        self.F = self.calculate_F()
       
    def update_Plength(self, P_length):
        """
        This function helps to update distance of load to the fulcrum.
        Other 3 variables of the lever class must exist.
        
        Attributes:
            P_length: new value of load arm
        
        Output:
            None
        """
        self.P_length = P_length
        self.P = self.calculate_P()
        
        
        
        