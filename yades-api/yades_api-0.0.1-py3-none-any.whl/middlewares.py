from aiohttp.web import middleware


@middleware
async def token_middleware(request, handler):
    token = None
    auth = request.headers.get('Authorization', '').split()
    if auth and auth[0] == 'Token':
        token = auth[1]

    request.token = token
    response = await handler(request)
    return response
