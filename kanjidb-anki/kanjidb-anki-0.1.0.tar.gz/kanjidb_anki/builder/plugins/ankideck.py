# -*- coding: utf-8 -*-
__all__ = ["Plugin"]
import genanki
from kanjidb.builder.plugins import PluginBase


class Plugin(PluginBase):
    """This plugin generate an Anki deck from database.

    This plugin require genanki to generate Anki decks.
    """

    @property
    def template_config(self):
        return {"output": "ankideck.apkg", "deck_id": 1, "title": "AnkiDeck"}

    @property
    def required_config(self):
        config = self.template_config
        config.update({"in": "db", "only": "kanjis"})

        return config

    def __call__(self, **kwargs):
        db = kwargs[self.plugin_config["in"]]
        only_kanjis = kwargs[self.plugin_config["only"]]

        model = genanki.Model(
            1607392319,
            "Simple Model",
            fields=[{"name": "Question"}, {"name": "Answer"},],
            templates=[
                {
                    "name": "Card 1",
                    "qfmt": "{{Question}}",
                    "afmt": '{{FrontSide}}<hr id="answer">{{Answer}}',
                }
            ],
        )

        deck = genanki.Deck(
            int(self.plugin_config["deck_id"]), self.plugin_config["title"]
        )

        notes = [generate_note(_, db.get(_, None), model) for _ in only_kanjis]
        for _ in notes:
            deck.add_note(_)

        genanki.Package(deck).write_to_file(self.plugin_config["output"])

    def __repr__(self):
        return "AnkiDeck"


def generate_note(kanji, data, model):
    return genanki.Note(
        model=model,
        fields=[
            kanji,
            "\n".join("{}: {}".format(_["type"], _["value"]) for _ in data["readings"]),
        ],
    )
