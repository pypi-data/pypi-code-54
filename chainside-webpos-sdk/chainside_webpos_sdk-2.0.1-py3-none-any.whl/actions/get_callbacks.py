"""
Nigiri auto-generated file
"""
from .common import ChainsideAction, ChainsideAuthenticatedAction, ChainsideAuthenticatingAction
from ..objects import *
from ..exceptions import *


class GetCallbacksAction(ChainsideAuthenticatedAction):
    route = '/payment-order/{payment_order_uuid}/callbacks'
    verb = 'GET'
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Api-Version": "v1"
    }
    query_parameters_schema = {}
    route_parameters_schema = {'payment_order_uuid': {
        'rules': ['required'], 'type': 'uuid'}}
    request_body_class = None
    response_body_class = CallbackList
    errors = dict(super(ChainsideAuthenticatedAction, ChainsideAuthenticatedAction).errors, **{
        '0001': ValidationErrorException,
        '3001': NotFoundException,
    })

    @property
    def payment_order_uuid(self):
        return self.route_parameters['payment_order_uuid']

    @payment_order_uuid.setter
    def payment_order_uuid(self, value):
        self.route_parameters['payment_order_uuid'] = value
