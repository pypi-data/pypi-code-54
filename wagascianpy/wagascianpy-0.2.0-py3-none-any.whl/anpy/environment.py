""" Set the environment variables for the WAGASCI analysis software """

# !/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Copyright 2019 Pintaudi Giorgio

# pylint: disable-msg=too-many-arguments

import shlex
import subprocess
import pprint
import os

WAGASCI_ENVIRONMENT_SCRIPT = "/opt/calicoes/config/wagasci_environment.sh"


class WagasciEnvironment(dict):
    """ Class to manage WAGASCI environment variables """

    def __init__(self, path=None):
        super(WagasciEnvironment, self).__init__()
        self._environment = dict()
        if path is None:
            environment_script_path = WAGASCI_ENVIRONMENT_SCRIPT
        else:
            environment_script_path = path
        if os.path.exists(environment_script_path):
            command = shlex.split("env -i bash -c 'source %s && env'" % environment_script_path)
            proc = subprocess.Popen(command, stdout=subprocess.PIPE)
            for line in proc.stdout:
                (key, _, value) = line.partition("=")
                try:
                    self.__setitem__(key, value.strip('\n'))
                except Exception as error:
                    print(("Failed add variable (" + str(key) + " = " + str(value) +
                           ") to the environment : " + str(error)))
            proc.communicate()
            try:
                self.__delitem__('_')
            except Exception as error:
                print("Failed to delete '_' : " + str(error))
        else:
            print("Environment script not found : {}".format(environment_script_path))
            print("Trying to get the environment from the shell")
            for variable_name, variable_value in os.environ.items():
                if variable_name.startswith("WAGASCI"):
                    self._environment[variable_name] = variable_value

    def print_env(self):
        """ Set WAGASCI environment variables """
        pprint.pprint(self._environment)

    def __getitem__(self, key):
        return self._environment[self.__keytransform__(key)]

    def __setitem__(self, key, value):
        self._environment[self.__keytransform__(key)] = value

    def __delitem__(self, key):
        del self._environment[self.__keytransform__(key)]

    def __iter__(self):
        return iter(self._environment)

    def __len__(self):
        return len(self._environment)

    @staticmethod
    def __keytransform__(key):
        return key
