import copy


def nestedShit(pureScript, fill, prevPageIndex, prevContentIndex, prevSceneIndex):
    while prevPageIndex < len(pureScript):
        page = pureScript[prevPageIndex]
        while prevContentIndex < len(page["content"]):
            content = page["content"][prevContentIndex]
            if "scene_info" in content:
                while prevSceneIndex < len(content["scene"]):
                    scene = content["scene"][prevSceneIndex]
                    # stuff to do
                    if "timestamp" in scene:
                        return pureScript
                    else:
                        if (
                            scene["type"] != "ACTION"
                            or (
                                len(scene["content"]) > 1
                                or (
                                    len(scene["content"]) == 1
                                    and "CONTINUED" not in scene["content"][0]["text"]
                                )
                            )
                        ) and (
                            scene["type"] != "TRANSITION"
                            or scene["type"] == "TRANSITION"
                            and "CONTINUED" not in scene["content"]["text"]
                        ):
                            scene["duration"] = fill
                        else:
                            scene["duration"] = 0.0

                    prevSceneIndex += 1
                prevSceneIndex = 0
            else:
                content["duration"] = fill
            prevContentIndex += 1
        prevContentIndex = 0
        prevPageIndex += 1
    return pureScript


def fillTimestamps(pureScript):
    startTimestamp = [0, 0]
    countInBetween = 0

    prevPageIndex = 0
    prevContentIndex = 0
    prevSceneIndex = 0

    pageIndex = 0
    while pageIndex < len(pureScript):
        page = pureScript[pageIndex]
        contentIndex = 0
        if "type" in page and page["type"] == "FIRST_PAGES":
            pageIndex += 1
            countInBetween += len(page["content"])
            continue
        while contentIndex < len(page["content"]):
            sceneIndex = 0
            content = page["content"][contentIndex]
            while sceneIndex < len(content["scene"]):
                scene = content["scene"][sceneIndex]
                # stuff to do
                if (
                    scene["type"] == "ACTION"
                    and "CONTINUED" in scene["content"][0]["text"]
                ):
                    x = 0

                if "timestamp" in scene:
                    fill = scene["timestamp"][0] - startTimestamp[1]
                    fill = fill / countInBetween if countInBetween > 0 else 0

                    scene["duration"] = scene["timestamp"][1] - scene["timestamp"][0]

                    if countInBetween > 0:
                        pureScript = nestedShit(
                            pureScript,
                            fill,
                            prevPageIndex,
                            prevContentIndex,
                            prevSceneIndex,
                        )

                    firstTimestamp = (
                        True
                        if startTimestamp[0] == 0 and startTimestamp[1] == 0
                        else False
                    )
                    startTimestamp = copy.copy(scene["timestamp"])
                    # if not firstTimestamp:
                    #     del scene["timestamp"]

                    countInBetween = 0
                    prevPageIndex = pageIndex
                    prevContentIndex = contentIndex
                    prevSceneIndex = sceneIndex + 1
                elif (
                    scene["type"] != "ACTION"
                    or (
                        len(scene["content"]) > 1
                        or (
                            len(scene["content"]) == 1
                            and "CONTINUED" not in scene["content"][0]["text"]
                        )
                    )
                ) and (
                    scene["type"] != "TRANSITION"
                    or (
                        scene["type"] == "TRANSITION"
                        and "CONTINUED" not in scene["content"]["text"]
                    )
                ):
                    countInBetween += 1

                sceneIndex += 1
            contentIndex += 1
        pageIndex += 1
    return pureScript
