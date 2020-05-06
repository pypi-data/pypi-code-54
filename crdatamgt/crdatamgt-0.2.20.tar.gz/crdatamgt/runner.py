import crdatamgt
import yaml
import os
import simplelogging


def main(log):



    def represent_none(self, _):
        return self.represent_scalar('tag:yaml.org,2002:null', '')

    yaml.add_representer(type(None), represent_none)

    try:
        with open("parameters.yaml", 'r') as stream:
            try:
                data_loaded = yaml.safe_load(stream)
                crdatamgt.project.project_load(**data_loaded)
            except Exception as e:
                log.exception(e)
                print("Please double-check your parameters.yaml document'")
                #os.startfile(os.path.join(os.getcwd(), 'parameters.yaml'))

    except FileNotFoundError as e:
        log.exception(e)
        data_loaded = crdatamgt.helpers.write_yaml()
        with open('parameters.yaml', 'w') as outfile:
            yaml.dump(data_loaded, outfile, default_flow_style=False)
        print("Please fill out the parameter.yaml document")
        #os.startfile(os.path.join(os.getcwd(), 'parameters.yaml'))



if __name__ == "__main__":
    cwd = os.getcwd()
    log = simplelogging.get_logger(file_name=os.path.join(cwd, 'cr.log'), console=False)
    try:
        main(log)
    except Exception as e:
        log.exception(e)

