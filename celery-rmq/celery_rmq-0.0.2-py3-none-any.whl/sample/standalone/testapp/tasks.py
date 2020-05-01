from __future__ import absolute_import, unicode_literals

from celery import shared_task

from sample.standalone import app_provider


@shared_task
def generic_producer(message, exchange_name, route_key):
    producer = app_provider.get_producer()
    # print(message)
    producer.publish(message, content_type='application/json', exchange=exchange_name, routing_key=route_key)
