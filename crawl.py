import time
import sys
import datetime
import multiprocessing

from pykrx import stock
from pykrx import bond

from slack_alert import slack_notification

class StockCrawl:

    def __init__(self):
        tmp = datetime.date.today()
        self.today = ''.join(str(tmp).split('-'))

        d1 = datetime.timedelta(days = 1)
        self.yesterday = ''.join(str(tmp - d1).split('-'))

        df = stock.get_market_ohlcv(self.yesterday, self.today, "005930")
        if len(df) != 2:
            print("Today is not the day the market open")
            sys.exit()
        else:
            print("Today is the day the market open")

    def get_ticker(self):
        tickers = stock.get_market_ticker_list()
        return tickers

    def get_stock_data(self, tickers):

        num = 1000

        for each_ticker in tickers[:num]:
            try:
                df = stock.get_market_ohlcv(self.yesterday, self.today, each_ticker)
                print(df)
            except:
                continue
        print("This passsed", end_time - start_time)

# 이것도 존나 어려운거였네

# def get_ohlcv(args):

#     try:
#         yesterday = args[0]
#         today = args[1]
#         ticker = args[2]

#         df = stock.get_market_ohlcv(yesterday, today, ticker)
#         print(df)
#     except:
#         pass

# TODO
# 주가 정보를 불러와서 특정 기준이 넘으면 리턴 하는 건데
# 그 로직들을 봐야지
# 상한가인 친구들 탐지
# 하한가인 친구들 탐지
# 20퍼 내외의 등락을 하는 친구 탐지
# PER, PBR이 괜찮은 친구 탐지
# 기본적인 재무 정보를 긁어와서 필터링 하기
# 업종까지 크롤링 해주면 좋은데 왜 안해주는건지 ㅋㅋ 알아보자 # 네이버 금융에 있네
# 볼린저 밴드

# 도커 이미지로 만들기
# cloud에 배포 이건 차차 알아보자
# 로깅 추가하기
# 로그를 모으는 연습하기

def df_to_text(df):

    result_text = "   ".join(['티커','시가','종가','등락률'])
    result_text += '\n'

    ticker = [stock.get_market_ticker_name(each) for each in df.index.tolist()]
    start_price = df['시가'].tolist()
    end_price = df['종가'].tolist()
    fluc_rate = df['등락률'].tolist()

    for a,b,c,d in zip(ticker, start_price, end_price, fluc_rate):
        
        tmp = '   '.join([a, str(b), str(c), str(round(d,2)) ])
        tmp += '\n'
        result_text += tmp
    
    return result_text

if __name__ == '__main__':

    # 오늘 날짜 얻기
    # TODO 공휴일을 어떻게 볼건지

    tmp = datetime.date.today()
    today = ''.join(str(tmp).split('-'))

    d1 = datetime.timedelta(days = 1)
    yesterday = ''.join(str(tmp - d1).split('-'))

    df = stock.get_market_ohlcv(today)

    # 맨처음에 정보를 받아오면 좋겠는데
    upper_limit = df.loc[df['등락률'] > 20]
    if len(upper_limit):
        result = df_to_text(upper_limit)
        slack_notification(result)

    high_stock = df.loc[(df['등락률'] >= 10) & (df['등락률'] <= 20)]
    if len(high_stock):
        result = df_to_text(high_stock)
        slack_notification(result)

    lower_limit = df.loc[df['등락률'] < -29]
    if len(lower_limit):
        result = df_to_text(lower_limit)
        slack_notification(result)
    
    low_stock = df.loc[(df['등락률'] <= -10) & (df['등락률'] >= -20)]
    if len(low_stock):
        result = df_to_text(low_stock)
        slack_notification(result)

    # # low_stock = df.loc[(df['등락률'] <= -10) & (df['등락률'] >= -20)]
    # slack_notification("안녕안녕\t오늘의 종목이야")

    # check today is the day the market opens
    # 너무 많이 콜을 하면 에러가 나나 보다
    # 이부분은 내가 라이브러리를 보고 수정하자
    # df = stock.get_market_ohlcv(yesterday, today, "005930")
    # breakpoint()
    # if len(df) != 2:
    #     print("Today is not the day the market open")
    #     sys.exit()
    # else:
    #     print("Today is the day the market open")

    # # Start crawl the stock marke data
    # # TODO 따로 빼서 저장해놓기 너무 오래 걸림
    # tickers = stock.get_market_ticker_list()

    # num = 1000

    # start_time = time.time()
    # pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    # pool.map(get_ohlcv, zip([yesterday]*num, [today]*num, tickers[:num]))
    # pool.close()
    # pool.join()
    # end_time = time.time()

    # print("This passsed", end_time - start_time)

    # start_time = time.time()
    # for each_ticker in tickers[:num]:
    #     try:
    #         df = stock.get_market_ohlcv(yesterday, today, each_ticker)
    #         print(df)
    #     except:
    #         continue
    # end_time = time.time()
    # print("This passsed", end_time - start_time)
