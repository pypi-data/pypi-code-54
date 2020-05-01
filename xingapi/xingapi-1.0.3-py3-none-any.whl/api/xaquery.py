import pythoncom
import win32com.client

from xingapi import Res
import pandas as pd
import time
from datetime import timedelta

class QueryEvents:
    def __init__(self):
        self.received = False

    def OnReceiveData(self, trcode):
        self.received = True

    def OnReceiveMessage(self, err, code, msg):
        pass

class Query:
    def __init__(self, trcode):
        self.com = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", QueryEvents)
        self.res = Res(trcode)
        self.com.LoadFromResFile(self.res.path)

    def __call__(self, **input_kwargs):
        return self.call(**input_kwargs)

    def set_inputs(self, block_name, **kwargs):
        for k, v in kwargs.items():
            self.com.SetFieldData(block_name, k, 0, v)

    def get_outputs(self, block_name, *args):
        counts = self.com.GetBlockCount(block_name)
        data = []
        for i in range(counts):
            datum = {}
            for k in args:
                label = self.res.blocks[block_name][k]
                value = self.com.GetFieldData(block_name, k, i)
                datum[label] = value
            data.append(datum)
        return pd.DataFrame(data)

    def request(self, occurs=False):
        self.com.received = False
        self.com.Request(occurs)
        while not self.com.received:
            pythoncom.PumpWaitingMessages()

    def wait(self):
        delay = 1/self.com.GetTRCountPerSec(self.res.name)
        time.sleep(delay)

        limit = self.com.GetTRCountLimit(self.res.name)
        count = self.com.GetTRCountRequest(self.res.name)
        print(f'[{count:4}/{limit:4}]', end='\r')
        
        if count==limit:
            remaining = 600-count*delay
            start = time.time()
            while True:
                elapsed = time.time()-start
                time.sleep(0.1)
                print(f'[{count:4}/{limit:4}] 조회제한 경과시간 {timedelta(seconds=elapsed)}', end='\r')
                if elapsed>remaining:
                    break

    def block_request(self, is_next=False, **input_kwargs):
        for block_name, block_codes in self.res.blocks.items():
            if 'InBlock' in block_name:
                self.set_inputs(block_name, **input_kwargs)
        
        self.request(is_next)
        self.wait()

        outputs = {}
        for block_name, block_codes in self.res.blocks.items():
            if 'OutBlock' in block_name: 
                output_args = tuple(block_codes.keys())
                outputs[block_name] = self.get_outputs(block_name, *output_args)
        return outputs

    def call(self, **input_kwargs):
        return self.block_request(is_next=False, **input_kwargs)
    
    def next(self, **input_kwargs):
        return self.block_request(is_next=True, **input_kwargs)

