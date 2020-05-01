import pyetcd
import etcdgrpc

class EtcdClient(object):
    '''
    The Util which implements KV and txn service
    '''
    def __init__(self, endpoints):
        '''
        The format of endpoints
        IP_1:Port1,IP_2:Port2...
        '''
        super().__init__()
        self.balancerSrv = pyetcd.Balancer(endpoints)
        self.kvSrv = pyetcd.KV(self.balancerSrv)

    def Put(self, key, value):
        """Save a key with a value\n
        When everyting is fine, it would return OK
        """
        if (key != ""):
            return self.kvSrv.Put(key,value)
        
        raise ValueError("Key could not be empty!")

    def Get(self, key):
        if (key != ""):
            return self.kvSrv.Get(key)
            
        raise ValueError("Key could not be empty")
        

    def Del(self, key):
        key = key.strip()
        if (key != ""):
            return self.kvSrv.Del(key)
        
        raise ValueError("Key could not be empty")


