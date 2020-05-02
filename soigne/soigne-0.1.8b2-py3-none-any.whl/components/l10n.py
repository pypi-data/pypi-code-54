#!/usr/bin/env python
# coding=utf-8

from os import listdir as scan_languages_dir

import configparser


def __(phrase, *args):
    return Translation.translate(phrase, args)


class Language:
    DEFAULT = 'ru'

    _data = None

    name = ''
    locale = ''
    phrases = {}

    def __init__(self, locale, data):
        self.locale = locale
        self._data = data

        self.name = self._data['language']['name']

        self._load_phrases()
        pass

    def _load_phrases(self):
        """ Сохраняет фразу в списке фраз языка.
        """
        for phrase in self._data.items('phrases'):
            self.phrases[phrase[0]] = phrase[1]

        pass

    def get_phrases(self):
        return self.phrases


class Translation:
    """ Переводчик.
    Хранит список языков, список фраз выбранного языка,
    переводит необходимые фразы.
    """

    dir = ''
    languages = {}
    language = Language

    _parser = None

    def __init__(self, lang_dir, lang):
        self._parser = configparser.ConfigParser()

        self.dir = lang_dir

        self.load_languages()
        self.select_language(lang)
        pass

    @staticmethod
    def translate(phrase, args):
        if phrase not in Translation.language.phrases:
            return phrase

        return Translation.language.phrases.get(phrase)

    def load_languages(self):
        for lang in scan_languages_dir(self.dir):
            self.load_language(lang)

        pass

    def load_language(self, lang):
        """ Добавляет словарь фраз по локали в глобальный спсиок фраз.
        """
        # Читаем файл языка
        self._parser.read(self.dir + lang)

        # Добавляем язык в переводчик.
        lang = lang.replace('.ini', '')
        self.languages[lang] = Language(lang, self._parser)

        pass

    def select_language(self, lang):
        """ Выбираем указанный язык.
        """
        if lang not in self.languages:
            raise RuntimeError('Unknown language <' + lang + '>.')

        self.language = self.languages[lang]
        pass
