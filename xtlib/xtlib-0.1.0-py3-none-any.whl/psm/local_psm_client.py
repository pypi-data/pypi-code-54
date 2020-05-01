#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# local_psm_client.py: talk to Pool State Mgr running on local machine
import os
import time
import uuid
import psutil
import shutil

from xtlib import utils
from xtlib import pc_utils
from xtlib import constants
from xtlib import file_utils
from xtlib import process_utils
from xtlib.helpers.xt_config import get_merged_config

CONTROLLER_NAME_PATTERN = "xtlib.controller"
PY_RUN_CONTROLLER ="__run_controller__.py"

class LocalPsmClient():
    def __init__(self):
        self.box_is_windows = pc_utils.is_windows()
        self.psm_queue_path = os.path.expanduser(constants.PSM_QUEUE)
        self.psm_log_path = os.path.expanduser(constants.PSM_LOGDIR)
        self.cwd_path = os.path.expanduser(constants.CWD)

        # ensure our required dirs have been created
        if not os.path.exists(self.cwd_path):
            os.makedirs(self.cwd_path)

        if not os.path.exists(self.psm_queue_path):
            os.makedirs(self.psm_queue_path)

    def enqueue(self, team, job, node, fn_zip):
        # copy file to box (with unique name)
        #guid = str(uuid.uuid4())
        ticks = time.time()

        # copy SCRIPT
        fn_entry = "{}.{}.{}.{}.zip".format(team, job, node, int(10*ticks))
        fn_dest = os.path.join(self.psm_queue_path, fn_entry)
        shutil.copyfile(fn_zip, fn_dest)

        return fn_entry

    def dequeue(self, fn_entry):
        # delete file
        fn_dest = os.path.join(self.psm_queue_path, fn_entry)

        if os.path.exists(fn_dest):
            os.remove(fn_dest)

    def enum_queue(self):
        # list contents of queue
        entries = os.listdir(self.psm_queue_path)
        
        # get current entry being processed by controller
        current = self.get_running_entry_name()
        if not self._get_controller_process():
            current = None
        
        return entries, current

    def _is_psm_running(self):
        processes = psutil.process_iter()
        psm_count = 0

        for p in processes:
            try:
                if p.name().lower().startswith("python"):
                    #print("process name: {}".format(p.name()))
                    cmd_line = " ".join(p.cmdline())

                    if constants.PSM in cmd_line:
                        psm_count += 1

            except BaseException as ex:
                pass
            
        return psm_count > 0

    def _get_controller_process(self):
        processes = psutil.process_iter()
        controller_process = None

        for p in processes:
            try:
                if p.name().lower().startswith("python"):
                    #print("process name: {}".format(p.name()))
                    cmd_line = " ".join(p.cmdline())

                    if CONTROLLER_NAME_PATTERN in cmd_line or PY_RUN_CONTROLLER in cmd_line:
                        controller_process = p
                        break

            except BaseException as ex:
                pass
            
        return controller_process

    def start_psm_if_needed(self):
        running = self._is_psm_running()
        #print("PSM running=", running)

        if not running:
            # always copy psm.py (for xt dev/debug purposes)
            fn_src = os.path.join(file_utils.get_my_file_dir(__file__), constants.PSM)
            fn_dest = os.path.join(self.cwd_path, constants.PSM)
            shutil.copyfile(fn_src, fn_dest)

            # run psm
            fn_log = os.path.join(self.cwd_path, constants.PSMLOG)

            if self.box_is_windows:
                cmd_parts = ["cmd", "/c", "python -u {} > {}".format(fn_dest, fn_log)]
            else:
                cmd_parts = ["bash", "-c", "python -u {} > {}".format(fn_dest, fn_log)]
            
            process_utils.start_async_run_detached(cmd_parts, self.cwd_path, "runpsm.log")

    def get_running_entry_name(self):
        text = None

        controller_cwd = utils.get_controller_cwd(self.box_is_windows, is_local=True)

        fn_current = os.path.join(controller_cwd, constants.CURRENT_RUNNING_ENTRY)
        if os.path.exists(fn_current):
            text = file_utils.read_text_file(fn_current).strip()

        return text

    def get_status(self, fn_entry):
        status = "completed"      # unless below finds different

        fn_queue_entry = os.path.join(self.psm_queue_path, fn_entry)
        if os.path.exists(fn_queue_entry):
            status = "queued"
        else:
            text = self.get_running_entry_name()
            if text == fn_entry:
                # entry might be running; is the controller active?
                if self._get_controller_process():
                    status = "running"

        return status

    def cancel(self, fn_entry):
        cancelled = False
        status = "completed"

        # don't call get_entry_status - check details JIT to minimize race conditons
        fn_queue_entry = os.path.join(self.psm_queue_path, fn_entry)

        if os.path.exists(fn_queue_entry):
            os.remove(fn_queue_entry)
            cancelled = True
        else:
            text = self.get_running_entry_name()
            if text == fn_entry:
                # entry might be running; is the controller active?
                p = self._get_controller_process()
                if p:
                    p.kill()
                    cancelled = True

        return cancelled, status

    def read_log_file(self, fn_entry, start_offset, end_offset):

        fn_entry_base = os.path.splitext(fn_entry)[0]
        fn_log = os.path.join(self.psm_log_path, fn_entry_base + ".log")

        new_bytes = b""

        if os.path.exists(fn_log):
            with open(fn_log, "rb") as infile:
                infile.seek(start_offset)

                if end_offset:
                    new_bytes = infile.read(end_offset-start_offset)
                else:
                    new_bytes = infile.read()

        return new_bytes
