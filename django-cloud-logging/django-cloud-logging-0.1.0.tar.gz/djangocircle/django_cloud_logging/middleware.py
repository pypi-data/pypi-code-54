from rest_framework.views import exception_handler
from django.conf import settings
import traceback
import logging

if not hasattr(settings, 'DJANGOCIRCLE_CONFIG') or not "CLOUD_LOGGING_HANDLER" in settings.DJANGOCIRCLE_CONFIG:
    print("Invalid configurtaion - configure the DJANGOCIRCLE_CONFIG.CLOUD_LOGGING_HANDLER in settings.py")
    logger = logging.getLogger()
else:
    logger = logging.getLogger(settings.DJANGOCIRCLE_CONFIG["CLOUD_LOGGING_HANDLER"])

def cloud_logging_exception_handler(exc, context):
    error_response = exception_handler(exc, context)
    logger.error(traceback.format_exc())
    return error_response
