from xingapi.api.xasession import Session
from xingapi.api.xaquery import Query
from xingapi.api.xareal import Real, RealManager

from xingapi.app.shcodes import StockCodes

class App:
    session = Session()
    query = None
    real = None

    def __init__(self, login_txt=None, *login_args, **login_kwargs):
        """app instance 시작            
        """

        if login_txt:
            self.login_from_txt(login_txt)
        elif login_args:
            self.login(*login_args)
        elif login_kwargs:
            self.login(**login_kwargs)

        self.종목코드 = StockCodes()

    def login(self, id, pw, cert):
        self.session.login(id, pw, cert)

    def login_from_txt(self, txt_path):
        with open(txt_path) as f:
            id, pw, cert = f.read().split()
        self.login(id, pw, cert)