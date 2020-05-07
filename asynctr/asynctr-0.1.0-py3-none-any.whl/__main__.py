from __future__ import absolute_import
import asynctr
import sys

USAGE = ("""Name: mou_translator
Usage:
$ async google translate text_to_translate to_lang from_lang
from_lang is optional
Example:
$ asynctr "bonjour" en
Hello
""")


def main():
    if len(sys.argv) < 3:
        print(USAGE)
        return 1
    text = sys.argv[1]
    dest = sys.argv[2]
    if len(sys.argv) > 3:
        src = sys.argv[3]
    else:
        src = "auto"
    translator = asynctr.Translator()
    print(translator.translate(text, dest, src))
    return 0


if __name__ == '__main__':
    main()
