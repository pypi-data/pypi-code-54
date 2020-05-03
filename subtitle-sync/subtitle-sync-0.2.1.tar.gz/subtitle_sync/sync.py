from __future__ import unicode_literals, print_function
import json
import re
import argparse
import copy

import srt
import spacy
from pysbd.utils import PySBDFactory

from subtitle_sync.formatText import formatSubs, formatScript
from subtitle_sync.markScriptWithRareWordsTimestamp import (
    markScriptWithRareWordsTimestamp,
)
from subtitle_sync.utils.furtherSyncScript import furtherSyncScript
from subtitle_sync.utils.traverseDialogue import traverseDialogue
from subtitle_sync.utils.tagTimestampToScript import tagTimestampToScript
from subtitle_sync.utils.fillTimetamps import fillTimestamps


def sync(moviePath, subsPath):
    subtitle = open(subsPath, "r")
    subtitle = list(srt.parse(subtitle.read()))

    script = open(moviePath, "rb")
    script = json.load(script)
    pureScript = copy.copy(script)

    nlp = spacy.load("en_core_web_lg")

    # explicitly adding component to pipeline
    # (recommended - makes it more readable to tell what's going on)
    nlpSentece = spacy.blank("en")
    nlpSentece.add_pipe(PySBDFactory(nlpSentece))

    custom_lookup = {
        "til": "until",
    }

    def change_lemma_property(doc):
        for token in doc:
            if token.text in custom_lookup:
                token.lemma_ = custom_lookup[token.text]
        return doc

    nlp.add_pipe(change_lemma_property, first=True)

    subtitle = formatSubs(nlpSentece, subtitle)
    script = formatScript(nlpSentece, script)

    (
        script,
        scriptWithTimestamp,
        subsWithTimestamp,
    ) = markScriptWithRareWordsTimestamp(nlp, script, subtitle)

    pureScript = tagTimestampToScript(pureScript, scriptWithTimestamp)

    prevTimestamp = {"timestamp": [0, 0]}
    index = 0
    while index < len(scriptWithTimestamp):
        content = scriptWithTimestamp[index]
        if (
            "timestamp" in content
            and prevTimestamp["timestamp"][1] - (content["timestamp"][1]) > 50
        ):
            print("------")
            print(prevTimestamp)
            print()
            print(content)
            print("------")
            if (
                prevTimestamp["timestamp"][1]
                < scriptWithTimestamp[index]["timestamp"][1]
            ):
                del content["timestamp"]

            else:
                del prevTimestamp["timestamp"]
        if "timestamp" in content:
            prevTimestamp = content
        index += 1

    pureScript = fillTimestamps(pureScript)

    return pureScript


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse Screenplay PDF into JSON")

    parser.add_argument(
        "-m",
        metavar="screenplay",
        type=str,
        help="screenplay json path",
        required=True,
    )

    parser.add_argument(
        "-s", metavar="subs", type=str, help="subtitle json path", required=True,
    )

    # start from skipPage set up by user.  default to 0
    args = parser.parse_args()
    moviePath = args.m
    subsPath = args.s
    scriptWithTimestamp = sync(moviePath, subsPath)
    file0 = open("timestamped.json", "w+")
    json.dump(scriptWithTimestamp, file0, indent=4, ensure_ascii=False)
