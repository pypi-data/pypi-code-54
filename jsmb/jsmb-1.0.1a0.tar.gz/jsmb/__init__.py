import tempfile
from smb.SMBConnection import SMBConnection
import socket
import logging
import os


class jsmb(object):
    def __init__(self, ip, username, password):
        self.ip = ip
        self.username = username
        self.password = password

        self.server = SMBConnection(self.username, self.password, self.username, self.ip, self.ip, use_ntlm_v2=True,
                                    sign_options=SMBConnection.SIGN_WHEN_SUPPORTED,
                                    is_direct_tcp=True)
        self.server.connect(self.ip, 445)

    def upload(self, sharename, filelocal, fileremoto):
        data = open(filelocal, 'rb')
        file = '/' + fileremoto
        self.server.storeFile(sharename, file, data)
        return "file has been uploaded"

    def download(self, sharename, file, fileremoto):
        tempPath = os.path.realpath(file)
        with open(tempPath, "wb+") as fo:
            self.server.retrieveFile(sharename, fileremoto, fo)
            fo.close()
        return tempPath

    def delete(self, sharename, fileremoto):
        self.server.deleteFiles(sharename, fileremoto)

    def list(self, sharename):
        filelist = self.server.listPath(sharename, '/')
        return filelist
