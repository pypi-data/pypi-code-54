import aiohttp
import sys
import re
import logging
if sys.version_info[0] < 3:
    import urllib2
    import urllib
else:
    import html.parser
    import urllib.request
    import urllib.parse

log = logging.getLogger(__name__)


SPECIAL_CASES = {
    'ee': 'et',
}

agent = {'User-Agent':
         "Mozilla/4.0 (\
                 compatible;\
                 MSIE 6.0;\
                 Windows NT 5.1;\
                 SV1;\
                 .NET CLR 1.1.4322;\
                 .NET CLR 2.0.50727;\
                 .NET CLR 3.0.04506.30\
                 )"}

languages = {
    "ab": "Abkhaz",
    "aa": "Afar",
    "af": "Afrikaans",
    "ak": "Akan",
    "sq": "Albanian",
    "am": "Amharic",
    "ar": "Arabic",
    "an": "Aragonese",
    "hy": "Armenian",
    "as": "Assamese",
    "av": "Avaric",
    "ae": "Avestan",
    "ay": "Aymara",
    "az": "Azerbaijani",
    "bm": "Bambara",
    "ba": "Bashkir",
    "eu": "Basque",
    "be": "Belarusian",
    "bn": "Bengali",
    "bh": "Bihari",
    "bi": "Bislama",
    "bs": "Bosnian",
    "br": "Breton",
    "bg": "Bulgarian",
    "my": "Burmese",
    "ca": "Catalan",
    "ch": "Chamorro",
    "ce": "Chechen",
    "ny": "Nyanja",
    "zh": "Chinese",
    "cv": "Chuvash",
    "kw": "Cornish",
    "co": "Corsican",
    "cr": "Cree",
    "hr": "Croatian",
    "cs": "Czech",
    "da": "Danish",
    "dv": "Divehi",
    "nl": "Dutch",
    "dz": "Dzongkha",
    "en": "English",
    "eo": "Esperanto",
    "et": "Estonian",
    "ee": "Ewe",
    "fo": "Faroese",
    "fj": "Fijian",
    "fi": "Finnish",
    "fr": "French",
    "ff": "Fula",
    "gl": "Galician",
    "ka": "Georgian",
    "de": "German",
    "el": "Greek",
    "gn": "Guarani",
    "gu": "Gujarati",
    "ht": "Haitian",
    "ha": "Hausa",
    "he": "Hebrew",
    "hz": "Herero",
    "hi": "Hindi",
    "ho": "Hiri-Motu",
    "hu": "Hungarian",
    "ia": "Interlingua",
    "id": "Indonesian",
    "ie": "Interlingue",
    "ga": "Irish",
    "ig": "Igbo",
    "ik": "Inupiaq",
    "io": "Ido",
    "is": "Icelandic",
    "it": "Italian",
    "iu": "Inuktitut",
    "ja": "Japanese",
    "jv": "Javanese",
    "kl": "Kalaallisut",
    "kn": "Kannada",
    "kr": "Kanuri",
    "ks": "Kashmiri",
    "kk": "Kazakh",
    "km": "Khmer",
    "ki": "Kikuyu",
    "rw": "Kinyarwanda",
    "ky": "Kyrgyz",
    "kv": "Komi",
    "kg": "Kongo",
    "ko": "Korean",
    "ku": "Kurdish",
    "kj": "Kwanyama",
    "la": "Latin",
    "lb": "Luxembourgish",
    "lg": "Luganda",
    "li": "Limburgish",
    "ln": "Lingala",
    "lo": "Lao",
    "lt": "Lithuanian",
    "lu": "Luba-Katanga",
    "lv": "Latvian",
    "gv": "Manx",
    "mk": "Macedonian",
    "mg": "Malagasy",
    "ms": "Malay",
    "ml": "Malayalam",
    "mt": "Maltese",
    "mi": "M\u0101ori",
    "mr": "Marathi",
    "mh": "Marshallese",
    "mn": "Mongolian",
    "na": "Nauru",
    "nv": "Navajo",
    "nb": "Norwegian Bokm\u00e5l",
    "nd": "North-Ndebele",
    "ne": "Nepali",
    "ng": "Ndonga",
    "nn": "Norwegian-Nynorsk",
    "no": "Norwegian",
    "ii": "Nuosu",
    "nr": "South-Ndebele",
    "oc": "Occitan",
    "oj": "Ojibwe",
    "cu": "Old-Church-Slavonic",
    "om": "Oromo",
    "or": "Oriya",
    "os": "Ossetian",
    "pa": "Panjabi",
    "pi": "P\u0101li",
    "fa": "Persian",
    "pl": "Polish",
    "ps": "Pashto",
    "pt": "Portuguese",
    "qu": "Quechua",
    "rm": "Romansh",
    "rn": "Kirundi",
    "ro": "Romanian",
    "ru": "Russian",
    "sa": "Sanskrit",
    "sc": "Sardinian",
    "sd": "Sindhi",
    "se": "Northern-Sami",
    "sm": "Samoan",
    "sg": "Sango",
    "sr": "Serbian",
    "gd": "Scottish-Gaelic",
    "sn": "Shona",
    "si": "Sinhala",
    "sk": "Slovak",
    "sl": "Slovene",
    "so": "Somali",
    "st": "Southern-Sotho",
    "es": "Spanish",
    "su": "Sundanese",
    "sw": "Swahili",
    "ss": "Swati",
    "sv": "Swedish",
    "ta": "Tamil",
    "te": "Telugu",
    "tg": "Tajik",
    "th": "Thai",
    "ti": "Tigrinya",
    "bo": "Tibetan",
    "tk": "Turkmen",
    "tl": "Tagalog",
    "tn": "Tswana",
    "to": "Tonga",
    "tr": "Turkish",
    "ts": "Tsonga",
    "tt": "Tatar",
    "tw": "Twi",
    "ty": "Tahitian",
    "ug": "Uighur",
    "uk": "Ukrainian",
    "ur": "Urdu",
    "uz": "Uzbek",
    "ve": "Venda",
    "vi": "Vietnamese",
    "vo": "Volapuk",
    "wa": "Walloon",
    "cy": "Welsh",
    "wo": "Wolof",
    "fy": "Western-Frisian",
    "xh": "Xhosa",
    "yi": "Yiddish",
    "yo": "Yoruba",
    "za": "Zhuang",
    "zu": "Zulu"
}


