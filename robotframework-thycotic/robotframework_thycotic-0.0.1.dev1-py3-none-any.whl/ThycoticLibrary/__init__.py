#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Cutting Edge QA Marcin Koperski

import os
import sys
import requests
import json
import getpass
from robot.api.deco import library, keyword
import robot.api.logger as logger


@library(scope="GLOBAL", version="3.2")
class ThycoticLibrary:
    token = None
    client = None
    # server fully qualified domain name
    serverFQDN = "FQDN.foo.com"
    # Where your trycotic server application is installed
    appPath = "/secretserver"

    @keyword
    def connect_to_server_thycotic(
        self, serverFQDN, username, password, appPath="/secretserver"
    ):
        self.username = username
        self.password = password
        self.serverFQDN = serverFQDN
        self.appPath = appPath

        url = "https://{}{}/oauth2/token".format(self.serverFQDN, self.appPath)

        payload = {
            "username": self.username,
            "password": self.password,
            "grant_type": "password",
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        response = requests.request("POST", url, data=payload, headers=headers)

        self.token = json.loads(response.text)["access_token"]

    @keyword
    def getSecretById(self, secretId):
        url = "https://{}{}/api/v1/secrets/{}".format(
            self.serverFQDN, self.appPath, secretId
        )
        headers = {
            "authorization": "Bearer {}".format(self.token),
            "Accept": "application/json",
        }

        response = requests.request("GET", url, headers=headers)

        secret = json.loads(response.text)

        for item in secret["items"]:
            if item["isPassword"]:
                return item["itemValue"]

    @keyword
    def getSearchSecrets(self, searchText):
        searchFilter = "?filter.includeRestricted=true&filter.includeSubFolders=true&filter.searchtext={}".format(
            searchText
        )

        url = "https://{}{}/api/v1/secrets{}".format(
            self.serverFQDN, self.appPath, searchFilter
        )
        headers = {
            "authorization": "Bearer {}".format(self.token),
            "Accept": "application/json",
        }

        response = requests.request("GET", url, headers=headers)

        self.allSecrets = json.loads(response.text)
        listOfSecrets = []
        for secret in self.allSecrets["records"]:
            listOfSecrets.append(secret)
            logger.info("Name={}->ID={}".format(secret["name"], secret["id"]))
        return listOfSecrets
