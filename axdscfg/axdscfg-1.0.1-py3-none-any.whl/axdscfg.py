
import argparse
import os

from axdscfg.utils import generate_key, encrypt_credentials_file

def main():

    parser = argparse.ArgumentParser(prog='axdscfg',
            description='Credentials from encrypted file package.')

    group = parser.add_mutually_exclusive_group()

    group.add_argument('-e', '--encrypt_key', action='store_true',
            help='Encrypt a file named credentials to credentials.enc')

    group.add_argument('-g', '--gen_key', action='store_true',
            help='Generates a key named axds_cfg.key')

    parser.add_argument('-d', '--dir', default='./',
            help='Specify a custom folder to save')

    args = parser.parse_args()

    config_path = args.dir

    if args.dir and not args.encrypt_key and not args.gen_key:
        print('Use -h for help')

    if args.encrypt_key:
        print('encrypting credentials...')
        config_path = os.path.abspath(config_path)
        encrypt_credentials_file(config_path)

    if args.gen_key:
        print('generating key...')
        config_path = os.path.abspath(config_path)
        generate_key(config_path)