class AsynctrBaseException(Exception):
    """Base class for all asynctr Exceptions"""


class InvalidLanguageException(AsynctrBaseException):
    """Exception raised when a language cannot be found"""


class Translator(object):
    def __init__(self, session: aiohttp.ClientSession = None):
        self.session = session or None

    @staticmethod
    def unescape(text):
        return html.unescape(text)

    async def translate(self, to_translate, to_language="auto", from_language="auto"):
        """
        Main translation command
        :param to_translate:
        :param to_language:
        :param from_language:
        :return: translation result
        """
        if to_language or from_language not in list(languages):
            if to_language and from_language != "auto":
                raise InvalidLanguageException(
                    "Invalid Language Typed! for full list of languages, use the 'get_langs()' function."
                )
            else:
                pass

        base_link = "http://translate.google.com/m?hl=%s&sl=%s&q=%s"
        if sys.version_info[0] < 3:
            to_translate = urllib.quote_plus(self, to_translate)
            link = base_link % (to_language, from_language, to_translate)
            request = urllib2.Request(link, headers=agent)
            raw_data = urllib2.urlopen(request).read()
        else:
            raw_data = await self.Translated.get_data(
                to_translate=to_translate,
                to_language=to_language,
                from_language=from_language
            )
        data = raw_data.decode("utf-8")
        expr = r'class="t0">(.*?)<'
        re_result = re.findall(expr, data)
        if len(re_result) == 0:
            result = ""
        else:
            result = self.unescape(re_result[0])

        translated = self.Translated(result)
        return await translated.ret_result(result, to_language)

    async def close(self):
        if self.session:
            await self.session.close()

    class Translated(object):
        def __init__(self, translated_obj=None, trans_to=None):
            self.translated = translated_obj
            self.translated_to = trans_to

        def __str__(self):
            return "<asynctr.translate.Translator.Translated object, text: {}, language: {}>".format(
                self.translated, self.translated_to)

        @staticmethod
        async def get_data(to_translate, to_language="auto", from_language="auto"):
            base_link = "http://translate.google.com/m?hl=%s&sl=%s&q=%s"
            to_translate = urllib.parse.quote(to_translate)
            link = base_link % (to_language, from_language, to_translate)
            request = urllib.request.Request(link, headers=agent)
            raw_data = urllib.request.urlopen(request).read()
            return raw_data

        @staticmethod
        async def ret_result(res, transto):
            return Translator.Translated(str(res), str(transto))

        def get(self, key):
            if key is None:
                return self.translated
            else:
                if key == 0:
                    return self.translated
                elif key == 1:
                    return self.translated_to
                elif key == "text":
                    return self.translated
                elif key == "lang":
                    return self.translated_to

        @staticmethod
        def get_langs():
            return languages
