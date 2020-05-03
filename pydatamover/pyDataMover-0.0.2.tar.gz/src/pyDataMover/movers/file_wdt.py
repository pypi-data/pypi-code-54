import logging
from tqdm import tqdm
tqdm.monitor_interval = 0 # If used, we are manually controlling the progress refresh
from ..route import Route
from ..utils import ProgressTypes, States
from .mover import MoverBase
from .._pyDataMover import (WdtTransferRequest,
                            ProgressReporter,
                            FileWdt as CFileWdt,
                            setupAbortChecker,
                            ThrottlerOptions,
                            Throttler,
                            ErrorCode,
                            )

class FileWdt(MoverBase):
    def __init__(self,
                 name: str,
                 src_dir: str,
                 uri: str,
                 weight: int = 1,
                 route: Route = None,
                 progress_type: ProgressTypes = ProgressTypes.TRACK,
                 options: dict = None):
        super().__init__(self)

        self.logger = logging.getLogger('pyWdt.FileWdt')

        self.progress_type = progress_type

        self.name = name
        self.uri = uri
        self.src_dir = src_dir

        self.async_code = None
        self.route = route
        self.weight = weight

        self.progress = list()
        self.pbar = None

        if options is None:
            options = {}
        import pprint
        pprint.pprint(options)
        self.options = self.generate_settings_obj(options)

        self.throttler = Throttler(self.options.getThrottlerOptions())

        self.transfer = WdtTransferRequest(self.uri)
        self.transfer.directory = self.src_dir

        print(f"PROGRESS TYPE: {self.progress_type}")
        self.progress_reporter = ProgressReporter(self.transfer)
        if self.progress_type == ProgressTypes.TRACK:
            print('TRACKING')
            self.progress_reporter.set_callbacks(
                self._gen_track_progress(),
                self._gen_null_log_progress(),
            )
        elif self.progress_type == ProgressTypes.DISPLAY:
            print('DISPLAY')
            self.progress_reporter.set_callbacks(
                self._gen_display_progress(),
                self._gen_null_log_progress(),
            )
        elif self.progress_type == ProgressTypes.NONE:
            print('NONE')
            self.progress_reporter.set_callbacks(
                self._gen_null_display_progress(),
                self._gen_null_log_progress(),
            )

        self.mover = CFileWdt(self.transfer)
        self.mover.setWdtOptions(self.options)
        #self.mover.setAbortChecker(setupAbortChecker())
        self.mover.setThrottler(self.throttler)
        self.mover.setProgressReporter(self.progress_reporter)

        self.request = self.mover.init()

    def start(self):

        if self.state != States.CREATED:
            print('Can only start a mover that is in a CREATED state.')
            return

        # FIXME: this needs to be moved.
        if self.progress_type == ProgressTypes.DISPLAY:
            self.pbar = tqdm(total=100, bar_format=self.tqdm_bar_format)

        self.async_code = self.mover.transferAsync()

        if self.route:
            self.route.add_transfer(transfer=self)

        return self.async_code

    def rethrottle(self, mbs: int) -> bool:

        if self.state not in [States.CREATED, States.RUNNING]:
            print('Can only rethrottle a mover that is in a CREATED or RUNNING state.')
            return

        self.options.avg_mbytes_per_sec = mbs
        self.throttler.setThrottlerRates(self.options.getThrottlerOptions())
        return True
