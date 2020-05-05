import pandas as pd
import crdatamgt.topic as topic
from crdatamgt.helpers import topic_directories, workbook_load_file, workbook_save
import datetime
import re

def project_load_from_workbooks(workbooks, **kwargs):
    result_wb = workbooks
    project_sheets = []
    formatting = {}
    if kwargs.get('OUTPUT DIRECTORY'):
        output_path = kwargs.get('OUTPUT DIRECTORY')
    else:
        import os
        output_path = os.path.split(kwargs.get('RESULTS DIRECTORY'))[0]
    for result in result_wb:
        result_data = topic.read_topic(result, kwargs.get('FORMULATION DIRECTORY'))
        test = pd.concat(result_data.values(), axis=1, sort=False)
        project_sheets.append(test)
    compiled = pd.concat(project_sheets[::-1], sort=False).set_index('Topic ID').sort_index().reset_index().drop(
        columns=['Test'], errors='ignore')

    formatting['header'] = {
        'bold': True,
        'text_wrap': False,
        'valign': 'top',
        'fg_color': '#D7E4BC',
        'border': 1,
        'font_size': 16}

    # Write the column headers with the defined format.

    project_name = re.search(r'\\(Project .*)\\', kwargs.get('RESULTS DIRECTORY'))[1]
    dt = datetime.datetime.now().strftime("%d_%m_%Y")
    excel_name = f'{project_name}_{dt}'
    workbook_save(excel_name, output_path, compiled, project_name, **formatting)


def project_load(**kwargs):
    if kwargs.get("TOPIC STRUCTURED"):
        topic_name, topic_path = topic_directories(kwargs.get('PROJECT DIRECTORY'))
        workbooks = [topic.load_topic(t_path) for t_path in topic_path]
        project_load_from_workbooks(workbooks, **kwargs)
    if kwargs.get('RESULT STRUCTURED'):
        workbooks = workbook_load_file(kwargs.get('RESULTS DIRECTORY'))
        project_load_from_workbooks(workbooks, **kwargs)
    else:
        # TODO: logging of badly formatted YAML
        pass
