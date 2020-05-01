import grpc

class Balancer(object):
    endPoints = []
    pool = []
    
    def __init__(self, endpoints):
        super().__init__()
        self.endPoints = str.split(endpoints,',')
        self.CreatePool(self.endPoints)


    def CreatePool(self, endPoints):
        for ep in endPoints:
            channel = grpc.insecure_channel(ep)
            self.pool.append(channel)
        pass

    '''
    Make it work first..
    '''
    def AvailableChannel(self):
        if (len(self.pool) > 0):
            return self.pool[0]
        
        return None