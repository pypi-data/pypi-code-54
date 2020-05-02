


def tagTimestampToScript(pureScript, scriptWithTimestamp):
    index = 0
    for pageIndex, page in enumerate(pureScript):
        for contentIndex, content in enumerate(page["content"]):
            if "scene_info" in content:
                for sceneIndex, scene in enumerate(content["scene"]):
                    if scene["type"] == "CHARACTER" or scene["type"] == "DUAL_DIALOGUE":

                        testDialogues = ""
                        if scene["type"] == "DUAL_DIALOGUE":
                            testDialogues = [
                                scene["content"]["character1"]["dialogue"],
                                scene["content"]["character2"]["dialogue"],
                            ]
                        else:
                            testDialogues = [scene["content"]["dialogue"]]

                        for line in scriptWithTimestamp:
                            if (
                                any(
                                    [
                                        line["dialogue"]
                                        in " ".join(
                                            list(
                                                filter(
                                                    lambda x: "(" != x[0], testDialogue,
                                                )
                                            )
                                        ).lower()
                                        for testDialogue in testDialogues
                                    ]
                                )
                                and "timestamp" in line
                            ):
                                pureScript[pageIndex]["content"][contentIndex]["scene"][
                                    sceneIndex
                                ]["timestamp"] = line["timestamp"]
    return pureScript