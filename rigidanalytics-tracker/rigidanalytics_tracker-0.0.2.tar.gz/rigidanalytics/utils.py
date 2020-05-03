from django.conf import settings


def is_analytics_sending_disabled():
    if 'DEBUG_DISABLE_ANALYTICS' in settings.RIGID_ANALYTICS \
            and settings.RIGID_ANALYTICS['DEBUG_DISABLE_ANALYTICS'] is not None:
        return settings.RIGID_ANALYTICS['DEBUG_DISABLE_ANALYTICS']
    else:
        return settings.DEBUG
