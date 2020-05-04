import requests, jsonpickle

def generate(base="https://db.marcusweinberger.repl.co"):
    return requests.get(base + "/generate").json()

def register(token, base="https://db.marcusweinberger.repl.co"):
    return requests.post(base+"/register", data={'token':token}).json()

class Client(object):
    def __init__(self, token, base="https://db.marcusweinberger.repl.co"):
        self.base = base
        self.token = token
    
    def _res(self, r):
        try:
            return jsonpickle.loads(r.json())
        except:
            try:
                return r.json()
            except:
                return r.content.decode()
    
    def store(self, key, data):
        r = requests.post(self.base + "/store", data={
            'token': self.token,
            'key': key,
            'data': jsonpickle.dumps(data),
        })
        return self._res(r)
    
    def retrieve(self, key):
        return self._res(requests.get('/'.join([self.base, self.token, key])))
    
    def delete(self, key):
        r = requests.post(self.base + "/delete", data={
            'token': self.token,
            'key': key,
        })
        return self._res(r)
    
    def unregister(self, conf=False):
        if conf:
            return self._res(requests.get(self.base + "/unregister/" + self.token))