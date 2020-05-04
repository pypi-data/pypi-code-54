import json
from aiohttp import web
import aiohttp_cors
import aiohttp_swagger
from typing import Callable, Any, List


def validate_required_params(_fun=None, *, names):
    """Validate that a query has all required parameters.

    Role of this decorator is to force returning a `web.HTTPForbidden`
    with an explicit message when one of required query parameters
    is missing.

    This will call the wrapped function with a dict containing
    all required parameters values.

    :param names: list of required parameters
    :return: result of wrapped function or `web.HTTPForbidden`
    """

    def wrapper(fun):
        async def run(self: web.View, *args, **kwargs):
            # Note that `self` is a `web.View` object.
            query = self.request.rel_url.query
            # Decode POST parameters
            if self.request.body_exists and self.request.content_type.endswith("json"):
                data = await self.request.json()
            else:
                data = {}
            # Check and get all parameters
            vals = {}
            for name in names:
                val = data.get(name, None) or query.get(name, None)
                if not val:
                    raise web.HTTPForbidden(
                        reason="{} parameter is required".format(name)
                    )
                vals[name] = val
            # Forward parameters to wrapped functions
            return await fun(self, *args, required_params=vals, **kwargs)

        return run

    return wrapper if not _fun else wrapper(_fun)


def KanjiView(*, db) -> web.View:
    class Wrapper(web.View, aiohttp_cors.CorsViewMixin):
        async def get(self):
            """
            ---
            description: This end-point allow to test that service is up.
            tags:
            - Health check
            produces:
            - text/plain
            responses:
                "200":
                    description: successful operation. Return "pong" text
                "405":
                    description: invalid HTTP Method
            """
            kanji = self.request.match_info["kanji"]
            data = db.get(kanji, None)
            if not data:
                return web.Response(text=json.dumps({"result": "Ko"}))

            data["kanji"] = kanji
            return web.Response(
                text=json.dumps({"result": "Ok", "params": data}, ensure_ascii=False)
            )

        async def post(self):
            text = await self.request.text()
            query = json.loads(text, encoding="utf8")
            kanjis = set(query["kanji"])

            data = {}
            for _ in kanjis:
                if _ in db:
                    data[_] = db[_]

            return web.Response(
                text=json.dumps({"result": "Ok", "params": data}, ensure_ascii=False)
            )

    return Wrapper


class Application(web.Application):
    def __init__(self, *args, db, base_url: str = None, **kwargs):
        super(Application, self).__init__(*args, **kwargs)

        base_url = base_url or ""
        cors = aiohttp_cors.setup(
            self,
            defaults={
                "*": aiohttp_cors.ResourceOptions(
                    allow_credentials=True, expose_headers="*", allow_headers="*",
                )
            },
        )
        cors.add(self.router.add_view(base_url + "/kanji/{kanji}", KanjiView(db=db)))
        cors.add(self.router.add_view(base_url + "/kanji", KanjiView(db=db)))

        aiohttp_swagger.setup_swagger(self)
