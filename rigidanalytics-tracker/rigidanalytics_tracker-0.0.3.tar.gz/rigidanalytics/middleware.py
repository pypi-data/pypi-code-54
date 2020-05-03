import time
import re

from django.conf import settings
from urllib.parse import urljoin

from .tracker.django import Tracker
from .utils import is_analytics_sending_disabled


BACKEND_ENDPOINT_BASIS = 'https://rigidanalytics.com'


class Analytics(object):

    def __init__(self, get_response):
        self.get_response = get_response
        self.intercepted_data = {}
        self.init_tracker()

    def init_tracker(self):
        base_url = settings.RIGID_ANALYTICS.get(
            'BACKEND_ENDPOINT', BACKEND_ENDPOINT_BASIS)
        endpoint = urljoin(base_url, settings.RIGID_ANALYTICS['PROJECT_ID'])
        self.tracker = Tracker(endpoint)

    def __call__(self, request):
        if is_analytics_sending_disabled():
            return self.get_response(request)

        start_time = time.time_ns()

        response = self.get_response(request)

        end_time = time.time_ns()
        processing_time = end_time - start_time

        self.tracker.send_analytics_data(
            request, response, start_time, processing_time,
            self.intercepted_data
        )

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        self.intercepted_data['view_name'] = view_func.__name__
