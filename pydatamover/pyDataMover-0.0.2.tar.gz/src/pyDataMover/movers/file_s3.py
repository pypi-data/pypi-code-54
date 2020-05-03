import logging
from enum import Enum
from tqdm import tqdm
tqdm.monitor_interval = 0 # If used, we are manually controlling the progress refresh
from ..utils import ProgressTypes, States
from .mover import MoverBase
from .._pyDataMover import (WdtTransferRequest,
                     ProgressReporter,
                     FileS3 as CFileS3,
                     setupAbortChecker,
                     ThrottlerOptions,
                     Throttler,
                     ErrorCode,
                     )

class FileS3(MoverBase):
    def __init__(self,
                 name: str,
                 src_dir: str,
                 thread_count: int = 8,
                 progress_type: ProgressTypes = ProgressTypes.TRACK,
                 options: dict = {}):
        super().__init__(progress_type=progress_type)

        self.logger = logging.getLogger('pyWdt.FileS3')

        self.name = name
        self.src_dir = src_dir
        self.thread_count = thread_count

        self.async_code = None

        self.progress = list()
        self.pbar = None
        self.options = self.generate_settings_obj(options)

        self.throttler = Throttler(self.options.getThrottlerOptions())

        self.transfer = WdtTransferRequest(5555, self.thread_count, self.src_dir)
        self.transfer.directory = self.src_dir
        self.transfer.destination = self.src_dir

        self.progress_reporter = ProgressReporter(self.transfer)
        if self.progress_type == ProgressTypes.TRACK:
            self.progress_reporter.set_callbacks(
                self._gen_display_progress(),
                self._gen_null_log_progress(),
            )
        if self.progress_type == ProgressTypes.DISPLAY:
            self.progress_reporter.set_callbacks(
                self._gen_display_progress(),
                self._gen_null_log_progress(),
            )
        elif self.progress_type == ProgressTypes.NONE:
            self.progress_reporter.set_callbacks(
                self._gen_null_display_progress(),
                self._gen_null_log_progress(),
            )

        self.mover = CFileS3(self.transfer)
        self.mover.setWdtOptions(self.options)
        self.mover.setThrottler(self.throttler)
        self.mover.setProgressReporter(self.progress_reporter)

        self.request = self.mover.init()

    def start(self):
        # FIXME: this needs to be moved.
        if self.progress_type == ProgressTypes.DISPLAY:
            self.pbar = tqdm(total=100, bar_format=self.tqdm_bar_format)

        self.async_code = self.mover.transferAsync()
        return self.async_code

    def rethrottle(self, mbs: int) -> bool:
        self.options.avg_mbytes_per_sec = mbs
        self.throttler.setThrottlerRates(self.options.getThrottlerOptions())
        return True
