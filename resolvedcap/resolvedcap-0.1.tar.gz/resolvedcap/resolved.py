import requests
from time import sleep
from http import cookiejar

class BlockAll(cookiejar.CookiePolicy):
    return_ok = set_ok = domain_return_ok = path_return_ok = lambda self, *args, **kwargs: False
    netscape = True
    rfc2965 = hide_cookie2 = False

s = requests.Session()
s.cookies.set_policy(BlockAll())

def resss(key):
    url = 'http://2captcha.com/in.php'
    files = {'file': open('.\\captcha.png', 'rb')}
    data = {'key': key, 'method': 'post'}
    r = requests.post(url, files=files, data=data)
    captcha_id = r.text.split('|')[1]
    print(captcha_id)
    recaptcha_answer = s.get("http://2captcha.com/res.php?key={}&action=get&id={}".format(key, captcha_id)).text
    print("\nsolving captcha.. ")
    while 'CAPCHA_NOT_READY' in recaptcha_answer:
        sleep(2)
        recaptcha_answer = s.get("http://2captcha.com/res.php?key={}&action=get&id={}".format(key, captcha_id)).text
        sleep(1)

    recaptcha_answer = recaptcha_answer.split('|')[1]
    return recaptcha_answer