""" A module for ping sweeping a network """
import multiprocessing
import subprocess
import os

def pinger( job_q, results_q ):
    """ A function for pinging using ping from system """
    DEVNULL = open(os.devnull,'w')
    while True:
        ip = job_q.get()
        if ip is None: break

        try:
            subprocess.check_call(['ping','-c1',ip],
                                  stdout=DEVNULL)
            results_q.put(ip)
        except:
            pass

def sweep(subnet):
    """ A sweeper for finding hosts that respond to ping given a class C network

    Args:
        subnet: A string in the form of 192.168.10 or similar
    
    Returns: A list of ip addresses that responded
    """
    responses = []
    pool_size = 255
    jobs = multiprocessing.Queue()
    results = multiprocessing.Queue()

    pool = [ multiprocessing.Process(target=pinger, args=(jobs,results))
             for i in range(pool_size) ]

    for p in pool:
        p.start()

    for i in range(1,255):
        value = str(subnet) + '.' + str(i)
        jobs.put(value)

    for p in pool:
        jobs.put(None)

    for p in pool:
        p.join()

    while not results.empty():
        ip = results.get()
        responses.append(ip)
    
    return responses

if __name__ == '__main__':
    sweep('10.10.10')