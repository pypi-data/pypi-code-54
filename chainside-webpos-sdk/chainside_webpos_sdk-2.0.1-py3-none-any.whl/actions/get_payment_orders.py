"""
Nigiri auto-generated file
"""
from .common import ChainsideAction, ChainsideAuthenticatedAction, ChainsideAuthenticatingAction
from ..objects import *
from ..exceptions import *


class GetPaymentOrdersAction(ChainsideAuthenticatedAction):
    route = '/payment-order'
    verb = 'GET'
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Api-Version": "v1"
    }
    query_parameters_schema = {'page': {'rules': ['nullable', 'min:0'], 'type': 'integer', 'description': 'Index of the page to be returned (default: 0)'}, 'sort_order': {'rules': ['in:asc,desc', 'nullable'], 'type': 'string', 'description': 'Ordering to be used for the sort (default: desc)'}, 'sort_by': {'rules': ['in:amount,created_at', 'nullable'], 'type': 'string', 'description': 'Field used to sort pages (default: created_at)'}, 'status': {
        'rules': ['in:pending,partial,mempool_unconfirmed,unconfirmed,paid,cancelled,expired,network_dispute,mempool_network_dispute,possible_chargeback,chargeback'], 'type': 'string', 'description': 'Status of the payment orders to retrieve'}, 'page_size': {'rules': ['nullable', 'max:40'], 'type': 'integer', 'description': 'Size of the returned page (default: 20)'}}
    route_parameters_schema = {}
    request_body_class = None
    response_body_class = PaymentOrderList
    errors = dict(super(ChainsideAuthenticatedAction, ChainsideAuthenticatedAction).errors, **{
        '1012': ForbiddenException,
    })

    @property
    def page(self):
        return self.query_parameters['page']

    @page.setter
    def page(self, value):
        self.query_parameters['page'] = value

    @property
    def sort_order(self):
        return self.query_parameters['sort_order']

    @sort_order.setter
    def sort_order(self, value):
        self.query_parameters['sort_order'] = value

    @property
    def sort_by(self):
        return self.query_parameters['sort_by']

    @sort_by.setter
    def sort_by(self, value):
        self.query_parameters['sort_by'] = value

    @property
    def status(self):
        return self.query_parameters['status']

    @status.setter
    def status(self, value):
        self.query_parameters['status'] = value

    @property
    def page_size(self):
        return self.query_parameters['page_size']

    @page_size.setter
    def page_size(self, value):
        self.query_parameters['page_size'] = value
