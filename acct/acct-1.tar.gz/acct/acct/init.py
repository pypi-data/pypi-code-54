# Import third party libs
from cryptography.fernet import Fernet
import yaml
import msgpack


def __init__(hub):
    # Remember not to start your app in the __init__ function
    # This function should just be used to set up the plugin subsystem
    # Add another function to call from your run.py to start the app
    hub.pop.sub.load_subdirs(hub.acct, recurse=True)


def cli(hub):
    hub.pop.config.load(["acct"], cli="acct")
    key = hub.OPT["acct"]["file_key"]
    fn = hub.OPT["acct"]["file"]
    ret = hub.acct.init.encrypt(fn, key)
    print(ret["msg"])


def encrypt(hub, fn, key=None):
    ret = {}
    print_key = False
    if key is None:
        print_key = True
        key = Fernet.generate_key()
    f = Fernet(key)
    tfn = f"{fn}.fernet"
    with open(fn, "rb") as rfh:
        data = yaml.safe_load(rfh.read())
    with open(tfn, "wb+") as wfh:
        wfh.write(f.encrypt(msgpack.dumps(data)))
    ret["msg"] = f"New encrypted file created at: {tfn}\n"
    if print_key:
        ret["msg"] += f"The file was encrypted with this key:\n{key}"
    return ret
