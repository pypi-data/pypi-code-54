import requests, json, jsonpickle

class OldClient(object):
    def __init__(self, token):
        self.url = "https://db.neelr.dev/api/%s/" % token
    
    def store(self, data: dict, key=""):
        r = requests.post(self.url + key, data=json.dumps(data))
        return (r.status_code == 201), r.content.decode()
    
    def retrieve(self, key=""):
        r = requests.get(self.url + key)
        if r.status_code == 404:
            return None
        return r.json()
    
    def delete(self, key=""):
        r = requests.delete(self.url + key)
        return r.status_code == 204

class Client(object):
    def __init__(self, token):
        self.url = "https://db.neelr.dev/api/%s/" % token
    
    def store(self, key, data):
        r = requests.post(self.url + key, data={'data':jsonpickle.dumps(data)})
        return (r.status_code == 201), r.content.decode()
    
    def retrieve(self, key):
        r = requests.get(self.url + key)
        if r.status_code == 404:
            return None
        return jsonpickle.loads(r.json()['data'])
    
    def delete(self, key):
        r = requests.delete(self.url + key)
        return r.status_code == 204
    
    def pull(self):
        return {x:jsonpickle.loads(i) for x,i in requests.get(self.url).json()['data'].items()}