import os
import discord
from discord.ext import commands
from gtts import gTTS
from io import BytesIO
from FFmpegPCMAudioGTTS import FFmpegPCMAudioGTTS
import requests
from bs4 import BeautifulSoup
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller 
from io import BytesIO
from total_champ_dic import *
import laftel

bot = commands.Bot(command_prefix='')

# 로그인
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name) # 토큰으로 로그인 된 bot 객체에서 discord.User 클래스를 가져온 뒤 name 프로퍼티를 출력
    print(bot.user.id) # 위와 같은 클래스에서 id 프로퍼티 출력
    print('------')

    # 상태창 '~하는 중'
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("업데이트"))


# 음성채널 입장        
@bot.command()
async def join(ctx):
    try:
        # if ctx.message.channel.name == '일반': #id is globally unique
        author = ctx.message.author
        channel = author.voice.channel
        await channel.connect()
        await ctx.send("ㄷㄷㄷㅈ")
        print("음성채널 입장 완료")
    except Exception as e:
        print("[Join에서 에러]", e)

# 음성채널 퇴장
@bot.command()
async def leave(ctx):
    try:
        await ctx.voice_client.disconnect()
        print("음성채널 퇴장 완료")
    except Exception as e:
        print("[Leave 함수에서 에러]", e)

# TTS
@bot.command(name="0")
async def _1(ctx, *, text=None):
    try:
        if len(text) > 50:
            await ctx.send('너무 긴 텍스트는 읽어드리지 않아요')
            raise Exception
        mp3_fp = BytesIO()
        tts = gTTS(text=text, lang='ko')
        tts.write_to_fp(mp3_fp)
        vc = ctx.guild.voice_client
        mp3_fp.seek(0)
        vc.play(FFmpegPCMAudioGTTS(mp3_fp.read(), pipe=True), after=print("Done"))
    except Exception as e:
        print("[TTS 함수에서 에러]", e)

# 코인 현재가
@bot.command(name="가즈아")
async def _1(ctx, *, text="비트코인"):
    try:
        url = "https://api.upbit.com/v1/market/all"
        querystring = {"isDetails":"false"}
        headers = {"Accept": "application/json"}
        response = requests.request("GET", url, headers=headers, params=querystring).json()
        dic = list(filter(lambda x: x["korean_name"] == text, response))
        dic = list(filter(lambda x: x["market"][0:3] == "KRW", dic))
        ticker = dic[0]['market']
        print(ticker)
        new_url = "https://api.upbit.com/v1/ticker?markets="+ticker
        response = requests.request("GET", new_url, headers=headers, params=querystring)
        price = int(response.json()[0]['trade_price'])
        voiceline = "{}..아직 {}원인데요??".format(text, price)
        await ctx.send(voiceline)

        mp3_fp = BytesIO()
        tts = gTTS(text=voiceline, lang='ko')
        tts.write_to_fp(mp3_fp)
        vc = ctx.guild.voice_client
        mp3_fp.seek(0)
        vc.play(FFmpegPCMAudioGTTS(mp3_fp.read(), pipe=True), after=print("Done"))

    except Exception as e:
        print("[가즈아 함수에서 에러]", e)

# https://stackoverflow.com/questions/62494399/how-to-play-gtts-mp3-file-in-discord-voice-channel-the-user-is-in-discord-py

# 웹 스크래핑 soup 객체 생성
def create_soup(url):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36", "Accept-Language": "ko"}
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    return soup

# 네이버 날씨 현재 온도
@bot.command(name="날씨")
async def _1(ctx):
    url = "https://weather.naver.com/"
    soup = create_soup(url)
    block = soup.find("div", attrs={"class":"weather_now"})
    temp = block.div.strong.get_text()

    # 맑음 흐림 비
    summary = block.p.span.get_text().strip()

    # 어제보다 3도 높아요
    s1 = block.p.em.get_text().strip()
    s2 = block.p.find_all('span')[1].get_text().strip()
    summary2 = f'{s1} {s2}'

    await ctx.send(f'{temp} {summary}')


