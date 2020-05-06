# Copyright 2019 WHG (International) Limited. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
import os
import sys
from time import sleep

import yaml

from ccvs_scanning_api_client.api.analysis_api import AnalysisApi
from ccvs_scanning_api_client.api_client import ApiClient
from ccvs_scanning_api_client.configuration import Configuration
from ccvs_scanning_api_client.models.analysis import Analysis


config = Configuration(host=os.environ.get('CCVS_API'))


def analysis(image_name, whitelist_file):
    analysis_api = AnalysisApi(ApiClient(config))
    whitelist = read_whitelist_file(whitelist_file)
    analysis_obj = analysis_api.analysis_create(
        Analysis(image=image_name, whitelist=whitelist)
    )
    x = 0
    print('Analysis: ', analysis_obj.id)  # noqa
    while True:
        analysis_result = analysis_api.analysis_read(analysis_obj.id)
        if analysis_result.result == 'pending':
            msg = 'Analysing image' + '.' * x
            print(msg)  # noqa
            sys.stdout.write('\033[F')
            sys.stdout.write('\033[K')
            x += 1
            sleep(5)
        else:
            sys.stdout.write('\033[K')
            print('Image Analyzed')  # noqa
            break
    return analysis_result


def summary(analysis_result):
    link = f'{config.host}container-scanning/analysis/{analysis_result.id}'
    resume = {
        'image': analysis_result.image,
        'link': link,
        'result': analysis_result.result,
        'errors': analysis_result.errors,
        'whitelist': analysis_result.whitelist,
        'total_vulns': {
            'high_vulns': 0,
            'medium_vulns': 0,
            'critical_vulns': 0,
            'low_vulns': 0,
            'unknown_vulns': 0,
            'negligible_vulns': 0
        }
    }

    vulns = analysis_result.ccvs_results
    if vulns:
        for vuln in vulns.values():
            if vuln:
                for level in vuln.items():
                    resume['total_vulns'][level[0]] += len(level[1])

    return resume


def read_whitelist_file(whitelist_file):

    if not whitelist_file:
        return {}

    print('Reading whitelist file')  # noqa
    with open(whitelist_file, 'r') as stream:
        try:
            data_loaded = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print('Error reading whitelist file. Error: %s', exc)  # noqa
            return {}
        else:
            return data_loaded
