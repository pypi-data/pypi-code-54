from colorama import Style, Fore
from copy import deepcopy


class LiveData:
    def __init__(self, symbol):
        self.timestamp = None
        # self.exchange = 'NSE'
        self.symbol = symbol
        self.symbol_id = None
        self.ltp = None
        self.best_bid_price = None
        self.best_bid_qty = None
        self.best_ask_price = None
        self.best_ask_qty = None
        self.volume = None
        self.atp = None
        self.oi = None
        self.turnover = None
        self.special_tag = ""
        self.day_high = None
        self.day_low = None
        self.day_open = None
        self.starting_formatter = ""
        self.ending_formatter = ""
        # For level 2 and level 3 data
        # self.bids = []
        # self.asks = []

    def __eq__(self, other):
        res = True
        try:
            if self.timestamp != other.timestamp \
                    or self.symbol != other.symbol\
                    or self.ltp != other.ltp\
                    or self.best_bid_price != other.best_bid_price\
                    or self.best_bid_qty != other.best_bid_qty\
                    or self.best_ask_price != other.best_ask_price\
                    or self.best_ask_qty != other.best_ask_qty\
                    or self.volume != other.volume\
                    or self.atp != other.atp\
                    or self.oi != other.oi\
                    or self.turnover != other.turnover:
                res = False
        except AttributeError:
            res = False
        return res

    def __str__(self):
        if self.special_tag == "":
            self.starting_formatter = self.ending_formatter = ""
        elif self.special_tag != "":
            if self.special_tag == "H":
                self.starting_formatter = f"{Style.BRIGHT} {Fore.GREEN}"
            elif self.special_tag == "":
                self.starting_formatter = f"{Style.BRIGHT} {Fore.RED}"
            self.ending_formatter = f"{Style.RESET_ALL}"
        op_dict = deepcopy(self.__dict__)
        del op_dict['starting_formatter']
        del op_dict['ending_formatter']
        return f"{self.starting_formatter} {str(op_dict)} {self.ending_formatter}"


class TouchlineData:
    def __init__(self):
        self.symbol = None
        self.truedata_id = None
        self.open = None
        self.high = None
        self.low = None
        self.close = None
        self.prev_close = None
        self.ttq = None
        self.oi = None
        self.turnover = None

    def __str__(self):
        return str(self.__dict__)
