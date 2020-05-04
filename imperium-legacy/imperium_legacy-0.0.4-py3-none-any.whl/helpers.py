from datetime import datetime, timedelta
import re


def exists(key, subject):
    split = key.split('.')
    for i, value in enumerate(split):
        if i == 0 and value == '$subject' or value == 'subject':
            continue

        if value not in subject:
            return False
        
        subject = subject[value]
    
    return True


def matches(expr, subject, flag=None):
    if flag is not None:
        flag = flag.lower()
        if flag == 'i':
            result = re.match(expr, subject, re.IGNORECASE)
        elif flag == 'm':
            result = re.match(expr, subject, re.MULTILINE)
        else:
            result = re.match(expr, subject)
    else:
        result = re.match(expr, subject)

    if result:
        return True
    else:
        return False


def date(string=None, date_format='%Y-%m-%d'):
    if string is not None:
        return datetime.strptime(string, date_format)

    return datetime.now()


def date_modify(date_obj, operation, value_type, value):
    operation = operation.lower()
    if operation == 'subtract' or operation == '-':
        if value_type == 'days' or value_type == 'day':
            return date_obj - timedelta(days=int(value))
        if value_type == 'months' or value_type == 'month':
            return date_obj - timedelta(days=int(value) * 30)
        if value_type == 'years' or value_type == 'year':
            return date_obj - timedelta(days=int(value) * 365)

    if operation == 'add' or operation == '+':
        if value_type == 'days' or value_type == 'day':
            return date_obj + timedelta(days=int(value))
        if value_type == 'months' or value_type == 'month':
            return date_obj + timedelta(days=int(value) * 30)
        if value_type == 'years' or value_type == 'year':
            return date_obj + timedelta(days=int(value) * 365)

    return date_obj


def get_value_xml(key: str, subject, raw=True):
    try:
        key_tag = subject.find(key)
        if key_tag is None:
            return None

        if raw:
            return key_tag.text
        else:
            return key_tag
    except:
        # TODO: Maybe log something ?
        return None


def get_attr_xml(key: str, subject):
    try:
        if key not in subject.attrib:
            return None

        return subject.attrib[key]
    except:
        # TODO: Maybe log something ?
        pass
