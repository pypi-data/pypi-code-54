def build_request(host, path, method='GET', headers=None, body=None):
    if headers is None:
        headers = {}

    headers['Host'] = host
    string = f'{method} /{path} HTTP/1.1\r\n'
    string += '\r\n'.join(f'{k}: {v}' for k, v in headers.items())
    string += '\r\n\r\n'

    if body is not None:
        string += body
        if 'content-length' not in headers:
            headers['content-length'] = len(body)

    return string.encode('utf-8')
