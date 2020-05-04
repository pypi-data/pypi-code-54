__all__ = ["Plugin", "load"]
from kanjidb.builder.plugins import PluginBase

try:
    from jamdict.kanjidic2 import Kanjidic2XMLParser
except Exception as e:
    raise Exception("Kanjidic2Plugin requires jamdict to be installed") from e


class Plugin(PluginBase):
    """This plugin load kanjis data from an external Kanjidic2 XML file.

    Kanjidic2 XML file is parsed using `jamdict`.
    """

    @property
    def template_config(self):
        return {"kd2_file": "kd2.xml"}

    @property
    def required_config(self):
        config = self.template_config
        config.update({"in": "kanjis", "out": "db"})

        return config

    def configure(self, **kwargs):
        super().configure(**kwargs)

        data = load(self.plugin_config["kd2_file"])
        print("{} loaded".format(self.plugin_config["kd2_file"]))
        self._kanjis = {_.literal: _ for _ in data.characters}

    def __call__(self, **kwargs):
        """Fill database with Kanjidic2 infos.

        :param db: database
        """
        kanjis = kwargs[self.plugin_config["in"]]

        kwargs[self.plugin_config["out"]] = {_: self.get_infos(_) for _ in kanjis}

        return kwargs

    def get_infos(self, kanji):
        """Get infos from Kanjidic2 for a single kanji.

        :param kanji: kanji to retrieve
        :return: dict containing all infos
        """
        data = self._kanjis[kanji]

        return {
            "stroke_count": data.stroke_count,
            "codepoints": [
                {"type": cp.cp_type, "value": cp.value} for cp in data.codepoints
            ],
            "readings": self.get_readings(kanji),
            "meanings": self.get_meanings(kanji),
        }

    def get_readings(self, kanji):
        data = self._kanjis[kanji].rm_groups[0]

        return [_.to_json() for _ in data.readings]

    def get_meanings(self, kanji):
        data = self._kanjis[kanji].rm_groups[0]

        return [_.to_json() for _ in data.meanings]

    def __repr__(self):
        return "Kanjidic2"


def load(stream):
    """Load a Kanjidic2 XML file using `jamdict`.

    :param stream: filelike object or filename
    :return: data loaded with `jamdict`.
    """
    parser = Kanjidic2XMLParser()
    if hasattr(stream, "read"):
        return parser.parse_str(stream.read())
    else:
        return parser.parse_file(stream)
