from csv import DictReader
from datetime import datetime

def main_assignment_from_row(item):
    DATE_FORMAT = '%Y-%m-%d'
    required_fields = ['date','Item','email_task','Lesson']
    for field in required_fields:
        if not field in item:
            raise Exception("Required field %s missing in row!" % field)
        if str(item[field]).strip() == "":
            raise Exception("Required field %s is empty!" % field)
    return {
        'dt_assignment': datetime.strptime(item['date'], DATE_FORMAT),
        'name': item['Name'],
        'task_name': item['Item'],
        'email_task': item['email_task'],
        'assistant': item['Assistant'],
        'lesson': item['Lesson']
    }

def assistant_from_row(item):
    DATE_FORMAT = '%Y-%m-%d'
    return {
        'name': item['Name'],
        'task_name': item['Item'],
        'dt_assignment': datetime.strptime(item['date'], DATE_FORMAT),
        'assistant': item['Assistant'],
        'email_assistant': item['email_assist'],
    }

def check_quality(filename):
    print("checking Quality")
    with open(filename, encoding='utf8') as f:
        reader = DictReader(f)
        for item in reader:
            main_assignment_from_row(item)


def main_assignment_from_csv(filename):
    with open(filename, encoding='utf8') as f:
        reader = DictReader(f)
        return [main_assignment_from_row(item) for item in reader]

def assistant_from_csv(filename):
    with open(filename, encoding='utf8') as f:
        reader = DictReader(f)
        only_non_empty_assistants = filter(lambda item: item['Assistant'] != '', reader)
        return [assistant_from_row(item) for item in only_non_empty_assistants]