# op.gg 소환사 전적 검색
@bot.command(name="전적")
async def _1(ctx, *, text):
    if text == None:
        print("아이디가 입력되지 않았어요")
    url_base = "https://www.op.gg/summoner/userName="
    url = url_base + text
    soup = create_soup(url)

    # 연승연패
    i = 0
    recent = soup.find("ul", attrs={"class":"css-164r41r exlvoq30"}).find_all("li", attrs={'class':'css-ja2wlz e19epo2o3'})
    wl = recent[0].find("div")['result']

    if wl == "LOSE":
        letter = "패"
    elif wl == "WIN":
        letter = "승"
    else:
        raise Exception

    for game in recent:
        if wl == game.find("div")['result']:
            i += 1
        else:
            break

    msg = f"[{str(i)}연{letter}중입니다]\n"

    # 모스트 챔프
    msg2 = ""
    ranked = soup.find("div", attrs={"class":"css-1s4j24f exxtup3"})
    champ_list = ranked.div.find_all("div", attrs={"class":"champion-box"})
    for champ in champ_list[:4]:
        champ_name = champ.find("div", attrs={"class":"info"}).find("div").find("a").text.strip()
        champ_kda = champ.find("div", attrs={"class":"kda"}).find("div").find("div").text.strip().split(":")[0]
        champ_winrate = champ.find("div", attrs={"class":"played"}).find_all("div")[0].text.strip()
        champ_game = champ.find("div", attrs={"class":"played"}).find_all("div")[1].text.strip()
        
        message = f'{champ_name} {champ_kda} {champ_game}판 {champ_winrate}'
        msg2 += message + "\n"

    await ctx.send(msg+msg2)


# op.gg 라인별 N티어 챔프
# '탑', '정글', '미드', '원딜', '서폿' 1~5티어 검색
def check_tier_argument(arg: str) -> str:
    if arg[-2:] == '티어':
        try:
            num = int(arg[:-2])
            if num > 5:
                return False, '티어는 1에서 5 사이의 숫자로 입력하세요'
            else:
                return True, num
        except:
            return False, '잘못된 입력 형식입니다'
    else:
        return False, ''


def get_tier_champ(tf, arg2, line):
    if tf == True:
        num = int(arg2)
        msg = f"[{line} {num}티어 챔프]"
        line_eng = {'탑':'top', '정글':'jungle', '미드':'mid', '원딜':'adc', '서폿':'support'}
        
        text = line_eng[line]
        url = f"https://www.op.gg/champions?position={text}"
        soup = create_soup(url)
        
        # class_name = 'positionRank css-1h9ha2a e1oulx2j4'
        champ_list = soup.find('table', attrs={'class':['positionRank', 'css']}).find('tbody').find_all("tr")
        print(len(champ_list))
        print(champ_list)
        for champ in champ_list:
                name = champ.find_all('td')[1].a.span.strong.text.strip()
                winrate = champ.find_all('td')[2].text.strip()
                pickrate = champ.find_all('td')[3].text.strip()
                tier = champ.find_all('td')[4].text.strip()
                tier = int(tier)

                if tier == num:
                    msg += f"\n{name} {winrate} {pickrate}"
                else:
                    continue
        return msg
    else:
        return arg2

@bot.command(aliases=['탑','정글','미드','원딜','서폿'])
async def _1(ctx, *, text="1티어"):
    tf, arg2 = check_tier_argument(text)
    print(ctx)
    print(ctx.invoked_with)
    msg = get_tier_champ(tf, arg2, ctx.invoked_with)
    print(msg)
    await ctx.send(msg)
    
# 메뉴 추천
@commands.cooldown(6, 30, commands.BucketType.user)
@bot.command(aliases=['뭐먹지', '오늘뭐먹지', '저녁뭐먹지', '메뉴추천', '점심메뉴추천', '저녁메뉴추천'])
async def _2(ctx):
    try:
        menu = ''
        with open(r'menu.txt', 'r', encoding='utf8') as f:
            x = random.randint(0, len(f.readlines()))

        with open(r'menu.txt', 'r', encoding='utf8') as f:
            i = 0
            for line in f:
                if x==i:
                    menu = line
                i += 1
        await ctx.send(menu)
    except Exception as e:
        print("[메뉴추천 함수에서 에러]", e)

# 애니 추천
@commands.cooldown(6, 30, commands.BucketType.user)
@bot.command(name="애니추천")
async def _1(ctx):
    msg = ["추천해줘도 안볼거 다 앎", "그 시간에 책이나 읽으세요"]
    try:
        tsun = random.random()
        if tsun < 0.2:
            await ctx.send(msg[0])
        elif tsun < 0.25:
            await ctx.send(msg[1])
        else:
            i=0
            x = random.randint(0, 2828)
            with open('animelist.txt', 'r', encoding='utf8') as f:
                for line in f:
                    if x==i:
                        anime = line
                    i += 1
            await ctx.send(anime)
    except Exception as e:
        print("[애니추천 함수에서 에러]", e)

# 애니 검색
@commands.cooldown(6, 30, commands.BucketType.user)
@bot.command(name="애니검색")
async def _1(ctx):
    url = 'https://share.streamlit.io/doorigin/domodomo-anime/main/main.py'
    await ctx.send(url)
   
