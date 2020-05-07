import multiprocessing

# TODO default configuration
host = '0.0.0.0'
port = '5000'
user = ''
group = ''
workers = multiprocessing.cpu_count() * 2 + 1
threads = 1
bind = f'{host}:{port}'
timeout = 60
