# TODO
# 기본적인 재무 정보를 긁어와서 필터링 하기
# 도커 이미지로 만들기
# cloud에 배포 이건 차차 알아보자
# 로깅 추가하기
# 로그를 모으는 연습하기

import time
import sys
import datetime

from pykrx import stock
from slack_alert import slack_notification

def df_to_text(df):

    result_text = "   ".join(['티커','시가','종가','등락률'])
    result_text += '\n'

    # 여기는 나중에 다른 함수로 교체를 해서 시간을 축소할 수 있다.
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
    # TODO 영업일 로직만 넣으면 될듯?

    tmp = datetime.date.today()
    today = ''.join(str(tmp).split('-'))

    d1 = datetime.timedelta(days = 1)
    yesterday = ''.join(str(tmp - d1).split('-'))

    # tickers = stock.get_market_ticker_list(today)
    # df = stock.get_market_fundamental(today)

    df = stock.get_market_ohlcv(today)

    # 장 안열리면 바로 종료
    if not df.iloc[0][0]:
        slack_notification(f'---------- {today} 오늘은 장이 열리지 않습니다. ------------')
        sys.exit(0)

    slack_notification(f'------------- {today} 등락률 ---------------')

    upper_limit = df.loc[df['등락률'] > 20]
    if len(upper_limit):
        slack_notification(" 금일 20% 이상 상승 종목")
        result = df_to_text(upper_limit)
        slack_notification(result)

    high_stock = df.loc[(df['등락률'] >= 10) & (df['등락률'] <= 20)]
    if len(high_stock):
        slack_notification(" 금일 20% 이하 10% 이상 상승 종목")
        result = df_to_text(high_stock)
        slack_notification(result)

    lower_limit = df.loc[df['등락률'] < -20]
    if len(lower_limit):
        slack_notification(" 금일 20% 이상 하락 종목")
        result = df_to_text(lower_limit)
        slack_notification(result)
    
    low_stock = df.loc[(df['등락률'] <= -10) & (df['등락률'] >= -20)]
    if len(low_stock):
        slack_notification(" 금일 10% 이상 20% 이하 하락 종목")
        result = df_to_text(low_stock)
        slack_notification(result)

    slack_notification('-----------------------------------')

    print("test")

# slack 알람까지 했단 말이지 그러면 뭘해야 되냐
# airflow
# 휴일인지 아닌지 판별하기
