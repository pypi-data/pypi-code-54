import re


def getSimilarity(nlp, maxDialogue, minDialogue, start, end):
    wordSnippet = (
        " ".join(re.split("[, ]", maxDialogue))[start : end + 1]
        if end
        else " ".join(re.split("[, ]", maxDialogue)[start:])
    )
    subtitleNLP = nlp(wordSnippet)
    scriptNLP = nlp(minDialogue)
    if not subtitleNLP.vector_norm or not scriptNLP.vector_norm:
        return 0
    similarity = subtitleNLP.similarity(scriptNLP)
    return similarity


def checkIfGoodEnough(
    nlp, scriptContent, subsContent, subsWord, scriptPercent, subsPercent
):
    def getNumberOfSameWords(scriptContent, subsContent):
        count = 0
        for scriptLemma in set(scriptContent["lemma"]):
            for subtitleLemma in set(subsContent["lemma"]):
                if scriptLemma == subtitleLemma:
                    count += 1
        return count

    # number of words in subtitle and screenplay dialogue that's the same
    count = getNumberOfSameWords(subsContent, scriptContent)

    # count of distinct words in both sentences (including unique)
    totalDistinctWordsInBoth = len(set(subsContent["lemma"] + scriptContent["lemma"]))

    # minimum dialogue length between script line and subtitle
    minDialogue = subsContent
    maxDialogue = scriptContent
    if len(scriptContent["lemma"]) < len(subsContent["lemma"]):
        minDialogue = scriptContent
        maxDialogue = subsContent

    isOneWord = "$" in subsWord[-1]

    # if count > 5, that's enough matches to say that its the correct match
    isManyCount = count > 5

    # if words besides unique is not many, than we pass in as a match
    checkCheck = totalDistinctWordsInBoth - count <= len(minDialogue["lemma"])

    def getMaxSimilarity():
        index = 0
        maxSimilarity = 0
        maxIndex = 0

        if index + len(minDialogue["dialogue"]) >= len(maxDialogue["dialogue"]):
            maxSimilarity = getSimilarity(
                nlp, maxDialogue["dialogue"], minDialogue["dialogue"], index, None,
            )
            maxIndex = index

        while index + len(minDialogue["dialogue"]) < len(maxDialogue["dialogue"]):
            similarity = getSimilarity(
                nlp,
                maxDialogue["dialogue"],
                minDialogue["dialogue"],
                index,
                index + len(minDialogue["dialogue"]),
            )
            if similarity > maxSimilarity:
                maxSimilarity = similarity
                maxIndex = index
            index += 1
        if maxSimilarity == 1 and len(minDialogue["dialogue"]) != len(
            maxDialogue["dialogue"]
        ):
            maxSimilarity = 0.99
        return (maxSimilarity, maxIndex)

    maxSimilarity, maxIndex = getMaxSimilarity()

    goodEnoughPercent = abs(scriptPercent - subsPercent) <= 0.10

    return (
        (
            isOneWord
            or isManyCount
            or checkCheck
            or (goodEnoughPercent and maxSimilarity >= 0.90)
        ),
        maxSimilarity,
        maxIndex,
    )


def getMatchingDistinctWords(nlp, scriptDistinct, subsDistinct, script, subs):
    """
    - traverses subsDistinct and scriptDistinct until there's a matching unique word.
    - The occurrence of the word in subtitles may be less than the occurrence of word in script, or vice versa.
    """
    matchingUniqueWords = []

    for subsWord, subsValue in subsDistinct.items():
        for scriptWord, scriptValue in scriptDistinct.items():
            scriptContentNoDuplicate = list(
                filter(lambda x: "##" not in x["dialogue"], scriptValue["content"])
            )
            if subsWord == scriptWord and len(subsValue["content"]) == len(
                scriptContentNoDuplicate
            ):
                takenScript = {}
                takenSubs = {}

                for scriptIndex, scriptContent in enumerate(scriptContentNoDuplicate):

                    scriptPercent = scriptContent["index"] / len(script)
                    for subsIndex, subsContent in enumerate(subsValue["content"]):
                        subsPercent = subsContent["timestamp"][0] / (
                            subs[-1]["start"].seconds - subs[0]["start"].seconds
                        )
                        if abs(scriptPercent - subsPercent) >= 0.15:
                            continue
                        if scriptIndex in takenScript and abs(
                            subsPercent - scriptPercent
                        ) >= abs(
                            takenScript[scriptIndex]["percent"]
                            - takenSubs[takenScript[scriptIndex]["subs"]]["percent"]
                        ):
                            continue
                        if subsIndex in takenSubs and abs(
                            subsPercent - scriptPercent
                        ) >= abs(
                            takenScript[takenSubs[subsIndex]["script"]]["percent"]
                            - takenSubs[subsIndex]["percent"]
                        ):
                            continue

                        goodEnough, maxSimilarity, maxIndex = checkIfGoodEnough(
                            nlp,
                            scriptContent,
                            subsContent,
                            subsWord,
                            scriptPercent,
                            subsPercent,
                        )

                        # if match already made for current subtitle OR current script, then
                        # don't bother considering current script<->subtitle match-
                        if (
                            scriptIndex in takenScript
                            and takenScript[scriptIndex]["similarity"] > maxSimilarity
                            or subsIndex in takenSubs
                            and takenSubs[subsIndex]["similarity"] > maxSimilarity
                        ):
                            continue

                        if goodEnough:
                            if scriptIndex in takenScript:
                                matchingUniqueWords[-1]["content"][-1] = {
                                    "timestamp": subsContent["timestamp"],
                                    "index": scriptValue["content"][scriptIndex][
                                        "index"
                                    ],
                                    "subsDialogue": subsContent["dialogue"],
                                    "matchIndex": maxIndex,
                                }
                            elif (
                                len(matchingUniqueWords) > 0
                                and matchingUniqueWords[-1]["word"] == subsWord
                            ):

                                matchingUniqueWords[-1]["content"].append(
                                    {
                                        "timestamp": subsContent["timestamp"],
                                        "index": scriptValue["content"][scriptIndex][
                                            "index"
                                        ],
                                        "subsDialogue": subsContent["dialogue"],
                                        "matchIndex": maxIndex,
                                    }
                                )
                            else:
                                matchingUniqueWords.append(
                                    {
                                        "word": subsWord,
                                        "content": [
                                            {
                                                "timestamp": subsValue["content"][
                                                    subsIndex
                                                ]["timestamp"],
                                                "index": scriptValue["content"][
                                                    scriptIndex
                                                ]["index"],
                                                "subsDialogue": subsValue["content"][
                                                    subsIndex
                                                ]["dialogue"],
                                                "matchIndex": maxIndex,
                                            }
                                        ],
                                    }
                                )

                            takenSubs[subsIndex] = {
                                "percent": subsPercent,
                                "similarity": maxSimilarity,
                                "script": scriptIndex,
                            }
                            takenScript[scriptIndex] = {
                                "percent": scriptPercent,
                                "similarity": maxSimilarity,
                                "subs": subsIndex,
                            }

    return matchingUniqueWords
