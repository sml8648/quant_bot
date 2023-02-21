import requests
from abc import abstractmethod
import pandas as pd
from pandas import DataFrame

market2mktid = {
        "ALL": "ALL",
        "KOSPI": "STK",
        "KOSDAQ": "KSQ",
        "KONEX": "KNX"
    }

class Get:
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0"}

    def read(self, **params):
        resp = requests.get(self.url, headers=self.headers, params=params)
        return resp

    @property
    @abstractmethod
    def url(self):
        return NotImplementedError


class Post:
    def __init__(self, headers=None):
        self.headers = {"User-Agent": "Mozilla/5.0"}
        if headers is not None:
            self.headers.update(headers)

    def read(self, **params):
        resp = requests.post(self.url, headers=self.headers, data=params)
        return resp

    @property
    @abstractmethod
    def url(self):
        return NotImplementedError

class KrxWebIo(Post):
    def read(self, **params):
        params.update(bld=self.bld)
        resp = super().read(**params)
        return resp.json()

    @property
    def url(self):
        return "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd"

    @property
    @abstractmethod
    def bld(self):
        return NotImplementedError

    @bld.setter
    def bld(self, val):
        pass

    @property
    @abstractmethod
    def fetch(self, **params):
        return NotImplementedError

class 전종목시세(KrxWebIo):
    @property
    def bld(self):
        return "dbms/MDC/STAT/standard/MDCSTAT01501"

    def fetch(self, trdDd: str, mktId: str) -> DataFrame:
        result = self.read(mktId=market2mktid[mktId], trdDd=trdDd)
        return DataFrame(result['OutBlock_1'])

class get_ticker(KrxWebIo):
    @property
    def bld(self):
        return "dbms/MDC/STAT/standard/MDCSTAT03901"

    def fetch(self, trdDd: str, mktId: str) -> DataFrame:
        result = self.read(mktId=market2mktid[mktId], trdDd=trdDd)
        return DataFrame(result['block1'])

if __name__ == '__main__':

    df = get_ticker().fetch('20230221','KOSPI')

    breakpoint()

    print(df)