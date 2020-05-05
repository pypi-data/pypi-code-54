import uvicorn

from spell.serving.server import make_app


uvicorn.run(make_app(), http="h11", loop="asyncio")
