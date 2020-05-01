import kombu
from celery import bootsteps

from celery_rmq.registry import get_queue


class BasicTestConsumer(bootsteps.ConsumerStep):

    def handle_message(self, body, message):
        print(body)
        message.ack()

    def get_consumers(self, channel):
        queue = get_queue("test_queue", "test_routing")
        return [kombu.Consumer(
            channel,
            queues=[queue],
            callbacks=[self.handle_message],
            accept=['json']
        )]
