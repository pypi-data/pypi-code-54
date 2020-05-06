from xingapi.api.xasession import Session
from xingapi.api.xaquery import Query
from xingapi.api.xareal import Real, RealManager

class StockInfo:
    def __init__(self, app=None):
        self.app = app
        self._종목코드 = None
    
    def __call__(self, 종목):
        if self.app:
            if 종목 in self.app.종목코드.전체:
                self._종목코드 = 종목
            else:
                self._종목코드 = self.app.종목코드.종목명으로검색(종목)
        else:
            self._종목코드 = 종목
        return self
    
    @property
    def 현재호가(self):
        return Query('t1101')(shcode=self._종목코드)['t1101OutBlock']

    @property
    def 현재시세(self):
        return Query('t1102')(shcode=self._종목코드)['t1102OutBlock']

    def 체결(self, 특이거래량='', 시작시간='', 종료시간=''):
        """시간대별 체결 조회

            특이거래량: "거래량>특이거래량" 만 조회
            시작시간: HHMMSS 형식
            종료시간: HHMMSS 형식
        """
        return Query('t1301').call(
            shcode=self._종목코드,
            cvolume=특이거래량,
            starttime=시작시간,
            endtime=종료시간,
        ).next(
            keypairs={'cts_time':'cts_time'}
        )['t1301OutBlock1']

    def 분봉(self, 작업구분=0):
        """분별주가 조회

            작업구분(int, str): 0:30초 1:1분 2:3분 3:5분 4:10분 5:30분 6:60분
        """
        return Query('t1302')(shcode=self._종목코드, gubun=작업구분, cnt=900)['t1302OutBlock1']

    def 일봉(self, 개수=-1):
        """일봉

            개수(int): -1: 끝까지, N: N개까지
        """
        return self.t1305(dwmcode=1, cnt=개수)

    def 주봉(self, 개수=-1):
        """주봉
        
            개수(int): -1: 끝까지, N: N개까지
        """
        return self.t1305(dwmcode=2, cnt=개수)

    def 월봉(self, 개수=-1):
        """월봉
        
            개수(int): -1: 끝까지, N: N개까지
        """
        return self.t1305(dwmcode=3, cnt=개수)

    def t1305(self, dwmcode, cnt):
        """기간별주가조회
        """
        if cnt>0:
            total = cnt//300
        else:
            total = -1 # 끝까지

        query = Query('t1305')
        df = query.call(
            shcode=self._종목코드, 
            dwmcode=dwmcode, 
            cnt=300,
        ).next(
            keypairs={'date':'date'}, 
            total=total
        )['t1305OutBlock1']
        return df.head(cnt)

    def __repr__(self):
        return 'Object from StockInfo Class'