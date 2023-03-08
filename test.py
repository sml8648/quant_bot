# TODO
# WISE Crawl
# Naver financial crawl using thread or multiprocess

from pykrx import stock
import datetime

import requests
from bs4 import BeautifulSoup as bs
from tqdm import tqdm, tqdm_pandas
tqdm_pandas(tqdm())

def category_parse(ticker):

    try:
        page = requests.get(f"https://finance.naver.com/item/main.naver?code={ticker}")
        soup = bs(page.text, "html.parser")
        elements = soup.select('#content > div.section.trade_compare > h4 > em > a')
        return elements[0].text
    except:
        return None

if __name__ == '__main__':

    tmp = datetime.date.today()
    today = ''.join(str(tmp).split('-'))

    d1 = datetime.timedelta(days = 1)
    yesterday = ''.join(str(tmp - d1).split('-'))

    df = stock.get_market_fundamental(today)
    df.reset_index(inplace=True)

    df['category'] = df['티커'].progress_apply(category_parse)

    breakpoint()

    
    


    