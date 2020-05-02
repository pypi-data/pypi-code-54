#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio

import os
import subprocess
import abc

from six import string_types

import anpy.analysis
import anpy.analyzer
import anpy.environment
import anpy.utils

# compatible with Python 2 *and* 3:
ABC = abc.ABCMeta('ABC', (object,), {'__slots__': ()})

MAX_THREADS = 4

ENV = anpy.environment.WagasciEnvironment()
ENV["WAGASCI_LIB"] = ENV['WAGASCI_MAINDIR'] + "/lib"


class Program(object):
    """
    Class to decode a list of runs as an uninterrupted job. The usage scenario is when
    you need to decode multiple runs in one batch and do not want to monitor the chain
    continuously. The decoding should go on even in case of error and print a report at the
    end.
    """

    def __init__(self):
        self._run_dict = {}
        self._save_with_repository = True
        self._save_dict = {}
        self._analyzer_factories = []

        # Enable thread safety
        chain = anpy.analysis.WagasciAnalysis(ENV["WAGASCI_LIB"])
        chain.enable_thread_safety()

    def start(self):
        for analyzer_factory in self._analyzer_factories:
            chains_for_each_run = {}
            for run_name, run_root_dir in sorted(self._run_dict.items()):

                if self._save_with_repository:
                    output_dir = run_root_dir
                else:
                    output_dir = self._save_dict[run_name]

                analyzer = analyzer_factory.get_analyzer(run_root_dir=run_root_dir, run_name=run_name,
                                                         output_dir=output_dir)
                print("Applying %s analyzer on %s" % (analyzer.name, run_name))

                chains_for_each_run[run_name] = {}
                analyzer.spawn(chains_for_each_run[run_name])
                anpy.utils.limit_chains(chains_for_each_run, MAX_THREADS)
            anpy.utils.join_chains(chains_for_each_run)

    def set_run_location(self, run_dict):
        self._run_dict = run_dict

    def get_run_location(self):
        return self._run_dict

    def set_save_location(self, save_dict):
        """
        Set a custom location where to store each run decoded data.
        :param save_dict: Dictionary where the key is the run name and the value is
                          the path of the folder where the decoded data is to be stored
        :rtype: None
        """
        self._save_dict = save_dict
        for run_name in self._run_dict:
            if run_name not in save_dict:
                raise KeyError("The save location dictionary does not contain the run named '%s'" % run_name)
        self._save_with_repository = False

    def _check_dependencies(self, factory):
        if (factory.depends is not None and
                factory.depends not in [factory.name for factory in self._analyzer_factories]):
            raise RuntimeError("{} depends on {} but not found".format(factory.name, factory.depends))
        return factory

    def add_step(self, name, **kwargs):
        analyzer_factory_producer = anpy.analyzer.AnalyzerFactoryProducer()
        factory = analyzer_factory_producer.get_factory(name, **kwargs)
        self._analyzer_factories.append(self._check_dependencies(factory))


class ProgramBuilder(ABC):
    """
    The ProgramBuilder interface specifies methods for creating the different parts of
    a program
    """

    def __init__(self):
        self._program = None

    @property
    @abc.abstractmethod
    def program(self):
        pass

    def add_decoder(self, **kwargs):
        self._program.add_step("decoder", **kwargs)

    def add_spill_number_fixer(self, **kwargs):
        self._program.add_step("spill_number_fixer", **kwargs)

    def add_beam_summary_data(self,
                              bsd_database_location,
                              bsd_repository_location,
                              download_bsd_database_location="/tmp/bsd/bsddb.db",
                              download_bsd_repository_location="/tmp/bsd",
                              t2krun=10,
                              **kwargs):
        if ':' in bsd_database_location:
            if len(bsd_database_location.split(':', 1)) != 2:
                raise ValueError("Invalid database location : %s" % bsd_database_location)
            hostname = bsd_database_location.split(':', 1)[0]
            remote_db_path = bsd_database_location.split(':', 1)[-1]
            local_db_path = download_bsd_database_location
            print("Copying remote database %s into location %s" % (remote_db_path, local_db_path))
            anpy.utils.scp_get(hostname, remote_db_path, local_db_path)
        else:
            local_db_path = bsd_database_location
        if not os.path.exists(local_db_path):
            raise EnvironmentError("Local BSD database not found at %s" % local_db_path)

        if ':' in bsd_repository_location:
            if len(bsd_repository_location.split(':', 1)) != 2:
                raise ValueError("Invalid repository location : %s" % bsd_repository_location)
            remote_repo_path = bsd_repository_location
            local_repo_path = download_bsd_repository_location
            print("Copying remote repository %s into location %s" % (remote_repo_path, local_repo_path))
            rsync = anpy.utils.which("rsync")
            if rsync is None:
                raise RuntimeError("rsync program not found")
            try:
                remote = "{}/t2krun{}/*".format(remote_repo_path, t2krun)
                local = "{}/t2krun{}/".format(local_repo_path, t2krun)
                anpy.utils.mkdir_p(local)
                subprocess.check_output([rsync, "-a", "-essh", remote, local])
            except subprocess.CalledProcessError as exception:
                raise RuntimeError("Error while copying the remote repository %s into the "
                                   "local directory %s : %s" % (remote_repo_path, local_repo_path, str(exception)))
        else:
            local_repo_path = bsd_repository_location
        if not os.path.exists(local_repo_path):
            raise EnvironmentError("Local BSD repository not found at %s" % local_repo_path)

        self._program.add_step("beam_summary_data",
                               bsd_database=local_db_path,
                               bsd_repository=local_repo_path,
                               **kwargs)

    def set_run_dict(self, run_dict):
        self._program.set_run_location(run_dict)

    def get_run_dict(self):
        return self._program.get_run_location()

    def set_save_dict(self, save_location):
        save_dict = {}
        if isinstance(save_location, dict):
            save_dict.update(save_location)
        elif isinstance(save_location, string_types):
            run_dict = self._program.get_run_location()
            for run_name in run_dict:
                save_dict[run_name] = os.path.join(save_location, run_name)
        self._program.set_save_location(save_dict)
