import crdatamgt
import yaml
import os

def main():
    def represent_none(self, _):
        return self.represent_scalar('tag:yaml.org,2002:null', '')

    yaml.add_representer(type(None), represent_none)

    try:
        with open("parameters.yaml", 'r') as stream:
            data_loaded = yaml.safe_load(stream)
            try:
                crdatamgt.project.project_load(**data_loaded)
            except TypeError:
                raise
                print("Please double-check your parameters.yaml document'")
                os.startfile(os.path.join(os.getcwd(), 'parameters.yaml'))
    except FileNotFoundError:
        data_loaded = crdatamgt.helpers.write_yaml()
        with open('parameters.yaml', 'w') as outfile:
            yaml.dump(data_loaded, outfile, default_flow_style=False)
        print("Please fill out the parameter.yaml document")
        os.startfile(os.path.join(os.getcwd(), 'parameters.yaml'))


if __name__ == "__main__":
    main()
