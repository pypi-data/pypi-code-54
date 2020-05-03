import requests, json, jsonpickle

def generate(base="https://jsonbin.marcusweinberger.repl.co"):
    return requests.get(base).content.decode()

class SimpleClient(object):
    def __init__(self, base="https://jsonbin.marcusweinberger.repl.co"):
        self.base = base
    
    def generate(self):
        return requests.get(self.base).content.decode()
    
    def store(self, token, key, data):
        r = requests.post(self.base + f"/{token}/{key}", data=json.dumps(data))
        return r
    def retrieve(self, token, key):
        r = requests.get(self.base + f"/{token}/{key}")
        return r
    def delete(self, token, key):
        r = requests.delete(self.base + f"/{token}/{key}")
        return r

class Client(object):
    def __init__(self, token, base="https://jsonbin.marcusweinberger.repl.co"):
        self.base = base
        self.token = token
    
    def url(self, key=""):
        return "%s/%s/%s" % (self.base, self.token, key)
    def generate(self):
        return requests.get(self.base).content.decode()
    def res(self, r):
        try:
            return r.json()
        except:
            return r.content.decode()
    
    def store(self, key, data):
        r = requests.post(self.url(key), data=jsonpickle.dumps(data))
        return self.res(r)
    
    def retrieve(self, key):
        r = requests.get(self.url(key))
        try:
            return jsonpickle.loads(r.content.decode())
        except:
            return self.res(r)
    
    def delete(self, key):
        r = requests.delete(self.url(key))
        return self.res(r)