"""
Nigiri auto-generated file
"""
from .common import ChainsideAction, ChainsideAuthenticatedAction, ChainsideAuthenticatingAction
from ..objects import *
from ..exceptions import *


class PaymentUpdateAction(ChainsideAuthenticatedAction):
    route = '/payment-order/{payment_order_uuid}/test/'
    verb = 'PATCH'
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Api-Version": "v1"
    }
    query_parameters_schema = {}
    route_parameters_schema = {'payment_order_uuid': {
        'rules': ['required'], 'type': 'uuid'}}
    request_body_class = PaymentUpdateObject
    response_body_class = None
    errors = dict(super(ChainsideAuthenticatedAction, ChainsideAuthenticatedAction).errors, **{
        '3001': NotFoundException,
        '0013': InvalidCallbackException,
    })

    @property
    def payment_order_uuid(self):
        return self.route_parameters['payment_order_uuid']

    @payment_order_uuid.setter
    def payment_order_uuid(self, value):
        self.route_parameters['payment_order_uuid'] = value

    @property
    def payment_update_object(self):
        return self.request_body

    @payment_update_object.setter
    def payment_update_object(self, value):
        self.request_body = value
