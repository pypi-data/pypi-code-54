#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
"""
    Méthode de la classe Simulation
 
    Usage:
 
    >>> from boiler_simulation import param , current_time, advance_time, setProp
    >>> param()
    >>> current_time()
    >>> advance_time()
    >>> setProp()
"""

import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup
import json
import sys

__all__ = ['param'],['current_time'],['advance_time'],['setProperties'],['delSimulation']
class Simulation:

    def __init__(self,param):
        ## constructeur de la classe
        
        self.url="http://localhost:5000/v1/Simulator/"
        self.header={"content-type": "application/json"}
        self.guid=""
        self.payloadInit=""
        v=self.checkServer("ping")
        if v=="ko":
            print("server non actif contacter votre administrateur")
            SystemExit()
        else:
            v1=str(param.get('service:dhw:production_fan_throttle'))
            v2=str(param.get('production:auxiliary:settings:startup_throttle'))
            v3=str(param.get('production:auxiliary:timers:ignition'))
            v4=str(param.get('production:auxiliary:timers:stop'))
            
            self.payloadInit=[
                    {
                    "urn": "service:dhw:production_fan_throttle",
                    "fields": [
                        {
                            "name": "value",
                            "value": v1
                        }
                    ]
                    },
                    {
                    "urn": "production:auxiliary:settings:startup_throttle",
                    "fields": [
                        {
                            "name": "value",
                            "value": v2
                        }
                    ]
                    },
                    {
                    "urn": "production:auxiliary:timers:ignition",
                    "fields": [
                        {
                            "name": "value",
                            "value": v3
                        }
                    ]
                    },
                    {
                    "urn": "production:auxiliary:timers:stop",
                    "fields": [
                        {
                            "name": "value",
                            "value": v4
                        }
                    ]
                    }    
                ]

            r=self.init("start")
            print(r)
            #s=self.send("service:dhw:START")
            #print(s)
            
    def __del__(self):
        ## destructeur de la classe
        try:
            t=self.send("service:dhw:STOP")
            print(t)  
        except ConnectionError:
            pass
    
    def __getitem__(self, key):
        r=self.results("results/lastOf/" + key)
        return r
    
    def __setitem__(self, key, value):
        self.setProperties(key,value)
        pass


    def init(self,route):
        try:
            r = requests.post(self.url + route,data=json.dumps(self.payloadInit), headers=self.header, verify=False)
            result="ko"
            if r.status_code == 200:
                self.guid = r.text.replace('"','')
                result = "Simulation initialisée avec le numéro : " + r.text.replace('"','')
            else:
                result = result + " erreur code : " + str(r.status_code) + " " + self.url + " " + route + " " +  str(self.payloadInit)
            return result       
            
        except IndexError:
            raise LookupError('init Error')
    
    def delSimulation(self,route):
        t=self.send("service:dhw:STOP")
        print(t)

    def checkServer(self,route):
        try: 
            result=""           
            r=requests.get(self.url  + route, headers=self.header, verify=False)
            if r.status_code == 200:
                result="Server dot net actif"
            else:
                result = "okP" #"server non actif contacter votre administrateur, code server :" + str(r.status_code) 
            return result
        except ConnectionError:
            print("server non actif contacter votre administrateur")
            sys.exit(141)


    def results(self,route):
        try:
            result="ko"
            if self.guid != "":
                r=requests.get(self.url + self.guid + "/" + route, headers=self.header, verify=False)
                if r.status_code == 200:
                    result=r.json()
                else:
                    if r.status_code == 204:
                        result="None"
                    else:
                        result = result + " erreur code : " + str(r.status_code) 
            return result
        except IndexError:
            raise LookupError('param Error')

    def send(self,key):
        try:
            route="message"
            payload={
                "urn": key,
                "value": "."
                }
            result="ko"
            route=("message")
            if self.guid != "":
                r=requests.post(self.url + self.guid + "/" + route, data=json.dumps(payload), headers=self.header, verify=False)
                if r.status_code == 200:
                    if key=="service:dhw:STOP":
                        result="STOP Simulation " 
                    else:
                        result="START Simulation "                     
                else:
                    result = result + " erreur code : " + str(r.status_code) + " " + r.text + " " + self.url + self.guid + "/" + route + " " + str(self.payloadStart)
            return result
        except IndexError:
            raise LookupError('start Error')
    
    def current_time(self,route):
        try:
            result="ko"
            if self.guid != "":
                r=requests.get(self.url + self.guid + "/" + route, headers=self.header, verify=False)
                if r.status_code == 200:
                    result=r.text
                else:
                    result = result + " erreur code : " + str(r.status_code) + " " + r.text + " " + self.url + self.guid + "/" + route + " " + str(self.payloadStop)
            return result
        except IndexError:
            raise LookupError('stop Error')

    def advance_time(self,advTime):
        try:
            route="time"
            result="ko"
            if self.guid != "":
                r=requests.post(self.url + self.guid + "/" + route, data=str(advTime), headers=self.header, verify=False)
                if r.status_code == 200:
                    result="Advanced_time " + str(advTime) + " ms"
                else:
                    result = result + " erreur code : " + str(r.status_code) + " " + r.text + " " + self.url + self.guid + "/" + route + " " + str(self.payloadStop)
            return result
        except IndexError:
            raise LookupError('stop Error')
    
    def setProperties(self,key,value):
        jsonval=[
            {
            "urn": str(key),
            "fields":[{"name":"value","value": str(value)}]
            }
        ]
        try:
            result="ko"
            route="properties"
            if self.guid != "":
                r=requests.post(self.url + self.guid + "/" + route, data=json.dumps(jsonval), headers=self.header, verify=False)
                if r.status_code == 200:
                    result= r.text
                else:
                    result = result + " erreur code : " + str(r.status_code) + " " + r.text + " " + self.url + self.guid + "/" + route + " " + str(jsonval)
            return result
        except IndexError:
            raise LookupError('stop Error')

    

if __name__ == "__main__":
    #Simulation.param()
    Simulation.current_time()
    Simulation.advance_time()
    Simulation.setProperties()
    Simulation.delSimulation()




        
