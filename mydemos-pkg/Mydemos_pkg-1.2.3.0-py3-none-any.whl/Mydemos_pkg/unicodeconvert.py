def nonBMPtoBMP(up):
    u=ord(up)
    vc = u - 0x10000
    vh = (vc & 0xFFC00) >>10
    vl = vc & 0x3FF
    w1 = 0xD800
    w2 = 0xDC00
    w1 = w1|vh
    w2 = w2|vl
    return chr(w1)+chr(w2)
import unicodedata
def UnicodetoASCII(s):
    return unicodedata.normalize('NFKD',s).encode('ascii','ignore')
def ASCIItoUnicode(s):
    return chr(ord(s))
