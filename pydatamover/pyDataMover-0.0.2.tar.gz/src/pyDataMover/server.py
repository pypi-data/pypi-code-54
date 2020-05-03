
#from .movers.file_wdt import FileWdt
#from .movers.wdt_file import WdtFile
#from .movers.file_s3 import FileS3
from .movers.file_file import FileFile
from .utils import ProgressTypes
from .route import Route

import datetime
import pandas as pd



class MoverServer():
    """
    pyDataMover server used to manage multiple movers.
    """

    mover_types = {
        #'wdt_file':  WdtFile,
        #'file_wdt':  FileWdt,
        'file_file': FileFile,
        #'file_s3':   FileS3,
        's3_file':   None,
        's3_s3':     None,
        'wdt_s3':    None,
        's3_wdt':    None,
    }

    def __init__(self, max_transfers: int = 5):
        self.max_transfers = max_transfers
        self.movers = dict()
        self.routes = dict()
        self.latest_progress = dict()

        self.start_datetime = datetime.datetime.now().timestamp()
        self.stats_ts = pd.DataFrame(index=pd.date_range(self.start_datetime, periods=1, freq='s'))

    def create(self,
               *args,
               mover_type: str,
               name: str,
               options: dict = {},
               progress_type: ProgressTypes = ProgressTypes.NONE,
               **kwargs):

        """
        Creates a new pyDataMover Mover.

        :param name: Unique name of the transfer
        :param progress_type: What type of progress callbcak will be used.
        :param options: A dict of options used as DataMover options.
        """

        if name in self.movers:
            raise ValueError(f'A mover by the name of "{name}" already exists')

        if mover_type not in self.mover_types or self.mover_types[mover_type] is None:
            raise ValueError(f'The mover "{name}" has not been implemented yet.')

        if mover_type == 'wdt_file': #FIXME
            if 'progress_type' in kwargs:
                del kwargs['progress_type']

        options['progress_report_interval_millis'] = 200

        self.movers[name] = self.mover_types[mover_type](
            *args,
            name=name,
            options=options,
            progress_type=progress_type,
            **kwargs,
        )

    def create_route(self, name, src_server, dst_server, src_dirs, dst_dirs, availible_bandwith = 1024, max_concurent_transfers = 5):

        if name in self.routes:
            raise ValueError(f'A Route by the name of "{name}" already exists')

        self.routes[name] = Route(
            name=name,
            src_server=src_server,
            dst_server=dst_server,
            src_dirs=src_dirs,
            dst_dirs=dst_dirs,
            availible_bandwith=availible_bandwith,
            max_concurent_transfers=max_concurent_transfers)
        return True

    def delete_route(self, name):

        if name not in self.routes:
            raise ValueError(f'No Route by the name of "{name}" exists, can not delete')

        # TODO: check of any transfers are active.
        del self.routes[name]


    def start(self, name: str):
        """
        Starts the receiver by name in Async mode and returns.

        :param name: Name of the reciver to start.
        """
        self.movers[name].start()

    def state(self, name: str) -> bool:
        """
        Retearch Ture or False depending on if the transfer
        :param name: Name of the reciver to stop.
        """

        return self.movers[name]['receiver'].state

    def finish(self, name: str, force: bool = False):
        """
        Finish a receiver by name and return the transfer repport

        :param name: Name of the reciver to stop.
        :param force: whether or not to force receiver to stop if it is not done.

        :return: report of the transfer
        """
        return self.movers[name].finish(force=force)


    def delete(self, name: str):
        del self.movers[name]

    def get_uri(self, name: str):
        """
        Returns a worker URI, with or without the secret, by name.

        :param name: The name of the Receiver request.

        :return: The Receiver URI with or without the secret.
        """

        return self.movers[name].get_uri()

    def rethrottle(self, name: str, mbs: int) -> bool:
        return self.movers[name].rethrottle(mbs)
