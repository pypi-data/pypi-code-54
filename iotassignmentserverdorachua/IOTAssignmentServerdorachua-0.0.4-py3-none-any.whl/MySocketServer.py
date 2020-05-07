import asyncio
import sys
from random import randint
from random import random
from datetime import datetime

import json
from IOTAssignmentUtilitiesdorachua import MySQLManager
from IOTAssignmentServerdorachua.GrabCar import GrabCar
from IOTAssignmentServerdorachua.MyNewCarsFeeder import MyNewCarsFeeder
import argparse

class MySocketServer:

    def __init__(self,u,pw,h,db):
        self.user = u
        self.password = pw
        self.host = h
        self.database = db
        self.isconnected = False

    def setNewCarsFeeder(self,feeder):
        self.feeder = feeder

    async def handle_client(self,reader, writer, cars, timeout,nextfeedtime,u,pw,h,db):        

            timenow = datetime.now()

            if timenow == nextfeedtime:
                cars,timeout,nextfeedtime = self.feeder.getCars()

            data = await reader.read(100)        
            message = data.decode("utf-8")
            addr = writer.get_extra_info('peername')

            dt = datetime.now()
            fn = f"{dt.year}-{dt.month}-{dt.day} {dt.hour}:{dt.minute}:{dt.second}"
            
            print(f"Received {message} from {addr} at {fn}")        
            
            str_to_send = ""
            readings = []
            for i in range(0,len(cars)):
                reading = cars[i].read(message)
                if reading is not None:
                    readings.append(reading)
                
            if len(readings)>0:            
                writer.write(json.dumps(readings).encode("utf-8"))
                await writer.drain()            
            
                #print("Close the connection")

            writer.close()    

async def main():

    try:
        
        #host,port = '134.209.106.132',8889 
        host,port = "127.0.0.1", 8889
        parser = argparse.ArgumentParser(description='Process some integers.')
        parser.add_argument('host')
        parser.add_argument('port',type=int)
        
        args = parser.parse_args()
        if args.host:
            host = args.host
        if args.host:
            port = args.port
        

        
        #cars = [gc.GrabCar("996432412828.0"),
        #        gc.GrabCar("1099511627855.0"),
        #        gc.GrabCar('1176821039224.0')]
        #cars = [#gc.GrabCar("34359738469.0"),gc.GrabCar("17179869274.0"),gc.GrabCar("17179869346.0"),
                #gc.GrabCar("68719476877.0"),gc.GrabCar("8589934741.0"),gc.GrabCar("42949673148.0")]
        #        gc.GrabCar("17179869282.0"), gc.GrabCar("17179869346.0"),gc.GrabCar("51539607588.0")]
        #cars = [gc.GrabCar("17179869282.0"), gc.GrabCar("17179869346.0"),gc.GrabCar("51539607588.0")]        
        u='iotuser';pw='iotPa55word!!';h='localhost';db='iotdatabase'
        
        myfeeder = MyNewCarsFeeder(u,pw,h,db,1,10)
        myserver = MySocketServer(u,pw,h,db)
        myserver.setNewCarsFeeder(myfeeder)

        cars,timeout,nextfeedtime,currentbid= myfeeder.getCars(3)
        print(f"Serving information for {len(cars)} cars")

        server = await asyncio.start_server(lambda r, w: myserver.handle_client(r, w, cars, timeout,nextfeedtime,u,pw,h,db), host,port)

        addr = server.sockets[0].getsockname()
        print(f'Serving on {addr}')

        async with server:
            await server.serve_forever()        
        
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit()

    except:
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])

asyncio.run(main())

