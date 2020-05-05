from collections import defaultdict
import yaml
import os
import argparse
import aithermal
import pandas as pd
import xlsxwriter
import datetime


def main():
    def represent_none(self, _):
        return self.represent_scalar('tag:yaml.org,2002:null', '')

    yaml.add_representer(type(None), represent_none)

    parameters = os.path.join(os.getcwd(), "parameters.yaml")
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', help='root path')

    try:
        with open(parameters, 'r') as stream:
            data_loaded = yaml.safe_load(stream)
            try:
                _run(*decomporess(data_loaded))
            except TypeError as e:
                print("Please double-check your parameters.yaml document'")
                raise e
                os.startfile(os.path.join(os.getcwd(), 'parameters.yaml'))
    except FileNotFoundError as e:
        data_loaded = aithermal.utils.write_yaml()
        with open('parameters.yaml', 'w') as outfile:
            yaml.dump(data_loaded, outfile, default_flow_style=False)
        print("Please fill out the parameter.yaml document")
        raise e
        os.startfile(os.path.join(os.getcwd(), 'parameters.yaml'))


def decomporess(data_loaded):
    wavelenths = data_loaded.get('WAVE LENGTHS')
    gradient = data_loaded.get('GRADIENT')
    rms = data_loaded.get('RMS')
    root = data_loaded.get('PROJECT DIRECTORY')
    isotherms = data_loaded.get('ISOTHERMS')
    baselines = data_loaded.get('BASELINE DIRECTORY')

    methods = [method for method in data_loaded.get('Techniques').keys() if method]
    topics, topic_paths = aithermal.topic_directories(root)
    method_paths = aithermal.method_directories(topic_paths, topics, isotherms, methods)
    return gradient, method_paths, rms, root, wavelenths, isotherms, baselines


def _run(gradient, method_paths, rms, root, wavelengths, isotherms, baseline_path):
    ir_list, ms_list, sta_list, gc_list = aithermal.method_sorting(method_paths)
    calibration = aithermal.calibration_check(root)

    sta_frames = aithermal.load_dsc(sta_list, baseline_path=baseline_path, method='tg')
    ir_frames = aithermal.load_dsc(ir_list, method='ir', rms=False, wavelengths=wavelengths)
    ms_frames = aithermal.load_dsc(ms_list, method='ms', file_type='txt')

    excel_path = os.path.join(root, f"Results_{datetime.date.today()}.xlsx")
    writer = pd.ExcelWriter(excel_path, engine='xlsxwriter')

    aithermal.write_sheets(sta_frames, 'TG', writer)
    aithermal.write_sheets(ir_frames, 'IR', writer)
    aithermal.write_sheets(ms_frames, 'MS', writer)

    writer.save()
    print('hold')



if __name__ == "__main__":
    main()
