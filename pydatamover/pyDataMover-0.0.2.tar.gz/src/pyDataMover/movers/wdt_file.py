"""
pyDataMover mover class'
"""
import socket
import logging
from ..utils import ProgressTypes, States
from .mover import MoverBase
from .._pyDataMover import (WdtTransferRequest,
                     ProgressReporter,
                     setupAbortChecker,
                     WdtFile as CWdtFile,
                     ThrottlerOptions,
                     Throttler,
                     ErrorCode,
                     )

# If used, we are manually controlling the progress refresh
#tqdm.monitor_interval = 0


class WdtFile(MoverBase):
    """
    Setup a WdtFile object to accept a connection and receive files.

    :param name: Unique name of the transfer
    :param start_port: Starting port.
    :param thread_count: number of ports to use.
    :param dst_dir: Directory to write data to.
    :param hostname: Hostname to use, default is the actual hostname.
    :param progress_type: What type of progress callbcak will be used.
    :param options: A dict of options used as WDT options.

    """
    def __init__(self,
                 name: str,
                 start_port: int,
                 thread_count: int,
                 dst_dir: str,
                 hostname: str = '',
                 progress_type = None,
                 options: dict = {}):
        super().__init__(progress_type=progress_type)

        self.logger = logging.getLogger('pyWdt.WdtFile')

        self.progress_type = progress_type

        self._state = States.CREATED
        self.name = name
        self.start_port = start_port
        self.thread_count = thread_count
        self.dst_dir = dst_dir
        self.hostname = hostname

        self.async_code = None

        self.progress = list()
        self.pbar = None
        self.options = self.generate_settings_obj(options)

        self.transfer = WdtTransferRequest(self.start_port, self.thread_count, self.dst_dir)
        self.transfer.hostName = hostname or socket.getfqdn()
        self.transfer.transferId = self.name

        self.progress_reporter = ProgressReporter(self.transfer)
        self.progress_reporter.set_callbacks(
            self._gen_null_display_progress(),
            self._gen_null_log_progress(),
        )

        self.mover = CWdtFile(self.transfer)
        #self.mover.setAbortChecker(setupAbortChecker())
        self.mover.setWdtOptions(self.options)
        self.mover.setProgressReporter(self.progress_reporter)

        self.request = self.mover.init()


    def start(self):
        """
        This method starts the mover in Async mode and returns.
        """
        self.async_code = self.mover.transferAsync()
        return self.async_code

    def get_url(self):
        return self.request.genWdtUrlWithSecret()


