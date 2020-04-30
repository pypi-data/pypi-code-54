import shutil
import pathlib
import nodeenv
import argparse
import subprocess

NPMWORKON_HOME=".npmvirtualenvs"

class NpmWorkon:

    def __init__(self):
        self.root = pathlib.Path().home() / NPMWORKON_HOME
        if not self.root.is_dir():
            self.root.mkdir()

    def build_parser(self):

        parser = argparse.ArgumentParser()
        parser.add_argument('environment', type=str, nargs='?', help="Environment to create")
        parser.add_argument('--node', type=str, help='Specify version of node to install')
        parser.add_argument('--rm', type=str, help="Remove environment")
        
        self.args = parser.parse_args()

    def no_argument(self):
        if len(vars(self.args)) <= 0:
            return True
        return False

    def show_environment(self):
        for npm_environment in self.root.glob('*'):
            if npm_environment.is_dir():
                print(npm_environment.stem)

    def create_environment(self, environment):
        path = self.root / environment

        if not path.exists():
            cmd = f"nodeenv {path}"
            result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        cmd = f"source { path / 'bin' / 'activate' }" # TODO: Not sure how to solve this :(

        import sys
        sys.stdout.write(cmd)
        
    def remove_environment(self, environment):
        shutil.rmtree( self.root / environment )

    def run(self):
        self.build_parser()

        if (name := self.args.environment):
            self.create_environment(name)
        elif (name := self.args.rm):
            self.remove_environment(name)
        else:
            self.show_environment()

npmworkon = NpmWorkon()

def main():
    npmworkon.run()

if __name__ == "__main__":
    main()
