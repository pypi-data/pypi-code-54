#!/usr/bin/env python3
# Copyright (c) 2020, Stefan Grönke
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted providing that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
import os
import sys
from .Changelog import Changelog

def run(*args):
    changelog = Changelog()

    percent_encoded = ("--percent-encode" in args)
    bump_version = ("--bump-version" in args)
    show_version_only = ("--version-only" in args)

    if "--version" in args:
        if bump_version is True:
            print("--version cannot be used with --bump-version")
            exit(1)
        _index = args.index("--version")
        version = args[_index + 1]
    elif bump_version is True:
        try:
            version = changelog.bump()
        except Exception as e:
            print(str(e).strip("\""), file=sys.stderr)
            exit(1)
    else:
        print(" ".join([
            f"Usage: {sys.argv[0]}",
            "--version (latest|<semver>|UNRELEASED)",
            "[--percent-encode]",
            "[--version-only]"
        ]))
        exit(1)

    try:
        if str(version) == "latest":
            section = changelog.versions[0]
        else:
            section = changelog.get_version(version)
    except KeyError as e:
        print(str(e).strip("\""), file=sys.stderr)
        exit(1)

    if section is None:
        exit(1)
    else:
        if show_version_only is True:
            print(str(section.version))
        elif percent_encoded is True:
            print(section.percent_encoded)
        else:
            print(str(section))

def main():
    run(*sys.argv[1:])

if __name__ == "__main__":
    main()
