#!/usr/bin/python3

import os
import argparse

# so you don't need to have this installed via pip
import sys
sys.path.append("..")

# can be either pip or local relative dir
from staticfg import CFGBuilder

def main():
    parser = argparse.ArgumentParser(description='Generate the control flow graph of a Python program')
    parser.add_argument('input_file', help='Path to a file containing a Python program for which the CFG must be generated')

    args = parser.parse_args()
    cfg_name = args.input_file.split('/')[-1]
    cfg = CFGBuilder().build_from_file(cfg_name, args.input_file)

    # Some options for wrapping:
    #cfg.build_visual(cfg_name[:-3] + '_cfg', format='pdf', calls=True)
    cfg.build_visual(cfg_name[:-3] + '_cfg', format='png', calls=True, show=False)
    #cfg.build_visual('controlflowgraph', format='png', calls=True, show=False)

    # removes the CFG file, which maybe we could just turn off?
    os.remove(cfg_name[:-3] + '_cfg')

if __name__ == '__main__':
    main()
