__app_settings__ = None


def get_app_settings(env_folder=None, refresh=False):
    import os
    import json
    from stratus_api.core.common import generate_random_id
    import logging

    global __app_settings__
    folder = os.getenv('ENV_FOLDER', '/apps/settings/')
    if env_folder is not None:
        folder = env_folder
    if __app_settings__ is None or refresh:
        app_settings = dict()

        for root, dirs, files in os.walk(folder, topdown=True):
            dirs.sort()
            for file in files:
                local_path = os.path.join(folder, '{0}/{1}'.format(root, file))
                try:
                    with open(local_path, 'rt') as f:
                        app_settings.update(json.load(f))
                except json.JSONDecodeError as e:
                    logging.error(local_path)
                    raise e
        prefix = ''
        if app_settings.get('environment', 'test') == 'test':
            prefix = generate_random_id().split('-')[0]
        app_settings['prefix'] = prefix
        __app_settings__ = {
            k: format_setting_value(v) for k, v in app_settings.items()
        }

    return __app_settings__


def format_setting_value(value):
    import json
    import logging
    formatted_value = value
    if any([i in value for i in ['"', '[', '{']]):
        try:
            formatted_value = json.loads(value)
        except json.JSONDecodeError as exc:
            logging.debug(exc)
    return formatted_value
