def add(req, res):
    if hasattr(req.apex, 'cors'):
        if hasattr(req.apex.cors, 'allow'):
            if hasattr(req.apex.cors.allow, 'origin'):
                origin = req.apex.cors.allow.origin
                res.headers.add('Access-Control-Allow-Origin', origin)
            if hasattr(req.apex.cors.allow, 'methods'):
                res.headers.add('Access-Control-Allow-Methods: %s' % ', '.join(req.apex.cors.allow.methods))