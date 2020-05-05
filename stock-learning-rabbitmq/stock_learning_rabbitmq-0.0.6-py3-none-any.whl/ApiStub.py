from stock_learning_rabbitmq.QueueNameConstants import API_QUEUE_NAME
from stock_learning_rabbitmq.Stub import Stub


class ApiStub(Stub):
    
    def __init__(self, server):
        super().__init__(server, API_QUEUE_NAME)

    def hello_world(self, content):
        self._send('hello-world', content)

    def persist_infomoney_ibovespa_historic_data(self, content):
        self._send('persist-infomoney-ibovespa-historic-data', content)
