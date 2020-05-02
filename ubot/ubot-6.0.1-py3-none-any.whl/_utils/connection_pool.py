import asyncio

from .http11 import build_request


class TCP(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def connection_lost(self, exc):
        # the transport is already close when we get here
        if exc:
            self.future.set_exception(exc)

    def data_received(self, data):
        # since:
        # 1) http parsing in python is _extremely_ inefficient compared to more modern solutions
        # 2) making the assumption that all the data will fit in a single socket.read and there will not be chunks both
        # speeds up and simplifies this code a lot
        # 3) we can safely make that assumption in the context of the Telegram bot API
        # this code doesn't (shouln't) need to be longer than this:
        self.future.set_result(data)

    def eof_received(self):
        # falsy -> the transport closes itself
        # truthy -> the protocol determines whether to close the transport
        # SSL doesn't support half-closed streams so here we go
        return False

    def write(self, data, future):
        self.future = future
        self.transport.write(data)


class HttpConnectionPool:
    def __init__(self, url, *, loop=None, size=5):
        self.url = url

        if loop is None:
            self.loop = asyncio.get_event_loop()
        else:
            self.loop = loop

        self.queue = asyncio.Queue(loop=loop)

        for _ in range(size):
            loop.create_task(self.open())

    async def open(self):
        transport = None

        while True:
            (future, req) = await self.queue.get()
            if transport is None:
                (transport, protocol) = await self.loop.create_connection(lambda: TCP(), self.url, 443, ssl=True)

            protocol.write(req, future)
            await future
            if self.queue.empty():
                transport.close()
                transport = None

    def request(self, path, method, headers, body):
        req = build_request(self.url, path, method, headers, body)
        future = self.loop.create_future()
        self.queue.put_nowait((future, req))
        return future
