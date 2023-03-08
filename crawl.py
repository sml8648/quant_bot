# TODO
# 기본적인 재무 정보를 크롤링해서 로직 추가
# 업종간 PER, PBR을 기준으로 종목 선별

import time
import sys
import datetime

from pykrx import stock
from slack_alert import slack_notification

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


    tmp = datetime.date.today()
    today = ''.join(str(tmp).split('-'))

    d1 = datetime.timedelta(days = 1)
    yesterday = ''.join(str(tmp - d1).split('-'))

    df = stock.get_market_ohlcv(today)

    # 장 안열리면 바로 종료
    if not df.iloc[0][0]:
        slack_notification(f'---------- {today} 오늘은 장이 열리지 않습니다. ------------')
        sys.exit(0)

    slack_notification(f'------------- {today} KOSPI 등락률 ---------------')

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

    df = stock.get_market_ohlcv(today, market='KOSDAQ')

    slack_notification(f'------------- {today} KOSDAQ 등락률 ---------------')

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
