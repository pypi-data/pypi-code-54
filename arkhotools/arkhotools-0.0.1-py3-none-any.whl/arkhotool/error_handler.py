import json
import os
import boto3

"""
@Doc
"""
sqs = boto3.resource('sqs')

def register_error(message,attrs,level = 'ERROR'):
	sqs_attr = attrs
	if type(sqs_attr) != 'dict':
		sqs_attr = {'application': 'noname', 'function': 'noname' }	
	else:
		if 'application' not in sqs_attr:
			sqs_attr.update( {'application':  'noname'})
		if 'function' not in sqs_attr:
			sqs_attr.update( {'function': 'noname' })

	sqs_name = os.getenv('SQS_NAME')
	queue = sqs.get_queue_by_name(QueueName=sqs_name)
	response = queue.send_message(MessageBody=str({ 'message': message }),
	    MessageAttributes={
	        'level': {
	            'StringValue': level,
	            'DataType': 'String'
	        },
	        'application':{
	        	'StringValue': sqs_attr['application'],
	        	'DataType': 'String' #
	        },
	        'function': {
	        	'StringValue': sqs_attr['function'],
	        	'DataType': 'String' #
	        }
	    }
	)
