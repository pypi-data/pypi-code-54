import re
import json

from subtitle_sync.utils.traverseDialogue import traverseDialogue
from subtitle_sync.utils.removeStopWords import (
    extractLemmaScript,
    extractLemmaSubs,
)
from subtitle_sync.utils.getMatchingDistinctWords import getMatchingDistinctWords


def getDistinctWordsSubs(subsLemma):
    distinctWords = {}
    for subtitle in subsLemma:
        for lemmaWord in subtitle["lemma"]:
            if len(lemmaWord) <= 2:
                continue
            distinctWords.setdefault(
                lemmaWord, {"count": 0, "content": []},
            )
            distinctWords[lemmaWord]["count"] += 1
            distinctWords[lemmaWord]["content"].append(
                {
                    "lemma": subtitle["lemma"],
                    "dialogue": subtitle["content"],
                    "timestamp": (subtitle["start"], subtitle["end"]),
                }
            )
    distinctWords = {k: v for k, v in distinctWords.items() if v["count"] <= 3}
    return distinctWords


def getDistinctWordsScript(scriptLemma):
    distinctWords = {}
    for index, section in enumerate(scriptLemma):
        for lemmaWord in section["lemma"]:
            if len(lemmaWord) <= 2:
                continue
            distinctWords.setdefault(lemmaWord, {"count": 0, "content": [],})
            distinctWords[lemmaWord]["count"] += 1
            distinctWords[lemmaWord]["content"].append(
                {
                    "lemma": section["lemma"],
                    "dialogue": section["dialogue"],
                    "index": index,
                }
            )
    distinctWords = {k: v for k, v in distinctWords.items() if v["count"] <= 3}
    return distinctWords


def getDistinctWordsTimestampScript(script, matchingDistinct):
    for matchingDistinctWord in matchingDistinct:
        for content in matchingDistinctWord["content"]:
            if (
                "timestamp" in script[content["index"]]
                and max(
                    script[content["index"]]["timestamp"][0], content["timestamp"][0]
                )
                - min(script[content["index"]]["timestamp"][1], content["timestamp"][1])
                < 20
            ):
                startTime = min(
                    script[content["index"]]["timestamp"][0], content["timestamp"][0]
                )
                endTime = max(
                    script[content["index"]]["timestamp"][1], content["timestamp"][1]
                )
                script[content["index"]]["timestamp"] = [startTime, endTime]
            else:
                script[content["index"]]["timestamp"] = content["timestamp"]
            script[content["index"]]["distinct"] = content
    return script


def getDistinctWordsTimestampSubs(subsLemma, subsDistinct):
    for subtitle in subsLemma:
        for word in subtitle["lemma"]:
            if word in subsDistinct:
                if "distinct" in subtitle:
                    subtitle["distinct"].append(word)
                else:
                    subtitle["distinct"] = [word]
    return subsLemma


def markScriptWithRareWordsTimestamp(nlp, script, subs):
    """
    1. remove stopwords from subtitle, and then get distinct words from them
    2. same thing for script
    3. get word matches between distinct words in script and subs
    4. tag timestamps of distinct words into the script
    """
    subsLemma = extractLemmaSubs(nlp, subs)
    subsDistinct = getDistinctWordsSubs(subsLemma)

    scriptLemma = extractLemmaScript(nlp, script)
    scriptDistinct = getDistinctWordsScript(scriptLemma)

    matchingDistinct = getMatchingDistinctWords(
        nlp, scriptDistinct, subsDistinct, script, subs
    )

    scriptDistinctTimestamp = getDistinctWordsTimestampScript(
        scriptLemma, matchingDistinct
    )
    subsDistinctTimestamp = getDistinctWordsTimestampSubs(subsLemma, subsDistinct)

    # file0 = open("subHelp.json", "w+")
    # json.dump(subsDistinct, file0, indent=4)
    # file0 = open("scriptHelp.json", "w+")
    # json.dump(scriptDistinct, file0, indent=4)
    # file0 = open("matchingHelp.json", "w+")
    # json.dump(matchingDistinct, file0, indent=4)
    # file0 = open("test.json", "w+")
    # json.dump(scriptDistinctTimestamp, file0, indent=4)

    return (script, scriptDistinctTimestamp, subsDistinctTimestamp)
