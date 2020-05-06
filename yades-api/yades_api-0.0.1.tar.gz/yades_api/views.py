import json
import uuid

from aiohttp import web

from yades_api import helpers


async def inbox_detail(request):
    mailbox = await request.app['db'].mailboxes.find_one(
        {'token': request.token}
    )
    if not mailbox:
        raise web.HTTPNotFound()

    context = {
        'address': mailbox['address'],
        'emails': mailbox['emails'],
    }
    return web.json_response(context)


async def inbox_create(request):
    db = request.app['db']
    config = request.app['config']
    token = request.token

    if token:
        await helpers.delete_mailbox_by_token(db, request.token)
    else:
        token = str(uuid.uuid4())

    data = await request.json()
    local = data.get('local')
    domain = data.get('domain')

    if not (local and domain):
        raise web.HTTPBadRequest(
            content_type='application/json',
            text=json.dumps({
                'code': 'no-required-fields'
            })
        )
    if domain not in config['allowed_domains']:
        raise web.HTTPBadRequest(
            content_type='application/json',
            text=json.dumps({
                'code': 'domain-not-allowed'
            })
        )
    address = f'{local}@{domain}'
    mailbox = await helpers.get_mailbox_by_address(db, address)
    if mailbox:
        raise web.HTTPBadRequest(
            content_type='application/json',
            text=json.dumps({
                'code': 'already-occupied'
            })
        )

    await helpers.create_mailbox(db, address, token)

    raise web.HTTPOk(
        content_type='application/json',
        text=json.dumps({
            'token': token,
            'address': address,
        })
    )


async def inbox_email_detail(request):
    email_uuid = request.match_info['uuid']
    current_mailbox = await helpers.get_mailbox_by_token(
        request.app['db'], request.token
    )
    email = await helpers.get_email(
        request.app['db'], email_uuid
    )
    if not email or email['to'] != current_mailbox['address']:
        raise web.HTTPNotFound()

    response = {
        'from_name': email['from_name'],
        'from_address': email['from_address'],
        'subject': email['subject'],
        'timestamp': email['timestamp'],
    }

    plain = email['payload'].get('text/plain')
    if plain:
        response.update({'plain': plain})

    html = email['payload'].get('text/html')
    if html:
        response.update({'html': html})

    return web.json_response(response)
