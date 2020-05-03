"""
Nigiri auto-generated file
"""
from .api_context import ChainsideApiContext
from .common import AuthenticatedClient
from .actions.factory import ChainsideFactory
from .lib.cache import CacheAdapterFactory
from .lib.constants import CHAINSIDE_API_HOSTNAME, CHAINSIDE_SANDBOX_API_HOSTAME


class Client(AuthenticatedClient):
    def __init__(self, config):

        super().__init__(config)
        self.login()

    def delete_payment_order(self, payment_order_uuid):
        action = self.factory.make('delete_payment_order')
        action.payment_order_uuid = payment_order_uuid
        return action.run()

    def get_payment_order(self, payment_order_uuid):
        action = self.factory.make('get_payment_order')
        action.payment_order_uuid = payment_order_uuid
        return action.run()

    def get_payment_orders(self, page=None, sort_order=None, sort_by=None, status=None, page_size=None):
        action = self.factory.make('get_payment_orders')
        if page:
            action.page = page
        if sort_order:
            action.sort_order = sort_order
        if sort_by:
            action.sort_by = sort_by
        if status:
            action.status = status
        if page_size:
            action.page_size = page_size
        return action.run()

    def create_payment_order(self, payment_order):
        action = self.factory.make('create_payment_order')
        action.payment_order = payment_order
        return action.run()

    def get_callbacks(self, payment_order_uuid):
        action = self.factory.make('get_callbacks')
        action.payment_order_uuid = payment_order_uuid
        return action.run()

    def payment_reset(self, payment_order_uuid):
        action = self.factory.make('payment_reset')
        action.payment_order_uuid = payment_order_uuid
        return action.run()

    def payment_update(self, payment_order_uuid, payment_update_object):
        action = self.factory.make('payment_update')
        action.payment_order_uuid = payment_order_uuid
        action.payment_update_object = payment_update_object
        return action.run()

    def client_credentials_login(self, client_credentials):
        action = self.factory.make('client_credentials_login')
        action.client_credentials = client_credentials
        return action.run()
