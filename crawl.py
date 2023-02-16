import time
import sys
import datetime
import multiprocessing

from pykrx import stock
from pykrx import bond

def get_ohlcv(args):

    try:
        yesterday = args[0]
        today = args[1]
        ticker = args[2]

        df = stock.get_market_ohlcv(yesterday, today, ticker)
        print(df)
    except:
        pass

if __name__ == '__main__':

    # 오늘 날짜 얻기
    # TODO 공휴일을 어떻게 볼건지
    tmp = datetime.date.today()
    today = ''.join(str(tmp).split('-'))

    d1 = datetime.timedelta(days = 1)
    yesterday = ''.join(str(tmp - d1).split('-'))

    # check today is the day the market opens
    # 너무 많이 콜을 하면 에러가 나나 보다
    # 이부분은 내가 라이브러리를 보고 수정하자
    df = stock.get_market_ohlcv(yesterday, today, "005930")
    if len(df) != 2:
        print("Today is not the day the market open")
        sys.exit()
    else:
        print("Today is the day the market open")

    # Start crawl the stock marke data
    # TODO 따로 빼서 저장해놓기 너무 오래 걸림
    tickers = stock.get_market_ticker_list()

    num = 1000

    start_time = time.time()
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    pool.map(get_ohlcv, zip([yesterday]*num, [today]*num, tickers[:num]))
    pool.close()
    pool.join()
    end_time = time.time()

    print("This passsed", end_time - start_time)

    # start_time = time.time()
    # for each_ticker in tickers[:num]:
    #     try:
    #         df = stock.get_market_ohlcv(yesterday, today, each_ticker)
    #         print(df)
    #     except:
    #         continue
    # end_time = time.time()
    # print("This passsed", end_time - start_time)
