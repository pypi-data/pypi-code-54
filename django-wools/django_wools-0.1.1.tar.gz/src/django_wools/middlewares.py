from typing import Callable

from django.http import HttpRequest, HttpResponse
from django.utils.timezone import now

ResponseGetter = Callable[[HttpRequest], HttpResponse]


class NowMiddleware:
    """
    This middleware adds a "now()" method to request objects, this way a
    common timestamp is available within the scope of the request. That's
    useful by example for token validity: if a token expires at a given time
    it allows to consider that the request conceptually happens instantly and
    every time you measure the token's validity you do so based on the
    request's global timestamp and not the actual time (which is just
    milliseconds away).
    """

    def __init__(self, get_response: ResponseGetter):
        """
        Storing away
        """

        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """
        Monkey-patching the request object with the custom now() function
        """

        fixed_now = now()
        object.__setattr__(request, "now", lambda: fixed_now)

        return self.get_response(request)
