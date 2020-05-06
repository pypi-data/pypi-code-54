CLI_CONFIG = {
    "file": {"positional": True,},
    "file_key": {"os": "ACCT_FILE_KEY",},
}
CONFIG = {
    "file": {
        "default": None,
        "help": "The file to encrypt, a new file will be created.",
    },
    "file_key": {
        "default": None,
        "help": "The key to encrypt the file with, if no key is passed a gey will be generated and displayed on after the encrypted file is created",
    },
}
SUBCOMMANDS = {}
DYNE = {
    "acct": ["acct"],
}
