
import socket
import math
from .utils import round_down


class Route():

    def __init__(self,
                 name,
                 src_server,
                 dst_server,
                 src_dirs,
                 dst_dirs,
                 availible_bandwith = 1024,
                 max_concurent_transfers = 5
                ):
        self.availible_bandwith = int(availible_bandwith)
        self.max_concurent_transfers = int(max_concurent_transfers)
        self.transfers = dict()
        self.total_weight = 0

        self.name = name
        self.src_server = src_server #or socket.getfqdn()
        self.dst_server = dst_server #or socket.getfqdn()
        self.src_dirs = src_dirs
        self.dst_dirs = dst_dirs

    def add_transfer(self, transfer):
        """
        Adds a transfer to the route
        """
        #if transfer.name in self.transfers:
        #    pass
        #    #BAD!!!!!
        print(f'add transfer {transfer.name}')
        self.transfers[transfer.name] = dict()
        self.transfers[transfer.name]['obj'] = transfer
        self.transfers[transfer.name]['weight'] = transfer.weight
        self.transfers[transfer.name]['throughput_percent'] = 0
        self.transfers[transfer.name]['mbs'] = 0

        self._calc_total_weight()
        self.redistribute()

    def del_transfer(self, name):
        # TODO: calidate transfer has finished
        del self.transfers[name]
        self._calc_total_weight()
        self.redistribute()

    def redistribute(self):
        for transfer in self.transfers:
            tfr = self.transfers[transfer]
            tfr['throughput_percent'] = tfr['weight'] / self.total_weight
            tfr['mbs'] = round_down(self.availible_bandwith * tfr['throughput_percent'], 1)
            print(f"Rethrottleing {tfr['obj'].name} to {tfr['mbs']}")
            tfr['obj'].rethrottle(tfr['mbs'])

    def _calc_total_weight(self):
        print("in calc")
        self.total_weight = 0
        for transfer in self.transfers:
            self.total_weight += int(self.transfers[transfer]['weight'])
        print(f"Total weight: {self.total_weight}")
