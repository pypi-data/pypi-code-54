

def str2hex(text):
    if type(text) == int:
        return text
    elif type(text) == str:
        value = 0
        for i in text:
            iv = ord(i)
            if (iv >= 97) and (iv <= 102): # a ~ f
                iv = iv - 97 + 10
                value = (value << 4) + iv
            elif (iv >= 65) and (iv <= 70): # A ~ F
                iv = iv - 65 + 10
                value = (value << 4) + iv
            elif (iv >= 0x30) and (iv <= 0x39):
                iv = iv - 0x30
                value = (value << 4) + iv
        return value
    elif type(text) == list:
        ls = []
        for cell in text:
            d = str2hex(cell)
            ls = ls.append(d)
        return ls
    else:
        print ('Invalid dtype')
        return 0

if __name__ == '__main__':
    i = str2hex('0x123456789abcdef0123')
    print(str(i) + ' = ' +  hex(i))
    if i == 5373003642731685151011:
        print('str2hex Test Pass')
    else:
        print('str2hex Test Fail')
