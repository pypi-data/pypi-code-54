from truedata_ws.websocket.TD import TD
import sys
from time import sleep

import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

from colorama import Style, Fore

symbols_to_test = {'NSE': ['BANKNIFTY-I', 'NIFTY-I'], 'MCX': ['CRUDEOIL-I']}


def run_all_tests(username, password, exchange, live_port, historical_port):
    td_app = get_connection(username, password, live_port, historical_port)
    run_historical_tests(td_app, symbols_to_test[exchange.upper()])
    run_live_tests(td_app, symbols_to_test[exchange.upper()])


def get_connection(username, password, live_port_ip, historical_port_ip):
    td_app = TD(username, password, live_port=live_port_ip, historical_port=historical_port_ip)
    return td_app


def run_historical_tests(td_app_ip, symbols):
    symbol = symbols[0]
    test_time = datetime.today()
    # Testing malformed historical contracts
    # hist_data_0 = td_app_ip.get_historic_data(f'BANKNIFTY99ZYXFUT')

    # Testing bar historical data
    hist_data_1 = td_app_ip.get_historic_data(f'{symbol}')
    hist_data_2 = td_app_ip.get_historic_data(f'{symbol}', duration='3 D')
    hist_data_3 = td_app_ip.get_historic_data(f'{symbol}', duration='3 D', bar_size='15 mins')
    hist_data_4 = td_app_ip.get_historic_data(f'{symbol}', bar_size='30 mins')
    hist_data_5 = td_app_ip.get_historic_data(f'{symbol}', bar_size='30 mins', start_time=test_time-relativedelta(days=3))
    # Testing tick historical data
    tick_hist_data_1 = td_app_ip.get_historic_data(f'{symbol}', bar_size='tick')
    tick_hist_data_2 = td_app_ip.get_historic_data(f'{symbol}', bar_size='tick', duration='3 D')
    tick_hist_data_3 = td_app_ip.get_historic_data(f'{symbol}', bar_size='tick', start_time=test_time-relativedelta(days=3))

    print(f'{Style.BRIGHT}{Fore.BLUE}------------- HIST BAR DATA TEST RESULTS -------------{Style.RESET_ALL}')
    print(f'{Style.BRIGHT}{Fore.BLUE}HISTDATA 1...{Style.RESET_ALL}')
    print(f"Command used -> hist_data_1 = td_app_ip.get_historic_data('{symbol}')")
    for hist_point in hist_data_1:
        print(hist_point)
    print(f'{Style.BRIGHT}{Fore.BLUE}HISTDATA 2...{Style.RESET_ALL}')
    print(f"Command used -> hist_data_2 = td_app_ip.get_historic_data('{symbol}', duration='3 D')")
    for hist_point in hist_data_2:
        print(hist_point)
    print(f'{Style.BRIGHT}{Fore.BLUE}HISTDATA 3...{Style.RESET_ALL}')
    print(f"Command used -> hist_data_3 = td_app_ip.get_historic_data('{symbol}', duration='3 D', bar_size='15 mins')")
    for hist_point in hist_data_3:
        print(hist_point)
    print(f'{Style.BRIGHT}{Fore.BLUE}HISTDATA 4...{Style.RESET_ALL}')
    print(f"Command used -> hist_data_4 = td_app_ip.get_historic_data('{symbol}', bar_size='30 mins')")
    for hist_point in hist_data_4:
        print(hist_point)
    print(f'{Style.BRIGHT}{Fore.BLUE}HISTDATA 5...{Style.RESET_ALL}')
    print(f"Command used -> hist_data_5 = td_app_ip.get_historic_data('{symbol}', bar_size='30 mins', start_time={test_time - relativedelta(days=3)})")
    for hist_point in hist_data_5:
        print(hist_point)
    print(f'{Style.BRIGHT}{Fore.BLUE}------------- HIST TICK DATA TEST RESULTS -------------{Style.RESET_ALL}')
    print(f'{Style.BRIGHT}{Fore.BLUE}TICKDATA 1...{Style.RESET_ALL}')
    print(f"Command used -> tick_data_1 = td_app_ip.get_historic_data('{symbol}', bar_size='tick')")
    for hist_point in tick_hist_data_1:
        print(hist_point)
    print(f'{Style.BRIGHT}{Fore.BLUE}TICKDATA 2...{Style.RESET_ALL}')
    print(f"Command used -> tick_data_2 = td_app_ip.get_historic_data('{symbol}', bar_size='tick', duration='3 D')")
    for hist_point in tick_hist_data_2:
        print(hist_point)
    print(f'{Style.BRIGHT}{Fore.BLUE}TICKDATA 3...{Style.RESET_ALL}')
    print(f"Command used -> tick_data_3 = td_app_ip.get_historic_data('{symbol}', bar_size='tick', start_time={test_time - relativedelta(days=3)})")
    for hist_point in tick_hist_data_3:
        print(hist_point)

    # Testing conversion to pandas dataframe
    print(f'{Style.BRIGHT}{Fore.BLUE}Converting df_1 to a Pandas DataFrame{Style.RESET_ALL}')
    print(f'Command used -> df = pd.DataFrame(hist_data_1)')
    df = pd.DataFrame(hist_data_1)
    print(df)


def run_live_tests(td_app_ip, symbols):
    # Testing Live data
    # td_app.start_live_data(f'BANKNIFTY{sys.argv[3]}FUTbk')
    print(f'{Style.BRIGHT}{Fore.BLUE}Checking LIVE data streaming...{Style.RESET_ALL}')
    req_id = td_app_ip.start_live_data([f'CRUDEOIL-I'])
    count = 0
    live_data_obj = td_app_ip.live_data[req_id]
    while count < 30:
        if live_data_obj != td_app_ip.live_data[req_id]:
            print(td_app_ip.live_data[req_id].__dict__)
            count = count + 1
            live_data_obj = td_app_ip.live_data[req_id]