# 일일 코로나 확진자
@bot.command(name="확진자")
async def _1(ctx):
    url = 'http://ncov.mohw.go.kr/'
    soup = create_soup(url)
    stat = soup.find("div", attrs={'class':'occurrenceStatus'})
    text = stat.h2.span.text.strip().split(',')[0]+")"
    num = soup.find("table", attrs={'class':'ds_table'}).tbody.tr.find_all('td')[3].text.strip()
    await ctx.send(f"오늘 확진자 {num}명 {text}")

# op.gg 제공 가장 많이 쓰이는 룬
@bot.command(name="룬", text=None, pos=None)
@commands.cooldown(1, 20, commands.BucketType.user)
async def _4(ctx, *, text=None):
    if text == None:
        await ctx.send("챔피언 이름을 적어주세요")
    elif text not in list(champ_dic().keys()):
        await ctx.send("챔피언 이름을 정확히 적어주세요")
    else:
        champ_url = champ_dic()[text]
        path = chromedriver_autoinstaller.install()
        url = f'https://www.op.gg{champ_url}/runes/'
        options = webdriver.ChromeOptions()
        options.add_argument('window-size=1920x3000')
        options.add_argument("--start-maximized")
        options.add_argument("disable-gpu")
        options.add_argument("disable-dev-shm-usage")
        browser = webdriver.Chrome(path, options=options)
        print(f"[로딩중] {url}")
        try:
            browser.get(url)
            element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH , '//*[@id="__next"]/div[5]/div[2]/div/div[2]/div[1]/div[1]')))
            scshot = element.screenshot_as_png #image byte
            arr = BytesIO(scshot)
            await ctx.send(f'{text} 룬 <{url}>')
            await ctx.send(file=discord.File(arr, f'{text}_rune.png'))

        except Exception as e:
            print(f'[Timeout]{e}')
            print('뭔가 문제')
        browser.quit()
        print("-----로딩완료-----")
        
# 멕가 유튜브
@bot.command(name="멕가유튜브")
async def _5(ctx):
    video_list = ['https://www.youtube.com/watch?v=rNNSAr1kCFk&t=160s&ab_channel=%EB%A9%95%EA%B0%80Youtube',
     'https://www.youtube.com/watch?v=hvVDmO8gceA&t=48s&ab_channel=%EB%A9%95%EA%B0%80Youtube',
     'https://www.youtube.com/watch?v=jVNE3LxHd6E&t=131s&ab_channel=%EB%A9%95%EA%B0%80Youtube',
     'https://www.youtube.com/watch?v=d_eKXJ348d8&t=211s&ab_channel=%EB%A9%95%EA%B0%80Youtube',
     'https://www.youtube.com/watch?v=fmwxZb-4pG8&ab_channel=%EB%A9%95%EA%B0%80Youtube',
     'https://www.youtube.com/watch?v=-bc-I2a4HRU&ab_channel=%EB%A9%95%EA%B0%80Youtube',
     'https://www.youtube.com/watch?v=Ox-pczThPtc&ab_channel=%EB%A9%95%EA%B0%80Youtube',
     'https://www.youtube.com/watch?v=Efte_fXVm70&ab_channel=%EB%A9%95%EA%B0%80Youtube']
     
    idx = random.randint(0, len(video_list)-1)
    url = video_list[idx]
    await ctx.send(f"심심할 때 보는 멕가 유튜브")
    await ctx.send(url)

# 비스크돌 라디오
@bot.command(aliases=['비스크돌', '비스크돌라디오', '성우라디오', 'ㄷㅁㄷㅁ라디오'])
async def _5(ctx):
    url = 'https://www.youtube.com/channel/UCZu4EgNb0G13sgcfJOHvDmA'
    await ctx.send(url)
    
# LAFTEL
@bot.command(name="라프텔")
async def _1(ctx, *, text, text2=None, text3=None, text4=None, text5=None):
    data = await laftel.searchAnime(f'{text} {text2} {text3}')  # List[SearchResult]
    data = await laftel.getAnimeInfo(data[0].id)  # AnimeInfo

    if len(data.content) > 300:
        content = f'{data.content[:300]}...'
    else:
        content = data.content
    embed=discord.Embed(title=data.name, url=data.url, description=content, color=discord.Color.purple())
    embed.set_thumbnail(url=data.image)
    embed.add_field(name="별점", value=data.avg_rating, inline=True)
    embed.add_field(name="장르", value=", ".join(str(x) for x in data.genres), inline=True)
    embed.add_field(name="방영분기", value=data.air_year_quarter, inline=True)
    await ctx.send(embed=embed)

# Error Handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send('This command is on a %.2fs cooldown' % error.retry_after)
    raise error  # re-raise the error so all the errors will still show up in console

try:
    DISCORD_TOKEN = os.environ['DISCORD_TOKEN']
except:
    print('error fetching DISCORD_TOKEN')

bot.run(DISCORD_TOKEN)
