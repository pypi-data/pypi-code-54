import inspect
import typing

import requests
from attr import asdict, validate

from pyquire.credentials import Credentials
from pyquire.models.common import QUIRE_API_URL, StatusCodes


def ptp(data: typing.AnyStr) -> typing.AnyStr:
    if data in ("global",):
        return "global_"

    return str(data).replace("_", "")


class api:
    @staticmethod
    def request(cls, method, *args, **kwargs):
        url = QUIRE_API_URL + getattr(args[0], "__api_path") + getattr(cls, "__api_path").format(**kwargs)
        data = kwargs.get("data", None)
        params = kwargs.get("params", None)
        returns = inspect.signature(cls).return_annotation
        credentials = Credentials.instance()
        requests_kw = {}

        if data:
            validate(data)
            data = {ptp(key): val for key, val in asdict(data, filter=lambda attr, value: value is not None).items()}
        elif params:
            validate(params)
            params = {ptp(key): val for key, val in
                      asdict(params, filter=lambda attr, value: value is not None).items()}

        if method.upper() == "GET":
            if data:
                requests_kw["data"] = data
            elif params:
                requests_kw["params"] = params

        elif method.upper() in ("POST", "PUT"):
            requests_kw["json"] = data or {}

        response = requests.request(
            method=method,
            url=url,
            headers={
                "Authorization": f"Bearer {credentials.access_token}"
            },
            **requests_kw
        )
        try:
            response.reason = StatusCodes.get_desc(response.status_code, response.reason)
            response.raise_for_status()
        except requests.HTTPError as e:
            if response.status_code == StatusCodes.UNAUTHORIZED:
                credentials.refresh_token()
                return api.request(cls, method, *args, **kwargs)
            else:
                raise e

        if type(returns) is typing._GenericAlias:
            returns = typing.get_args(returns)[0]

            return [returns(**{ptp(key): val for key, val in rtn.items()}) for rtn in response.json()]
        elif returns != inspect._empty and returns != typing.NoReturn:
            response = returns(**{ptp(key): val for key, val in response.json().items()})
        else:
            response = None

        return response

    @staticmethod
    def get(cls):
        def func_wrapper(*args, **kwargs):
            return api.request(cls, "GET", *args, **kwargs)

        return func_wrapper

    @staticmethod
    def delete(cls):
        def func_wrapper(*args, **kwargs):
            return api.request(cls, "DELETE", *args, **kwargs)

        return func_wrapper

    @staticmethod
    def put(cls):
        def func_wrapper(*args, **kwargs):
            return api.request(cls, "PUT", *args, **kwargs)

        return func_wrapper

    @staticmethod
    def post(cls):
        def func_wrapper(*args, **kwargs):
            return api.request(cls, "POST", *args, **kwargs)

        return func_wrapper

    @staticmethod
    def path(path):
        def decorator(cls):
            setattr(cls, "__api_path", path)
            return cls

        return decorator
