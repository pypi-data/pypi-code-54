from .SimpleMachines import SimpleMachine

class pulley(SimpleMachine):
    
    def __init__(self, F = None, P = None, movable = 0, fixed = 1):
        """
        a pulley simple machine class that holds basic calculations.
        Pulleys is assummed without weight.
        At least one of P or F is required.
        This is the simples pulley system that assume each movable pulleys
        tied end-to-end.
        
        
        Attributes:
           F (float): representing the force applied to the system in terms of Newton.
           P (float): representing the load that is carries by the system in terms of Newton.
           movable (int): number of movable pulleys. default = 0
           fixed (int): number of fixed pulleys. default = 1
        """
        try:
            self.F = F
            self.P = P
            self.movable = movable
            self.fixed = fixed
            
            if self.F is None:
                self.F = self.calculate_F()
            if self.P is None:
                self.P = self.calculate_P()
          
        except:
            print("One of F or P is required")
          
        SimpleMachine.__init__(self, self.F, self.P)
        
        
    def calculate_F(self):
        """
        This function helps to calculate F.
        
        Attributes:
            None
        
        Output:
            string with the updated F value
        """
        F = self.P / (2 ** self.movable)       
        print("F value is calculated as {:.2f} Newton".format(F))
        return(F)
        
    def calculate_P(self):
        """
        This function helps to calculate P. 
        
        Attributes:
            None
        
        Output:
            string with the updated P               
        """
        P = self.F * (2 ** self.movable)
        print("P value is calculated as {:.2f} Newton".format(P))
        return(P)
              
        
    
    

        
        
        