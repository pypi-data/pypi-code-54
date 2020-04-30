
from axdscfg.exceptions import ConfigFileNotFoundError, \
    KeyFileNotFoundError

import nacl.secret
from os.path import isfile
from configparser import RawConfigParser

# Arquivo de chave de criptografia
KEY_FILE = '/axds_cfg.key'
# Arquivo de senhas criptografadas
PASSWORD_FILE = '/credentials.enc'

class Credentials():
    CUSTOM_CONFIG_PATH = None
    CRYPT_KEY = None
    params = None

    # Se os arquivos de configuração estiverem em outro diretório,
    #    o diretório deverá ser passado na chamada da classe
    def __init__(self, config_path):
        if config_path.endswith('/') and len(config_path) >= 2:
            config_path = config_path.rstrip('/')

        self.CUSTOM_CONFIG_PATH = config_path
        self.CRYPT_KEY = self.CUSTOM_CONFIG_PATH + KEY_FILE

        if not isfile(self.CRYPT_KEY):
            raise KeyFileNotFoundError

        PARAMS_FILE = self.CUSTOM_CONFIG_PATH + PASSWORD_FILE

        if not isfile(PARAMS_FILE):
            raise ConfigFileNotFoundError

        self.params = self.__read_config(PARAMS_FILE)

    def __read_config(self, p_file):
        config_parser = RawConfigParser()

        # Chamada da função de decriptação
        config_file_binary = self.__decrypt_file(self.CRYPT_KEY, p_file)

        config_parser.read_string(config_file_binary.decode('utf-8'))
        return config_parser

    def __decrypt_file(self, key_file, in_filename):
        """ Decrypts a file using PyNaCl Secret Box.
            The method uses a key file to decrypt the credentials file.
        """
        with open(key_file, 'rb') as infile:
            key = infile.read()

        box = nacl.secret.SecretBox(key)

        with open(in_filename, 'rb') as infile:
            credentials_file_binary = box.decrypt(infile.read())

        return credentials_file_binary

    def get_config_param(self, param_section, param_key):
        return self.params.get(param_section, param_key)
