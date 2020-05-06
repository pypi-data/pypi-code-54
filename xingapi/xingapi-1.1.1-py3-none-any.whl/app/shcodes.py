from xingapi.api.xasession import Session
from xingapi.api.xaquery import Query
from xingapi.api.xareal import Real, RealManager

class StockCodes:
    def __init__(self):
        pass

    @property
    def 전체(self):
        return self.t8430(gubun=0)

    @property
    def 코스피(self):
        return self.t8430(gubun=1)

    @property
    def 코스닥(self):
        return self.t8430(gubun=2)

    @property
    def 관리대상(self):
        return self.t1404(jongchk=1)

    @property
    def 불성실공시(self):
        return self.t1404(jongchk=2)

    @property
    def 투자유의(self):
        return self.t1404(jongchk=3)

    @property
    def 투자환기(self):
        return self.t1404(jongchk=4)

    @property
    def 투자경고(self):
        return self.t1405(jongchk=1)

    @property
    def 매매정지(self):
        return self.t1405(jongchk=2)

    @property
    def 정리매매(self):
        return self.t1405(jongchk=3)

    @property
    def 투자주의(self):
        return self.t1405(jongchk=4)

    @property
    def 투자위험(self):
        return self.t1405(jongchk=5)

    @property
    def 위험예고(self):
        return self.t1405(jongchk=6)

    @property
    def 단기과열(self):
        return self.t1405(jongchk=7)

    @property
    def 단기과열예고(self):
        return self.t1405(jongchk=8)

    @property
    def 초저유동성(self):
        return self.t1410()

    @property
    def 증거금100(self):
        return self.t1411(jongchk=1, jkrate=100)

    @property
    def 당일상한가(self):
        return self.t1422(jnilgubun=0, sign=1)

    @property
    def 당일하한가(self):
        return self.t1422(jnilgubun=0, sign=4)

    @property
    def 전일상한가(self):
        return self.t1422(jnilgubun=1, sign=1)

    @property
    def 전일하한가(self):
        return self.t1422(jnilgubun=1, sign=4)

    @property
    def 시가총액상위순(self):
        return self.t1444()

    def t8430(self, gubun):
        df = Query('t8430')(gubun=0)['t8430OutBlock']
        if gubun == 0:
            return df['단축코드'].to_list()
        elif gubun == 1:
            return df[df['구분(1:코스피2:코스닥)']=='1']['단축코드'].to_list()
        elif gubun == 2:
            return df[df['구분(1:코스피2:코스닥)']=='2']['단축코드'].to_list()

    def t1404(self, jongchk):
        df = Query('t1404').call(gubun=0, jongchk=jongchk).next(keypairs={'cts_shcode':'cts_shcode'})['t1404OutBlock1']
        if df.empty: return []
        return df['종목코드'].to_list()

    def t1405(self, jongchk):
        df = Query('t1405').call(gubun=0, jongchk=jongchk).next(keypairs={'cts_shcode':'cts_shcode'})['t1405OutBlock1']
        if df.empty: return []
        return df['종목코드'].to_list()

    def t1410(self):
        df = Query('t1410').call(gubun=0).next(keypairs={'cts_shcode':'cts_shcode'})['t1410OutBlock1']
        if df.empty: return []
        return df['종목코드'].to_list()

    def t1411(self, jongchk, jkrate):
        df = Query('t1411').call(gubun=0, jongchk=jongchk, jkrate=jkrate).next(keypairs={'idx':'idx'})['t1411OutBlock1']
        if df.empty: return []
        return df['종목코드'].to_list()

    def t1422(self, jnilgubun, sign):
        df = Query('t1422')(qrygb=2, gubun=0, jnilgubun=jnilgubun, sign=sign)['t1422OutBlock1']
        if df.empty: return []
        return df['종목코드'].to_list()

    def t1444(self):
        df = Query('t1444').call(upcode='000').next(keypairs={'idx':'idx'})['t1444OutBlock1']
        if df.empty: return []
        return df['종목코드'].to_list()

    def __repr__(self):
        return 'Shcodes class instance'