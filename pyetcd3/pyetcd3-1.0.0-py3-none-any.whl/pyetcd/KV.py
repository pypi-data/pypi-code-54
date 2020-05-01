import etcdgrpc

class KV(object):
    NO_AVAILABLE_CHANNEL = "No channels availabel. Please check your cluster or your arguments..."
    def __init__(self, balancer):
        super().__init__()
        self._balancer = balancer

    def Put(self, key, value):
        channel = self._balancer.AvailableChannel()

        if (channel == None):
            return self.NO_AVAILABLE_CHANNEL

        stub = etcdgrpc.KVStub(channel)
        req = etcdgrpc.PutRequest()
        req.key = key.encode('utf-8')
        req.value = value.encode('utf-8')
        response  = stub.Put(req)
        return "OK"

    def Get(self, key):
        channel = self._balancer.AvailableChannel()

        if (channel == None):
            return self.NO_AVAILABLE_CHANNEL

        stub = etcdgrpc.KVStub(channel)
        rr = etcdgrpc.RangeRequest()
        rr.key = key.encode('utf-8')
        rrr = stub.Range(rr)
        return rrr.kvs[0].value.decode('utf-8')

    def Del(self, key):
        channel = self._balancer.AvailableChannel()

        if (channel == None):
            return self.NO_AVAILABLE_CHANNEL
        
        stub = etcdgrpc.KVStub(channel)
        drr = etcdgrpc.DeleteRangeRequest()
        drr.key = key.encode('utf-8')
        response = stub.DeleteRange(drr)
        return response.deleted == 1
