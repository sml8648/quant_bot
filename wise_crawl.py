# # 에너지
# https://www.wiseindex.com/Index/GetIndexComponets?ceil_yn=0&dt=20230303&sec_cd=G10
# https://www.wiseindex.com/Index/GetIndexComponets?ceil_yn=0&dt=20230303&sec_cd=G1010
# # 소재
# https://www.wiseindex.com/Index/GetIndexComponets?ceil_yn=0&dt=20230303&sec_cd=G1510

# # 자본재
# https://www.wiseindex.com/Index/GetIndexComponets?ceil_yn=0&dt=20230303&sec_cd=G2010

# # 상업서비스와공급품
# https://www.wiseindex.com/Index/GetIndexComponets?ceil_yn=0&dt=20230303&sec_cd=G2020

# # 운송
# https://www.wiseindex.com/Index/GetIndexComponets?ceil_yn=0&dt=20230303&sec_cd=G2030

# # 자동차와부품
# https://www.wiseindex.com/Index/GetIndexComponets?ceil_yn=0&dt=20230303&sec_cd=G2510

# # 내구소비재와의류
# https://www.wiseindex.com/Index/GetIndexComponets?ceil_yn=0&dt=20230303&sec_cd=G2520

# # 호텔, 레스토랑, 레저등
# https://www.wiseindex.com/Index/GetIndexComponets?ceil_yn=0&dt=20230303&sec_cd=G2530

# # 소매(유통)
# https://www.wiseindex.com/Index/GetIndexComponets?ceil_yn=0&dt=20230303&sec_cd=G2550

# # 교육서비스
# https://www.wiseindex.com/Index/GetIndexComponets?ceil_yn=0&dt=20230303&sec_cd=G2560

# # 식품과기본식료품소매
# https://www.wiseindex.com/Index/GetIndexComponets?ceil_yn=0&dt=20230303&sec_cd=G3010

# # 식품, 음료, 담배
# https://www.wiseindex.com/Index/GetIndexComponets?ceil_yn=0&dt=20230303&sec_cd=G3020

# # 가정용품과개인용품
# https://www.wiseindex.com/Index/GetIndexComponets?ceil_yn=0&dt=20230303&sec_cd=G3030

# # 건강관리장비와 서비스
# https://www.wiseindex.com/Index/GetIndexComponets?ceil_yn=0&dt=20230303&sec_cd=G3510

# # 제약과생물공학
# https://www.wiseindex.com/Index/GetIndexComponets?ceil_yn=0&dt=20230303&sec_cd=G3520

# # 은행
# https://www.wiseindex.com/Index/GetIndexComponets?ceil_yn=0&dt=20230303&sec_cd=G4010

# # 증권
# https://www.wiseindex.com/Index/GetIndexComponets?ceil_yn=0&dt=20230303&sec_cd=G4020

# # 다각화된금융
# https://www.wiseindex.com/Index/GetIndexComponets?ceil_yn=0&dt=20230303&sec_cd=G4030

# # 보험
# https://www.wiseindex.com/Index/GetIndexComponets?ceil_yn=0&dt=20230303&sec_cd=G4040

# # 부동산
# https://www.wiseindex.com/Index/GetIndexComponets?ceil_yn=0&dt=20230303&sec_cd=G4050

# # 소프트웨어와서비스
# https://www.wiseindex.com/Index/GetIndexComponets?ceil_yn=0&dt=20230303&sec_cd=G4510

# # 기술하드웨어와장비
# https://www.wiseindex.com/Index/GetIndexComponets?ceil_yn=0&dt=20230303&sec_cd=G4520

# # 반도체와반도체장비
# https://www.wiseindex.com/Index/GetIndexComponets?ceil_yn=0&dt=20230303&sec_cd=G4530

# # 전자와 전기제품
# https://www.wiseindex.com/Index/GetIndexComponets?ceil_yn=0&dt=20230303&sec_cd=G4535

# # 디스플레이
# https://www.wiseindex.com/Index/GetIndexComponets?ceil_yn=0&dt=20230303&sec_cd=G4540

# # 전기통신서비스
# https://www.wiseindex.com/Index/GetIndexComponets?ceil_yn=0&dt=20230303&sec_cd=G5010

# # 미디어와엔터테인먼트
# https://www.wiseindex.com/Index/GetIndexComponets?ceil_yn=0&dt=20230303&sec_cd=G5020

# # 유틸리티
# https://www.wiseindex.com/Index/GetIndexComponets?ceil_yn=0&dt=20230303&sec_cd=G5510
import datetime
import requests
from bs4 import BeautifulSoup as bs

sec_cd = [10, 1010, 1510, 2010, 2020, 2030, 2510, 2520, 2530, 2550, 2560, 3010, 3020, 3030, 3510, 3520, 4010, 4020, 4030, 4040, 4050, 4510, 4520, 4530, 4535, 4540, 5010, 5020, 5510]

if __name__ == '__main__':

    tmp = datetime.date.today()
    today = ''.join(str(tmp).split('-'))

    d1 = datetime.timedelta(days = 1)
    yesterday = ''.join(str(tmp - d1).split('-'))

    sample = '20230303'

    ticker_category_dict = []
    for each in sec_cd:

        response = requests.get(f"https://www.wiseindex.com/Index/GetIndexComponets?ceil_yn=0&dt={sample}&sec_cd=G{each}")

        for k in response.json()['list']:

            try:
                tmp = {k['CMP_KOR']:k['SEC_NM_KOR']}
                ticker_category_dict.append(tmp)
            except:
                breakpoint()

    breakpoint()