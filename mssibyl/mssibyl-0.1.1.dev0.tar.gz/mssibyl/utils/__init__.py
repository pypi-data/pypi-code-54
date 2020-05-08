#!/usr/bin/env python
# encoding: utf-8

from types import SimpleNamespace
from argparse import ArgumentParser



def build_args(args_dict):
    parser = ArgumentParser()
    for k,v in args_dict.items():
        print(k, v)
        parser.add_argument("--{}".format(k), type=type(v))

    parser.add_argument("--aa", type=int, default=1)

    return parser

