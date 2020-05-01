import inspect
import ctypes
import threading
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
import asyncio
import time

'''需要在if __anme__=='__main__':的环境下运行'''


# 获取cpu数量
def getCPUNumber():
    return multiprocessing.cpu_count()


# 进程池
def processPool(maxnum, func, argslist, onevalue=False):
    pool = ProcessPoolExecutor(max_workers=maxnum)
    ps = []
    for args in argslist:
        if onevalue:
            ps.append(pool.submit(func, args))  # 放入单值
        else:
            ps.append(pool.submit(func, *args))  # 执行多值
    # pools.map(func, *argslist)  # 维持执行的进程总数为num，当一个进程执行完毕后会开始执行排在后面的进程
    return pool, ps


# 线程池
def threadPool(maxnum, func, argslist, onevalue=False):
    pool = ThreadPoolExecutor(max_workers=maxnum)
    ps = []
    for args in argslist:
        if onevalue:
            ps.append(pool.submit(func, args))  # 放入单值
        else:
            ps.append(pool.submit(func, *args))  # 执行多值
    # pools.map(func, *argslist)  # 维持执行的进程总数为num，当一个进程执行完毕后会开始执行排在后面的进程
    return pool, ps


# 协程运行
def tasksRun(*tasks):
    if len(tasks) == 1:
        asyncio.get_event_loop().run_until_complete(asyncio.gather(tasks[0]))
    else:
        asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))


def retryFunc(func, *values, **args):
    ci = args.get('ci', 3)
    sleeptime = args.get('sleeptime', 1)
    sleepfunc = args.get('sleepfunc', time.sleep)
    index = args.get('index', '')
    for i in range(1, ci + 1):
        try:
            return func(*values)
        except Exception as e:
            print(e)
            print(index, '失败，正在重试...第', ci, '次')
            if sleeptime > 0: sleepfunc(sleeptime)
    print('重试全部失败，返回None')
    return None


# 多任务分配
def getTasks(num, taskdatas):
    tasklen = len(taskdatas)
    num = min(num, tasklen)
    cellnum = tasklen // num if tasklen % num == 0 else tasklen // num + 1
    tasks = list()
    for i in range(0, tasklen, cellnum):
        tasks.append(taskdatas[i:i + cellnum])
    return tasks


# 自定义线程类模型
class Thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.__alive = False

    def start(self):
        threading.Thread.start(self)
        self.__alive = True

    def stop(self):
        self.__alive = False
        stop_thread(self)

    def is_alive(self):
        return threading.Thread.is_alive(self) and self.__alive


# 关闭线程
def stop_thread(thread: Thread):
    tid = thread.ident
    exctype = SystemExit
    # _async_raise
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")
