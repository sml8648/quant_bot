from pykrx import stock
import datetime

import requests
from bs4 import BeautifulSoup as bs
from tqdm import tqdm, tqdm_pandas

# import concurrent.futures
# import threading

# thread_local = threading.local()

# def crawl_ticker(ticker, session):

#     url = f"https://comp.fnguide.com/SVO2/ASP/SVD_main.asp?pGB=1&gicode=A{ticker}"
#     with session.get(url) as response:

#         try:
#             soup = bs(response.text, "html.parser")
#             per = soup.select('#corp_group2 > dl:nth-child(1) > dd')[0].text
#             category_per = soup.select('#corp_group2 > dl:nth-child(3) > dd')[0].text
#             category = soup.select('#compBody > div.section.ul_corpinfo > div.corp_group1 > p > span.stxt.stxt2')[0].text
#             return per, category_per, category
#         except:
#             return None, None, None

# def crawl_all_ticker(tickers):
    
#     result_list = []
#     with requests.Session() as session:
#         for ticker in tqdm(tickers):
#             per, category_per, category = crawl_ticker(ticker, session)

#             if per == None: continue
#             tmp_list = [per, category_per, category]
#             result_list.append(tmp_list)

#     return result_list

# def crawl_without_thread(tickers):

#     result_list = []

#     for ticker in tqdm(tickers):

#         url = f"https://comp.fnguide.com/SVO2/ASP/SVD_main.asp?pGB=1&gicode=A{ticker}"

#         try:
#             response = requests.get(url)
#             soup = bs(response.text, "html.parser")
#             per = soup.select('#corp_group2 > dl:nth-child(1) > dd')[0].text
#             category_per = soup.select('#corp_group2 > dl:nth-child(3) > dd')[0].text
#             category = soup.select('#compBody > div.section.ul_corpinfo > div.corp_group1 > p > span.stxt.stxt2')[0].text
#             result_list.append([per, category_per, category])

#         except:
#             result_list.append([None, None, None])
    
#     return result_list

# def get_session():
#     if not hasattr(thread_local, "session"):
#         thread_local.session = requests.Session()
#     return thread_local.session

# def crawl_ticker(ticker):
#     session = get_session()

#     url = f"https://comp.fnguide.com/SVO2/ASP/SVD_main.asp?pGB=1&gicode=A{ticker}"
#     with session.get(url) as response:
#         try:
#             soup = bs(response.text, "html.parser")
#             per = soup.select('#corp_group2 > dl:nth-child(1) > dd')[0].text
#             category_per = soup.select('#corp_group2 > dl:nth-child(3) > dd')[0].text
#             category = soup.select('#compBody > div.section.ul_corpinfo > div.corp_group1 > p > span.stxt.stxt2')[0].text
#             return per, category_per, category
#         except:
#             return None, None, None

# def crawl_all_ticker(tickers):

#     with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
#         result = list(tqdm(executor.map(crawl_ticker, tickers), total=len(tickers)))

#     breakpoint()
#     return result

################## multiprocessing ##################################
# import multiprocessing
# import time

# def crawl_ticker(ticker):

#     url = f"https://comp.fnguide.com/SVO2/ASP/SVD_main.asp?pGB=1&gicode=A{ticker}"
#     response = requests.get(url)
#     try:
#         soup = bs(response.text, "html.parser")
#         per = soup.select('#corp_group2 > dl:nth-child(1) > dd')[0].text
#         category_per = soup.select('#corp_group2 > dl:nth-child(3) > dd')[0].text
#         category = soup.select('#compBody > div.section.ul_corpinfo > div.corp_group1 > p > span.stxt.stxt2')[0].text
#         category = category[4:].replace('\xa0','').strip()
#         return ticker, float(per), float(category_per), category
    
#     # FICS  ??????\xa0???\xa0??????
#     except:
#         return ticker, None, None, category

# def crawl_all_ticker(tickers):
#     with multiprocessing.Pool() as pool:
#        result = list(tqdm(pool.map(crawl_ticker, tickers), total=len(tickers)))
#     return result

import time
import pandas as pd
#################### Synchronous #####################################
def crawl_without_thread(tickers):

    result_list = []

    for ticker in tqdm(tickers):

        url = f"https://comp.fnguide.com/SVO2/ASP/SVD_main.asp?pGB=1&gicode=A{ticker}"
        response = requests.get(url)
        try:
            soup = bs(response.text, "html.parser")
            per = soup.select('#corp_group2 > dl:nth-child(1) > dd')[0].text
            category_per = soup.select('#corp_group2 > dl:nth-child(3) > dd')[0].text
            category = soup.select('#compBody > div.section.ul_corpinfo > div.corp_group1 > p > span.stxt.stxt2')[0].text
            category = category[4:].replace('\xa0','').strip()
            result_list.append((ticker, float(per), float(category_per), category))
        
        # FICS  ??????\xa0???\xa0??????
        except:
            result_list.append((ticker, None, None, category))
    
    return result_list

if __name__ == '__main__':

    tmp = datetime.date.today()
    today = ''.join(str(tmp).split('-'))

    d1 = datetime.timedelta(days = 1)
    yesterday = ''.join(str(tmp - d1).split('-'))

    # Thread??? ???????????? ????????? ??? ???????????????...
    # ????????? ????????? ????????? ???????????????.
    df = stock.get_market_fundamental(today)
    df.reset_index(inplace=True)

    result = crawl_without_thread(df['??????'].tolist())

    breakpoint()