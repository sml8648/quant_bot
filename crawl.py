# TODO
# 기본적인 재무 정보를 크롤링해서 로직 추가
# 업종간 PER, PBR을 기준으로 종목 선별

import time
import sys
import datetime

from pykrx import stock
from slack_alert import slack_notification
from category import get_ticker2
import pandas as pd
from fn_guide_crawl import *

def df_to_text(df):

    result_text = "   ".join(['종목명','시가','종가','등락률'])
    result_text += '\n'

    ticker = df['ISU_ABBRV'].tolist()
    start_price = df['시가'].tolist()
    end_price = df['종가'].tolist()
    fluc_rate = df['등락률'].tolist()
    tob = df['업종'].tolist()

    for a,b,c,d,e in zip(ticker, start_price, end_price, fluc_rate,tob):

        try:
            tmp = '   '.join([a, str(b), str(c), str(round(d,2)), str(e)])
            tmp += '\n'
            result_text += tmp
        except:
            breakpoint()
    
    return result_text

if __name__ == '__main__':

    tmp = datetime.date.today()
    today = ''.join(str(tmp).split('-'))

    d1 = datetime.timedelta(days = 1)
    yesterday = ''.join(str(tmp - d1).split('-'))

    df = stock.get_market_ohlcv(today)[['시가','고가','저가','종가','등락률']]
    df.reset_index(inplace=True)

    df2 = get_ticker2().fetch(today, 'KOSPI')
    df2 = df2[['ISU_SRT_CD','KIND_STKCERT_TP_NM','ISU_ABBRV']]

    df = pd.merge(df,df2, left_on='티커', right_on='ISU_SRT_CD', how='inner')
    
    df = df.loc[df['KIND_STKCERT_TP_NM'] == '보통주'].reset_index(drop=True)

    result = crawl_all_ticker(df['티커'].tolist())
    result = pd.DataFrame(result, columns=['티커','PER','업종PER','업종'])

    df = pd.merge(df,result, left_on='티커', right_on='티커', how='inner')

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

    df = df.loc[~df['PER'].isna()]
    df['PER_DIV'] = df['PER'] / df['업종PER']
    df = df.sort_values(by=['PER_DIV'], ascending=True)

    # Decorator로 대체 가능할듯
    slack_notification(" 업종PER 기준 매우 낮은 종목")
    result = df_to_text(df.head(10))
    slack_notification(result)

    breakpoint()

    # df = stock.get_market_ohlcv(today, market='KOSDAQ')[['시가','고가','저가','종가','등락률']]
    # df.reset_index(inplace=True)

    # df2 = get_ticker2().fetch(today, 'KOSDAQ')
    # df2 = df2[['ISU_SRT_CD','KIND_STKCERT_TP_NM','ISU_ABBRV']]

    # df = pd.merge(df,df2, left_on='티커', right_on='ISU_SRT_CD', how='inner')
    
    # df = df.loc[df['KIND_STKCERT_TP_NM'] == '보통주'].reset_index(drop=True)

    # result = crawl_all_ticker(df['티커'].tolist())
    # result = pd.DataFrame(result, columns=['티커','PER','업종PER','업종'])

    # df = pd.merge(df,result, left_on='티커', right_on='티커', how='inner')

    # slack_notification(f'------------- {today} KOSDAQ 등락률 ---------------')

    # upper_limit = df.loc[df['등락률'] > 20]
    # if len(upper_limit):
    #     slack_notification(" 금일 20% 이상 상승 종목")
    #     result = df_to_text(upper_limit)
    #     slack_notification(result)

    # high_stock = df.loc[(df['등락률'] >= 10) & (df['등락률'] <= 20)]
    # if len(high_stock):
    #     slack_notification(" 금일 20% 이하 10% 이상 상승 종목")
    #     result = df_to_text(high_stock)
    #     slack_notification(result)

    # lower_limit = df.loc[df['등락률'] < -20]
    # if len(lower_limit):
    #     slack_notification(" 금일 20% 이상 하락 종목")
    #     result = df_to_text(lower_limit)
    #     slack_notification(result)
    
    # low_stock = df.loc[(df['등락률'] <= -10) & (df['등락률'] >= -20)]
    # if len(low_stock):
    #     slack_notification(" 금일 10% 이상 20% 이하 하락 종목")
    #     result = df_to_text(low_stock)
    #     slack_notification(result)

    # slack_notification('-----------------------------------')
