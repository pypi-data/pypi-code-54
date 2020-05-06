# -*- coding: utf-8 -*-

from test.api_v1 import Build


class TestBuild:
    sample_data = {
        "git_repo": "https://github.com/torvalds/linux.git",
        "git_ref": "master",
        "target_arch": "x86",
        "toolchain": "gcc-9",
        "kconfig": ["allyesconfig"],
    }

    def test_key_is_based_on_input(self):
        b1 = Build.put(None, self.sample_data)
        b2 = Build.put(None, self.sample_data)
        assert b1["build_key"] == b2["build_key"]
