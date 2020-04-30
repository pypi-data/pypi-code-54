
from os.path import isfile

from axdscfg.exceptions import ConfigFileNotFoundError, \
    KeyFileNotFoundError

import nacl.secret
import nacl.utils

# Arquivo de chave de criptografia
KEY_FILE = '/axds_cfg.key'
# Arquivo de senhas criptografadas
CREDENTIALS_FILE = '/credentials'
PASSWORD_FILE = '/credentials.enc'

def generate_key(key_path):
    if key_path.endswith('/') and len(key_path) >= 2:
        key_path = key_path.rstrip('/')

    key_file = key_path + KEY_FILE

    key = nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)
    with open(key_file, 'wb') as outfile:
        outfile.write(key)

def encrypt_credentials_file(config_path):
    if config_path.endswith('/') and len(config_path) >= 2:
        config_path = config_path.rstrip('/')

    if not isfile(config_path + KEY_FILE):
        raise KeyFileNotFoundError

    with open(config_path + KEY_FILE, 'rb') as infile:
        key = infile.read()

    box = nacl.secret.SecretBox(key)

    credentials_infile = config_path + CREDENTIALS_FILE
    if not isfile(credentials_infile):
        raise ConfigFileNotFoundError

    credentials_outfile = config_path + PASSWORD_FILE
    with open(credentials_infile, 'rb') as infile:
        with open(credentials_outfile, 'wb') as outfile:
            outfile.write(box.encrypt(infile.read()))
