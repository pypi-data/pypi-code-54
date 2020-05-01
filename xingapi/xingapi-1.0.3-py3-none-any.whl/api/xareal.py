import pythoncom
import win32com.client

from queue import Queue
from threading import Thread
from xingapi import Res
import pandas as pd

class RealEvents:
    def __init__(self):
        self.queue = None

    def OnReceiveRealData(self, trcode):
        self.res = Res(trcode)
        data = {}
        for key, label in self.res.blocks['OutBlock'].items():
            data[label] = self.GetFieldData("OutBlock", key)
        df = pd.DataFrame([data])
        self.queue.put((trcode, df))


class Real:
    def __init__(self, trcode, queue):
        self.com = win32com.client.DispatchWithEvents("XA_DataSet.XAReal", RealEvents)
        self.res = Res(trcode)
        self.com.LoadFromResFile(self.res.path)
        self.com.queue = queue

    def set_inputs(self, block_name, **kwargs):
        for k, v in kwargs.items():
            self.com.SetFieldData(block_name, k, v)
    
    def advise(self, **input_kwargs):
        self.set_inputs('InBlock', **input_kwargs)
        self.com.AdviseRealData()
        return self

    def advise_many(self, key, vals):
        for val in vals:
            self.set_inputs('InBlock', **{key:val})
            self.com.AdviseRealData()
        return self
    
    def run(self):
        while True:
            pythoncom.PumpWaitingMessages()

    def unadvise(self):
        self.com.UnadviseRealData()
        return self

class RealManager:
    def add(self, trcode, callback=None):
        if not callback:
            callback = self.callback
        queue = Queue()
        real = Real(trcode, queue)
        th = Thread(target=callback, args=(queue,), daemon=True)
        th.start()
        return real

    def callback(self, queue):
        while True:
            data = queue.get()
            print(data)