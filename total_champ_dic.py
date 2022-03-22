import requests
from bs4 import BeautifulSoup

def create_soup(url):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36", "Accept-Language": "ko"}
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    return soup

def champ_dic():
    total_champ_dic=dict()
    url = 'https://www.op.gg/champions'
    soup = create_soup(url)
    champ_list = soup.find("nav", attrs={'class':'css-pqbqz6 e1n0mtzi8'}).findChildren('a', recursive=False)
    for champ in champ_list:
        total_champ_dic[champ.img['alt']] = champ['href']
        
    dic_update = {
    '갱플': '갱플랭크',
    '그라': '그라가스',
    '글가': '그라가스',
    '그브': '그레이브즈', 
    '궨': '그웬',
    '노틸': '노틸러스',
    '누누': '누누와 윌럼프',
    '다리': '다리우스', 
    '드븐': '드레이븐',
    '리산': '리산드라',
    '마이': '마스터 이', 
    '마오': '마오카이',
    '말파': '말파이트',
    '모데': '모데카이저', 
    '몰가': '모르가나',
    '문도': '문도 박사',
    '미포': '미스 포츈',
    '볼베': '볼리베어',
    '블미': '블라디미르',
    '블라디': '블라디미르',
    '블츠': '블리츠크랭크', 
    '블크': '블리츠크랭크', 
    '블리츠': '블리츠크랭크', 
    '삐뽀': '뽀삐',
    '사일': '사일러스',
    '세주': '세주아니',
    '짜오': '신 짜오',
    '쓸쉬': '쓰레쉬',
    '무무': '아무무',
    '솔': '아우렐리온 솔',
    '아우솔': '아우렐리온 솔',
    '아아번': '아이번',
    '아트': '아트록스',
    '아펠': '아펠리오스',
    '알리': '알리스타',
    '과학': '야스오',
    '오리': '오리아나',
    '수학': '요네', 
    '워웍': '워윅',
    '이렐': '이렐리아', 
    '이즈': '이즈리얼',
    '일라': '일라오이',
    '자르반': '자르반 4세',
    '카시': '카시오페아',
    '카타': '카타리나',
    '칼리': '칼리스타', 
    '케틀': '케이틀린',
    '킨드': '킨드레드',
    '켄치': '탐 켄치',
    '트타': '트리스타나',
    '트린': '트린다미어',
    '트페': '트위스티드 페이트',
    '피들': '피들스틱',
    '딩거': '하이머딩거',
    '하딩': '하이머딩거'
    }

    for key, value in dic_update.items():
        total_champ_dic[key] = total_champ_dic[value]

    return total_champ_dic