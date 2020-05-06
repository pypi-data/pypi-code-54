import asyncio
import argparse
import logging

from aiohttp.web import run_app
from environs import Env
from motor.motor_asyncio import AsyncIOMotorClient

from yades_api.app import create_app


async def close_db(app):
    app['db'].client.close()


def main():
    env = Env()
    env.read_env()

    with env.prefixed('YADES_'):
        parser = argparse.ArgumentParser(description="")
        parser.add_argument(
            '--host', type=str,
            default=env('API_HOST', 'localhost'),
            help='Host to listen on'
        )
        parser.add_argument(
            '--port', type=int,
            default=env.int('API_PORT', 8080),
            help='Port to listen on'
        )
        parser.add_argument(
            '--db-uri', type=str,
            default=env.str('MONGODB_URI', 'mongodb://localhost:27017'),
            help='Uri of mongodb server'
        )
        parser.add_argument(
            '--db-name', type=str,
            default=env.str('MONGODB_NAME', 'yades'),
            help='Name of mongodb database'
        )
        parser.add_argument(
            '--allowed-domains', nargs='+',
            default=env.list('ALLOWED_DOMAINS', []),
            help='Domains that can be used for receiving emails'
        )
    args = parser.parse_args()

    config = {
        'mongodb_uri': args.db_uri,
        'mongodb_name': args.db_name,
        'api_host': args.host,
        'api_port': args.port,
        'allowed_domains': args.allowed_domains,
    }

    logging.basicConfig(level=logging.DEBUG)

    if not config['allowed_domains']:
        raise Exception('No allowed domains specified')

    loop = asyncio.get_event_loop()

    db = AsyncIOMotorClient(
        config['mongodb_uri'],
        io_loop=loop
    )[config['mongodb_name']]

    app = create_app(loop, config, db)
    app.on_cleanup.append(close_db)

    run_app(app, host=config['api_host'], port=config['api_port'])


if __name__ == '__main__':
    main()
