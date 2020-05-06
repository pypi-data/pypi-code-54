import sys
from .websocket import tests

print(f'Running main with sys.argv = {sys.argv}')
if sys.argv[1] == 'run_all_tests':
    username = sys.argv[2]
    password = sys.argv[3]
    exchange = sys.argv[4]
    try:
        live_port = int(sys.argv[5])
        hist_port = int(sys.argv[6])
    except IndexError:
        live_port = None
        hist_port = None
    tests.run_all_tests(username, password, exchange, live_port, hist_port)
