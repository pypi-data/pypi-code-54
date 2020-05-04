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

        path = fileremoto
        x = path.split("/")
        x.pop()
        if(len(x) > 0):
            carpeta = ''
            for value in x:
                valorfinal = value.translate(
                    {ord(c): "" for c in "\\/:*?\"<>|."})
                if valorfinal != '':
                    carpeta = carpeta+"/"+valorfinal

            if carpeta != '':
                self.mkdir('Compartida', carpeta)

        self.server.storeFile(sharename, fileremoto, data)
        return True

    def download(self, sharename, filelocal, fileremoto):
        path = filelocal
        x = path.split("/")
        x.pop()
        if(len(x) > 1):
            carpeta = './'
            for value in x:
                valorfinal = value.translate(
                    {ord(c): "" for c in "\\/:*?\"<>|."})
                if valorfinal != '':
                    carpeta = carpeta+"/"+valorfinal
                    os.mkdir(carpeta)

        with open(filelocal, "wb+") as fo:
            self.server.retrieveFile(sharename, fileremoto, fo)
            fo.close()
        return filelocal

    def delete(self, sharename, fileremoto):
        self.server.deleteFiles(sharename, fileremoto)

    def list(self, sharename):
        filelist = self.server.listPath(sharename, '/')
        return filelist

    def mkdir(self, sharename, path):
        x = path.split("/")
        if(len(x) > 1):
            carpeta = ''
            for value in x:
                valorfinal = value.translate(
                    {ord(c): "" for c in "\\/:*?\"<>|."})
                if valorfinal != '':

                    carpeta = carpeta+"/"+valorfinal
                    self.server.createDirectory(sharename, carpeta)
        else:
            self.server.createDirectory(sharename, path)
