from typing import List

from deckz.builder import Builder
from deckz.config import get_config
from deckz.paths import Paths
from deckz.targets import Targets


def run(
    paths: Paths,
    build_handout: bool,
    build_presentation: bool,
    build_print: bool,
    target_whitelist: List[str],
) -> None:
    config = get_config(paths)
    targets = Targets(paths=paths, fail_on_missing=True, whitelist=target_whitelist)
    Builder(
        config,
        paths,
        targets,
        build_handout=build_handout,
        build_presentation=build_presentation,
        build_print=build_print,
    )
