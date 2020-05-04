HTFW=65248
def HalfToFullWidth(s):
    '''
    This is for like 'ａ'to'a'.
    '''
    try:
        sn=ord(s)+HTFW
        temptp_1_1=chr(sn)
    except:
        raise UnicodeEncodeError("this is not a fullwidth alpha.")
    finally:
        pass
    
    return chr(sn)
def FullToHalfWidth(s):
    '''
    This is for like 'a'to'ａ'.
    '''
    try:
        sn=ord(s)-HTFW
        temptp_1_1=chr(sn)
    except:
        raise UnicodeEncodeError("this is not a fullwidth alpha.")
    finally:
        pass
    return chr(sn)
