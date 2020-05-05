import os

from prutils.pr_dmhelper import DMHelper
from prutils.pr_requests import downloadfile, downloadfile_session
from prutils.pr_utils import get_timestamp13, md5


class YDLoginer():
    def __init__(self, s, username, password, work_dir):
        self.vcode_im_path =  os.path.join(work_dir, "login_vcode.jpg")
        self.s = s
        self.password = password
        self.username = username

    def is_logined(self):
        url = "https://note.youdao.com/yws/mapi/user?method=get&vendor=&multilevelEnable=true"
        r = self.s.get(url)
        return r.status_code == 200

    def get_vcode_im_url(self):
        url = "https://note.youdao.com/login/acc/urs/verify/get?product=YNOTE&width=80&height=32&rc=0.%s" % get_timestamp13()
        return url

    def update_download_vcode_im(self):
        downloadfile_session(self.s, self.get_vcode_im_url(), self.vcode_im_path)
        return self.vcode_im_path

    def do_login(self, vcode=""):
        url = "https://note.youdao.com/login/acc/urs/verify/check"
        params = {
            "app": "web",
            "product": "YNOTE",
            "tp": "urstoken",
            "cf": "6",
            "fr": "1",
            "systemName": "Windows",
            "deviceType": "WindowsPC",
            "ru": "https://note.youdao.com/signIn//loginCallback.html",
            "er": "https://note.youdao.com/signIn//loginCallback.html",
            "vcode": vcode,
            "timestamp": get_timestamp13()
        }
        data = {
            "username": self.username,
            "password": md5(self.password.encode())
        }
        r = self.s.post(url, params=params, data=data)
        if "ecode" in r.url:
            return False
        return True

    def login(self):
        if not self.is_logined():
            if not self.do_login():
                dm = DMHelper()
                dm.dialog(self.update_download_vcode_im(), self.update_download_vcode_im, self.do_login)
            assert(self.is_logined())