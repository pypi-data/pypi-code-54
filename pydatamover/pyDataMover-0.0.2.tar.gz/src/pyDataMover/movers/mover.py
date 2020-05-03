

from .._pyDataMover import WdtOptions, ErrorCode
from ..utils import ProgressTypes, States

import uuid
import pandas as pd
from datetime import datetime as dt

class MoverBase:
    """
    Base class for pyDataMover.
    """

    def __init__(self, progress_type=ProgressTypes.NONE):
        if progress_type in ProgressTypes:
            self.progress_type = progress_type
        else:
            self.progress_type = ProgressTypes.NONE

        self.tqdm_bar_format = '{l_bar}{bar}|{n_fmt}% [{elapsed}<{remaining}{postfix}]'

        self.uid = uuid.uuid4()

        pd_now = pd.Timestamp.now()
        self.stats_avg_throughput = pd.Series( [0], index=[pd_now])
        self.stats_cur_throughput = pd.Series( [0], index=[pd_now])
        self.stats_per_throughput = pd.Series( [0], index=[pd_now])
        self.latest_progress = dict()

        self.final_report = None
        self.name = None
        self.mover = None
        self.route = None
        self.progress = list()
        self.pbar = None

    def start(self):
        pass #stub child needs to overwrite

    def stop(self):
        pass #stub child needs to overwrite

    def finish(self, force=False) -> dict:
        """
        Finishes the transfer. If force is True it will abort if it is still running.
        """
        if self.final_report:
            return self.final_report

        self.finish_called = True

        if self.mover is None:
            print('CRAP!!!!!!!!!!!!!!!!!!')
            return False

        if self.mover.isStale():
            rep = self.mover.finish()

            self.final_report = self.transfer_report_to_dict(rep)
        else:
            if force:
                self.mover.abort(ErrorCode.Abort)
                rep = States.FORCEEND
            else:
                rep = States.ABORTED

        #if self.route:
        #    self.route.del_transfer(self.name)

        return self.final_report

    @property
    def state(self):
        """
        Return the state of the mover.
        """

        if self.final_report:
            return States.DONE

        if self.mover.hasStarted():
            if self.mover.isStale():
                state = States.FINISHED
            else:
                state = States.RUNNING
        else:
            state = States.CREATED

        return state

    @property
    def stats(self):
        """Process and return mover stats"""
        #TODO add some pandas magic
        return self.progress

    # Not always needed
    def get_uri(self):
        """ sub method to be replaced"""
        return None

    def get_options(self):
        # FIXME: make sure this is destroid or copied as wdt_options is a reference
        # back to C++
        options = dict()
        wdt_options =  self.mover.getWdtOptions()
        for attr in dir(wdt_options):
            if attr.startswith('__') or attr in ['getThrottlerOptions', 'shouldPreallocateFiles']:
                continue

            if attr == 'isLogBasedResumption':
                value = (wdt_options.enable_download_resumption and not wdt_options.resume_using_dir_tree)
            elif attr == 'isDirectoryTreeBasedResumption':
                value = (wdt_options.enable_download_resumption and wdt_options.resume_using_dir_tree)
            else:
                value = wdt_options.__getattribute__(attr)
            options[attr] = value
        return options

    # Not always needed
    def rethrottle(self, mbs: int) -> bool:
        """ sub method to be replaced"""
        return None

    def generate_settings_obj(self, options):
        """
        Converts a dict of options to a WdtOptions object
        """

        #option_map = {
        #    'thread_count': 'num_ports',
        #}
        obj = WdtOptions()
        for arg in options:
        #    if arg in option_map:
        #        arg = option_map[arg]
            if hasattr(obj, arg):
                #self.logger.debug(f'Setting: {arg} to {options[arg]}')
                print(f'Setting: {arg} to {options[arg]}')
                setattr(obj, arg, options[arg])
            else:
                raise ValueError(f'The attribute "{arg}" is not a valid option')
        return obj

    def transfer_report_to_dict(self, rep):
        """
        Converts a WDT transfer report object to a dict.

        :params rep: The WDT transfer report object to convert.

        :return: Dict of the report
        """
        thread_stats = list()
        for thread in rep.getThreadStats():
            ts_data = {
                'data_bytes': thread.getDataBytes(),
                'header_bytes': thread.getHeaderBytes(),
                'num_blocks_sent': thread.getNumBlocksSend(),
                'total_bytes': thread.getTotalBytes(False),
                'total_sender_bytes': thread.getTotalSenderBytes(),
            }
            thread_stats.append(ts_data)

        return {
            #'summary':                  rep.getSummary(), # FIXME
            'throughput_mbs':           rep.getThroughputMBps(),
            'total_time':               rep.getTotalTime(),
            'transferred_source_stats': rep.getTransferredSourceStats(),
            'failed_source_stats':      rep.getFailedSourceStats(),
            'thread_stats':             thread_stats,
            'failed_directories':       rep.getFailedDirectories(),
            'total_file_size':          rep.getTotalFileSize(),
            'current_throughput_mbps':  rep.getCurrentThroughputMBps(),
            'num_discoverd_files':      rep.getNumDiscoveredFiles(),
            'file_discoveryFinished':   rep.fileDiscoveryFinished(),
            'previously_sent_bytes':    rep.getPreviouslySentBytes(),
        }

    def _update_progress(self, progress, averageThroughput, currentThroughput, numDiscoveredFiles, fileDiscoveryFinished):
        now = dt.now().timestamp()
        pd_now = pd.Timestamp.now()
        self.latest_progress = {
            'state':                    self.state.name,
            'datetime':                 dt.now().timestamp(),
            'progress':                 progress,
            'average_throughput':       averageThroughput,
            'current_throughput':       currentThroughput,
            'num_discoverd_files':      numDiscoveredFiles,
            'file_discovery_finishded': fileDiscoveryFinished,
        }

        self.stats_avg_throughput = self.stats_avg_throughput.append(
            pd.Series([averageThroughput], index=[pd_now]))
        self.stats_cur_throughput = self.stats_cur_throughput.append(
            pd.Series([currentThroughput], index=[pd_now]))
        self.stats_per_throughput = self.stats_per_throughput.append(
            pd.Series([progress], index=[pd_now]))

    def _gen_track_progress(self):
        """
        """
        def track_progress(progress, averageThroughput, currentThroughput, numDiscoveredFiles, fileDiscoveryFinished):
            self._update_progress(progress, averageThroughput, currentThroughput, numDiscoveredFiles, fileDiscoveryFinished)
            return True
        return track_progress

    def _gen_display_progress(self):
        """
        Default function generator for displaying transfer progress callback.
        """
        def display_progress(progress, averageThroughput, currentThroughput, numDiscoveredFiles, fileDiscoveryFinished):
            self._update_progress(progress, averageThroughput, currentThroughput, numDiscoveredFiles, fileDiscoveryFinished)
            self.pbar.set_postfix_str(
                s=f"avg: {round(averageThroughput, 1): 7}, cur: {round(currentThroughput, 1): 7} Mb/s, fcount: {numDiscoveredFiles: 4}",
                refresh=False)
            self.pbar.update(progress - self.pbar.n)
            return True
        return display_progress

    def _gen_log_progress(self):
        """
        Default function generator for logging transfer progress callback.
        """
        def log_progress(effectiveDataBytes, progress, averageThroughput, currentThroughput, numDiscoveredFiles, fileDiscoveryFinished):
            return True
        return log_progress

    def _gen_null_display_progress(self):
        """
        Function generator for noop display progress callback.
        """
        def null_display_progress(progress, averageThroughput, currentThroughput, numDiscoveredFiles, fileDiscoveryFinished):
            self._update_progress(progress, averageThroughput, currentThroughput, numDiscoveredFiles, fileDiscoveryFinished)
            return True
        return null_display_progress

    def _gen_null_log_progress(self):
        """
        Function generator for noop logging progress callback.
        """
        def null_log_progress(effectiveDataBytes, progress, averageThroughput, currentThroughput, numDiscoveredFiles, fileDiscoveryFinished):
            return True
        return null_log_progress

























