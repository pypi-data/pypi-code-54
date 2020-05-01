import os
import sys
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer
import time
import random
import hashlib
import string
import json
import shutil
import psutil
from . import contants
from . import util

KEY_LENGTH = 32

TAMPER_ALERT_RESULT = {
    "score": 0,
    "output": "Result tampering detected!",
    "visibility": "visible",
    "extra_data": {}
}

class ProcessTracker:
    def __init__(self):
        self.pids_on_startup = self._scan_new_pids([])
        self.new_pids = []

    def _scan_new_pids(self, ignore_pids):
        pids = psutil.pids()
        return [pid for pid in pids if pid not in ignore_pids]

    def update_pids(self):
        self.new_pids = self._scan_new_pids(self.pids_on_startup)
        # print(self.new_pids)

    def purge(self):
        if contants.IS_WINDOWS: return
        for pid in self.new_pids:
            psutil.Process(pid).kill()


class ResultWatchdog:
    def __init__(self, result_file, timeout=600):
        self.hash_file = "./result_hash.txt"
        self.tamper_file = "./tamper.json"
        self.key = ''.join(random.choices(string.ascii_lowercase + string.digits, k=KEY_LENGTH))
        self.result_file = result_file
        self.timeout = timeout
        self.tamper_alert_result = json.dumps(TAMPER_ALERT_RESULT)
        self.tamper_hash = self._generate_hash(self.tamper_alert_result)
        self.process_tracker = ProcessTracker()

    def launch(self):
        if contants.IS_WINDOWS:
            print("Result Watchdog cannot run in the background in windows. Running as main process.")  
        elif os.fork() != 0: return
        self._launch_watchdog()

    def _launch_watchdog(self):
        path = os.path.abspath(os.path.dirname(self.result_file))
        print(path)
        event_handler = Handler(self.result_file, lambda: self._validate_result())
        observer = Observer()
        observer.schedule(event_handler, path=path, recursive=False)
        observer.start()
        start = time.time()
        try:
            while time.time() - start < self.timeout:
                self.process_tracker.update_pids()
                time.sleep(0.3)
        except KeyboardInterrupt:
            print("Stopping watchdog")
        observer.stop()
        observer.join()
        print("Watchdog terminated")
        sys.exit()
        

    def _generate_hash(self, s):
        h = hashlib.sha256()
        h.update(s.encode('utf-8'))
        h.update(self.key.encode("utf-8"))
        return h.hexdigest()

    def submit_hash(self, s):
        with open(self.hash_file, "w+") as f:
            f.write(self._generate_hash(s))

    def _validate_result(self):
        if not os.path.exists(self.hash_file):
            self._write_tamper_alert_result()
            return
        
        with open(self.hash_file) as f:
            ref_hash = f.read()

        with open(self.result_file) as f:
            result = f.read()
        result_hash = self._generate_hash(result)
        if result_hash != ref_hash:
            self._write_tamper_alert_result()

    def _write_tamper_alert_result(self):
        self._find_tampering_process()
        os.remove(self.result_file)
        with open(self.hash_file, "w+") as f:
            f.write(self.tamper_hash)
        
        succeeded = False
        while not succeeded:
            try:
                with open(self.result_file, "w+") as f:
                    f.write(self.tamper_alert_result)
                succeeded = True
            except PermissionError:
                pass
        self.process_tracker.purge()

    # def _find_tampering_process(self):
    #     print("Scanning processes")
    #     for pid in self.new_pids:
    #         try:
    #             proc = psutil.Process(pid)
    #             # this returns the list of opened files by the current process
    #             print(proc.pid,proc.name)
    #             flist = proc.open_files()
    #             if flist:
    #                 for nt in flist:
    #                     if "result.json" in nt.path:
    #                         print("!!!!!!!!!")
    #                     print("\t",nt.path)

    #         # This catches a race condition where a process ends
    #         # before we can examine its files    
    #         except psutil.NoSuchProcess as err:
    #             print("****",err) 
    #         except psutil.AccessDenied:
    #             pass
    #     print("Scanning complete")

class Handler(PatternMatchingEventHandler):
    def __init__(self, result_file, callback):
        # print(os.path.basename(result_file))
        PatternMatchingEventHandler.__init__(self, patterns=['*.json'], ignore_directories=True, case_sensitive=False)
        self.callback = callback

    def on_created(self, event):
        self.callback()

    def on_modified(self, event):
        self.callback()
