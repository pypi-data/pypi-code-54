# -*- coding: utf-8 -*-
__all__ = ["PluginsKanjiStreamTestCase"]
import os
import unittest
from kanjidb.builder.plugins import kanjistream
from kanjidb.encoding import UNICODE_PLUS

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
KANJIS_UTF8_TXT = os.path.join(DATA_DIR, "kanjis_utf8.txt")
KANJIS_UNICODE_TXT = os.path.join(DATA_DIR, "kanjis_unicode.txt")


class PluginsKanjiStreamTestCase(unittest.TestCase):
    def test(self):
        plugin = kanjistream.Plugin()
        config = plugin.required_config
        config.update(
            {
                "encoding": UNICODE_PLUS,
                "separator": ";",
                "in": [KANJIS_UNICODE_TXT],
                "out": "kanjis",
            }
        )

        plugin.configure(global_config={}, plugin_config=config)

        result = plugin()
        print(result)
        self.assertTrue("kanjis" in result, "Invalid output")
        kanjis = result["kanjis"]
        self.assertEqual(kanjis, ["一", "二"], "Invalid result")

    def test_loads(self):
        # UTF8 encoded
        self.assertEqual(kanjistream.loads("一"), ["一"])
        self.assertEqual(kanjistream.loads("一二"), ["一", "二"])
        # With custom separator
        self.assertEqual(kanjistream.loads("一;二", sep=";"), ["一", "二"])
        # Unicode, keep same encoding
        self.assertEqual(
            kanjistream.loads("U+4E00;U4E8C", sep=";"), ["U+4E00", "U4E8C"]
        )
        # Unicode, convert to UTF8
        self.assertEqual(
            kanjistream.loads("U+4E00;U4E8C", encoding=UNICODE_PLUS, sep=";"),
            ["一", "二"],
        )

    def test_load(self):
        # UTF8 encoded
        self.assertEqual(kanjistream.load(KANJIS_UTF8_TXT, sep=";"), ["一", "二"])
        # Unicode
        self.assertEqual(
            kanjistream.load(KANJIS_UNICODE_TXT, encoding=UNICODE_PLUS, sep=";"),
            ["一", "二"],
        )


if __name__ == "__main__":
    unittest.main()
