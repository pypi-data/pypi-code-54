#!/usr/bin/python3

import time
import yaml
import sys

def build(story, speed=4, repeat=1, force=False):

    stream = open(story, 'r')
    story = yaml.safe_load(stream)
    build = {
        "states": [],
        "env": {},
        "repeat": repeat,
        "speed": speed
    }

    if 'env' in story:
        build["env"] = story["env"]

    if 'repeat' in story and force is False:
        try:
            build["repeat"] = int(story["repeat"])
        except TypeError: pass

    if 'speed' in story and force is False:
        try:
            build["speed"] = int(story["speed"])
        except TypeError: pass

    if build["speed"] > 10:
        build["speed"] = 10
    elif build["speed"] < 0:
        build["speed"] = 0

    bundle = None
    if 'states' in story:
        build["states"] = []
        for states in story['states']:
            for state in states:
                bundle = states[state]
                for key in bundle:
                    bundle[key] = bundle[key].format(**build["env"])
                build["states"].append(bundle)

    print(build["speed"], build["repeat"])
    return build

def run(build):
    cursor = -1
    for a in range(0,len(build["states"]) * build["repeat"]):
        if cursor >= len(build["states"]) - 1:
            cursor = 0
        else:
            cursor = cursor + 1
        print(chr(27) + "[2J")
        for key in build["states"][cursor]:
            print(build["states"][cursor][key])
        time.sleep((11-build["speed"])/10)

def cli_storii():
    speed = 4  # default value
    repeat = 3  # default value
    force = False
    try:
        speed = int(sys.argv[2])
        force = True
    except:pass
    try:
        repeat = int(sys.argv[3])
        force = True
    except:pass
    try:
        b = build(sys.argv[1], speed=speed, repeat=repeat, force=force)
        run(b)
    except IndexError:
        print("no file provided")
    except FileNotFoundError:
        print("file not found")

if __name__ == '__main__':
    cli_storii()
