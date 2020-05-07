"""
from pykakasi import kakasi
from pypinyin import pinyin, Style


k2h = kakasi()  # Kanji to Hiragana
k2h.setMode('J', 'H')
h2r = kakasi()  # Hiragana to Romaji
h2r.setMode('H', 'a')  # Hiragana to ascii
h2r.setMode('K', 'a')  # Katakana
h2r.setMode('s', True)  # add space
h2r.setMode('C', True)  # capitalize, default: no capitalize
k2hc = k2h.getConverter()
h2rc = h2r.getConverter()


def detect_lang(text):
    for char in text:
        if '\u3000' <= char <= '\u30ff' or '\uff00' <= char <= '\uffef':
            return 'Japanese'
        if '\u3400' <= char <= '\u9fff':
            return 'Chinese'  # characters
    return False


def format_romaji(romaji):
    romaji.replace('  ', ' ')
    romaji.replace('ei', 'e').replace('ei', 'e')


def convert(text, lang='Japanese'):
    if lang == 'Japanese':
        result = ''
        hinagana = k2hc.do(text)
        romaji = h2rc.do(hinagana).split(' ')
        for i in romaji:
            result += i[:1].upper()
    elif lang == 'Chinese':
        result = ''
        for char in pinyin(text, style=Style.FIRST_LETTER):
            result += ''.join(char)
        return result.upper()
"""


demo = {
    '田所': 'TDKR',
    '多田': 'TD',
    # Combination first
    '野': 'Y',
    '獣': 'J',
    '先': 'SN',
    '輩': 'PI',
    '田': 'T',
    '所': 'TKR',
    '浩': 'K',
    '二': 'J',
    '多': 'T',
    '數': 'KZ',
    '人': 'HT',
}


def tdn_demo(text):
    for i in demo:
        text = text.replace(i, demo[i])
    return text
