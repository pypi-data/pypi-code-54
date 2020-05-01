import json

def asjson(req, res):
    """ send json """
    res.json.code = res.status
    res.data = json.dumps(res.json)
    res.content_type = 'application/json'
