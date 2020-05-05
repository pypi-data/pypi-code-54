import json
import os
from pathlib import Path
from typing import Callable, Optional

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse, Response
from starlette.routing import Route
import yaml

from spell.serving.exceptions import BadAPIResponse, InvalidServerConfiguration
from spell.serving.api import API
from spell.serving.types import APIResponse


def make_api_route(func: Callable[[Request], APIResponse]) -> Callable[[Request], APIResponse]:
    async def endpoint(request: Request) -> Response:
        return wrap_response(await func(request))

    return endpoint


def wrap_response(response: APIResponse) -> Response:
    if isinstance(response, bytes):
        return Response(content=response, media_type="application/octet-stream")
    elif isinstance(response, str):
        return PlainTextResponse(content=response)
    elif isinstance(response, Response):
        return response
    else:
        try:
            json.dumps(response)
        except Exception as e:
            raise BadAPIResponse(
                "Invalid response. Return an object that is JSON-serializable (including its "
                "nested fields), a bytes object, a string, or a "
                "starlette.response.Response object"
            ) from e
        return JSONResponse(response)


def make_api() -> None:
    config_path = get_path_env_or_raise("SPELL_PREDICTOR_CONFIG", is_file=True)
    predictor_file = get_path_env_or_raise("SPELL_PREDICTOR_FILE", is_required=False, is_file=True)
    if predictor_file:
        classpath = get_env_or_raise("SPELL_PREDICTOR_CLASSPATH", is_required=False)
        api = API.from_file(predictor_file, classname=classpath)
    else:
        predictor_module = get_path_env_or_raise(
            "SPELL_PREDICTOR_MODULE",
            is_dir=True,
            not_found_error="Either SPELL_PREDICTOR_FILE or SPELL_PREDICTOR_MODULE must be provided",
        )
        classpath = get_env_or_raise(
            "SPELL_PREDICTOR_CLASSPATH",
            not_found_error="SPELL_PREDICTOR_CLASSPATH must be provided when using SPELL_PREDICTOR_MODULE",
        )
        api = API.from_module(predictor_module, classpath)
    initialize_predictor(api, config_path)
    return api


def get_path_env_or_raise(
    name: str,
    is_required: bool = True,
    is_file: bool = False,
    is_dir: bool = False,
    not_found_error: Optional[str] = None,
) -> Optional[Path]:
    var = get_env_or_raise(name, is_required=is_required, not_found_error=not_found_error)
    if var is None:
        return var
    var = Path(var)
    if is_file and not var.is_file():
        raise InvalidServerConfiguration(f"{var} used in {name} is not a file")
    elif is_dir and not var.is_dir():
        raise InvalidServerConfiguration(f"{var} used in {name} is not a dir")
    return var


def get_env_or_raise(
    name: str, is_required: bool = True, not_found_error: Optional[str] = None,
) -> Optional[str]:
    var = os.getenv(name)
    if is_required and var is None:
        message = not_found_error or f"{name} environment variable must be provided"
        raise InvalidServerConfiguration(message)
    return var


def initialize_predictor(api: API, config_path: str) -> None:
    try:
        with open(config_path) as f:
            config = yaml.safe_load(f)
        api.initialize_predictor(config)
    except FileNotFoundError as e:
        raise InvalidServerConfiguration(f"Could not find config file at {config_path}") from e


def make_app(api: Optional[API] = None) -> Starlette:
    if not api:
        api = make_api()
    routes = [
        Route("/predict", make_api_route(api.predict), methods=["POST"]),
        Route("/health", make_api_route(api.health), methods=["GET"]),
    ]

    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
            allow_credentials=True,
        ),
        Middleware(GZipMiddleware),
    ]

    return Starlette(
        debug=os.getenv("SPELL_PREDICTOR_DEBUG", False), routes=routes, middleware=middleware,
    )
    # TODO(justin): Use a startup method to set ready check to True
