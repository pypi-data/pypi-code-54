from IPython.core.magic import (Magics, magics_class, line_cell_magic)
import logging
import requests
import json
import os
import sys


@magics_class
class PostCell(Magics):

    VERSION = 0.1
    REGISTERED = False

    def find_configfile(self,file_name='postcell.conf'):
        current_dir = os.getcwd()
        parents = len(os.getcwd().split(os.path.sep)) 

        for _ in range(parents):
            file_path = os.path.join(current_dir,file_name)
            if os.path.isfile(file_path): return file_path
            current_dir = os.path.dirname(current_dir)

    def load_config_vals(self, config_file_path=None):
        if config_file_path is None:
            config_file_path = self.find_configfile()

        if config_file_path is None: print("Error: Unable to find config file postcell.conf in current directory or any parent directory")
        else:
            print(f"Loading config file from {config_file_path}")
            with open(config_file_path, 'r') as config_file:
                conf = json.load(config_file)

                for k in ['student_id', 'url', 'class_id', 'instructor_id', 'should_send_to_server']:
                    if k not in conf:
                        print(f"Error: Unable to find value for '{k}' in config file at {config_file_path}", file=sys.stderr)
                
                return (conf['student_id'], conf['url'], conf['class_id'], conf['instructor_id'], conf['should_send_to_server'])


    def register_postcell(self, args):
        """Loads user name and server url

        Parameters:
        args (str): This string should contain just the word 'register' or config file path or user name and url

        """

        params_list = args.strip().split(" ")[1:] # remove the first keyword, which should always be 'register'
        params = dict(zip([a.strip('-') for a in params_list[0::2]], params_list[1::2]))


        if(len(params_list) == 0): # No arguments, find config file and load parameters
            self.student_id, self.url, self.class_id, self.instructor_id, self.should_send_to_server = self.load_config_vals()

        elif('config' in params): # Load config file from specified path
            config_file_path = params['config']
            self.student_id, self.url, self.class_id, self.instructor_id, self.should_send_to_server = self.load_config_vals(config_file_path)
        else: # User name and url are provided in-line
            for k in ['student_id', 'url', 'class_id', 'instructor_id']:
                if k not in params:
                    print(f"Error: Unable to find value for '{k}' in parameters in cell", file=sys.stderr)

            self.student_id     = params['student_id']
            self.url            = params['url']
            self.instructor_id  = params['instructor_id']
            self.class_id       = params['class_id']
            self.should_send_to_server = params.get('should_send_to_server', True)

        self.REGISTERED = True
        print(f"Registered user {self.student_id} at {self.url}")
    
    def send_to_server(self, args, cell):
        exercise = args.strip()

        if not self.REGISTERED:
            print("You are not registered. Please register using `%postcell register` before submitting exercises", file=sys.stderr)
            return
        try:
            data = { #TODO: On server, add a UTC timestamp to this
                'postcell_version': self.VERSION,
                'instructor_id': self.instructor_id,
                'class_id': self.class_id,
                'student_id': self.student_id,
                'exercise_name': exercise,
                'cell_contents': cell
            }

            headers = {'Content-Type': 'application/json'}

            #print(data)

            if self.should_send_to_server:
                resp = requests.post(self.url, data=json.dumps(data), headers=headers)
            else:
                print("Code not posted to server. Property 'should_send_to_server' is false or not provided")

            if(resp.ok): print("Cell posted for evaluation")
            else: print("Server response:"+resp.text, resp, file=sys.stderr)                

        except Exception as inst:
            print("Exception:"+inst, file=sys.stderr)
            logging.error(inst)
        get_ipython().run_cell(cell)  

    def version(self):
        print(str(self.VERSION))      

    @line_cell_magic
    def postcell(self, line, cell=None):
        if(line.startswith("register")):
           self.register_postcell(line)
        elif(line.startswith("version")):
           self.version()
        else:
            self.send_to_server(line, cell)
