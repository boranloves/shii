import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import json
import time
import os
import asyncio
from youtube_search import YoutubeSearch
import sympy
import requests
from koreanbots.integrations.discord import DiscordpyKoreanbots
import random
import re
from korcen import korcen

start_time = datetime.utcnow()
why = ['으에?', '몰?루', '왜요용', '잉', '...?', '몰라여', '으에.. 그게 뭐징?', '네?']

class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix=["/", "!", "시이 "], intents=discord.Intents.all(), case_insensitive=True, sync_command=True)

    async def on_ready(self):
        print(f"Logged in as {self.user}")
        await self.change_presence(status=discord.Status.online,
                                   activity=discord.Activity(type=discord.ActivityType.listening, name="류현준 난간 "))
        await self.tree.sync()

        kb = DiscordpyKoreanbots(self,
                                 run_task=True)
        ss = self.guilds
        print(ss)
        simulate_stock_market.start()
        if not os.path.exists(json_file_path):
            with open(json_file_path, 'w') as file:
                json.dump({}, file)

class BotSettings:
    def __init__(self):
        self.detect_swearing = False


json_file_path = 'bot_info.json'
attendance_file = 'attendance.json'
intents = discord.Intents.all()
bot = Bot(intents=intents)
NAVER_CAPTCHA_API_URL = 'https://openapi.naver.com/v1/captcha/nkey?code='
NAVER_CAPTCHA_CHECK_URL = 'https://openapi.naver.com/v1/captcha/ncaptcha.bin?key='
KITSU_API_URL = "https://kitsu.io/api/edge/anime"
naver_client_id = ''
naver_client_secret = ''
KAKAO_API_KEY = ''
server_data_path = 'server_data.json'
happiness_file_path = 'happiness.json'
money_file = 'user_money.json'
audio_file_path = "output.wav"
mamo_file = 'mamo.json'
lv_file = 'lv.json'
SETTINGS_FILE = "bot_settings.json"
count_FILE = 'count.json'
start_time = datetime.now()
settings = BotSettings()
intents.message_content = True


async def load_datas():
    try:
        with open(count_FILE, 'r') as file:
            data = json.load(file)
            return data.get('command_count', 0)
    except FileNotFoundError:
        print("데이터 파일이 없습니다. 새로운 파일을 생성합니다.")
        return 0


async def save_data():
    command_count = await load_datas()
    data = {"command_count": command_count + 1}
    with open(count_FILE, 'w') as file:
        json.dump(data, file)

# 명령어가 실행될 때마다 커맨드 카운트를 업데이트합니다.
async def update_command_count():
    command_count = await load_datas()
    data = {"command_count": command_count + 1}
    with open(count_FILE, 'w') as file:
        json.dump(data, file)


def load_experience():
    try:
        with open(lv_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# 경험치와 레벨을 저장하는 함수
def save_experience():
    with open(lv_file, 'w') as file:
        json.dump(experience, file, indent=4)

# 경험치와 레벨 딕셔너리를 로드합니다.
experience = load_experience()

def search_anime(query):
    # Kitsu API로 애니를 검색하는 함수
    response = requests.get(KITSU_API_URL, params={"filter[text]": query})
    if response.status_code == 200:
        data = response.json()
        if data['data']:  # 결과가 있는 경우
            anime = data['data'][0]
            attributes = anime['attributes']
            title = attributes['canonicalTitle']
            synopsis = attributes['synopsis']
            rating = attributes['averageRating']
            episodes = attributes['episodeCount']
            cover_image = attributes['posterImage']['original']
            embed = discord.Embed(title=f"**{title}**", description=f"평점: {rating}", color=0xFFB2F5)
            embed.set_thumbnail(url=cover_image)
            embed.add_field(name="에피소드 수", value=f"`{episodes}` 편", inline=False)
            return embed
    return None


def get_school_code(school_name):
    base_url = "https://open.neis.go.kr/hub/schoolInfo"
    api_key = ""
    url = f"{base_url}?Type=json&pIndex=1&pSize=1&SCHUL_NM={school_name}&KEY={api_key}"

    response = requests.get(url)
    data = response.json()

    try:
        school_code = data['schoolInfo'][1]['row'][0]['ATPT_OFCDC_SC_CODE']
        return school_code
    except (KeyError, IndexError):
        return None


# 학교급식 정보 가져오기 함수
def get_school_lunch(school_code, date=''):
    base_url = 'https://open.neis.go.kr/hub/mealServiceDietInfo'
    api_key = ''
    url = f'{base_url}?Type=json&pIndex=1&pSize=1&KEY={api_key}&ATPT_OFCDC_SC_CODE=J10&SD_SCHUL_CODE={school_code}&MLSV_FROM_YMD={date}&MLSV_TO_YMD={date}'

    response = requests.get(url)
    data = response.json()

    try:
        menu = data['mealServiceDietInfo'][1]['row'][0]['DDISH_NM']
        return menu
    except (KeyError, IndexError):
        return None


# 사용자 돈 데이터를 불러오는 함수
def load_money():
    try:
        with open(money_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


# 사용자 돈 데이터를 저장하는 함수
def save_money(data):
    with open(money_file, 'w') as file:
        json.dump(data, file, indent=4)


class Happiness:
    def __init__(self):
        self.users = {}

    def get_user_happiness(self, server_id, user_id):
        return self.users.get(server_id, {}).get(user_id, 0)

    def set_user_happiness(self, server_id, user_id, happiness):
        if server_id not in self.users:
            self.users[server_id] = {}
        self.users[server_id][user_id] = happiness

    def increment_user_happiness(self, server_id, user_id, amount=1):
        current_happiness = self.get_user_happiness(server_id, user_id)
        new_happiness = current_happiness + amount
        self.set_user_happiness(server_id, user_id, new_happiness)

    def save_to_file(self):
        with open(happiness_file_path, 'w') as file:
            json.dump(self.users, file, indent=2)

    def load_from_file(self):
        if os.path.exists(happiness_file_path):
            with open(happiness_file_path, 'r') as file:
                self.users = json.load(file)


def save_settings():
    with open(SETTINGS_FILE, 'w') as file:
        json.dump(settings.__dict__, file)

# 설정 로드 함수
def load_settings():
    try:
        with open(SETTINGS_FILE, 'r') as file:
            data = json.load(file)
            settings.detect_swearing = data.get('detect_swearing', False)
    except FileNotFoundError:
        print("설정 파일이 없습니다. 새로운 설정 파일을 생성합니다.")

# 설정 로드
load_settings()


def load_bot_info():
    file_path = json_file_path

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            bot_info = json.load(file)
            print(bot_info)
    except FileNotFoundError:
        bot_info = {}

    return bot_info


def save_bot_info(bot_info):
    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(bot_info, file, indent=2, ensure_ascii=False)


def papago_translate(text, source_lang, target_lang):
    url = 'https://openapi.naver.com/v1/papago/n2mt'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Naver-Client-Id': naver_client_id,
        'X-Naver-Client-Secret': naver_client_secret
    }
    data = {
        'source': source_lang,
        'target': target_lang,
        'text': text
    }
    response = requests.post(url, headers=headers, data=data)
    result = response.json()
    translated_text = result['message']['result']['translatedText']
    return translated_text


# 네이버 검색 함수
def naver_search(query):
    url = 'https://openapi.naver.com/v1/search/blog.json'
    headers = {
        'X-Naver-Client-Id': naver_client_id,
        'X-Naver-Client-Secret': naver_client_secret
    }
    params = {
        'query': query
    }
    response = requests.get(url, headers=headers, params=params)
    result = response.json()
    if 'items' in result:
        return result['items'][0]['title'], result['items'][0]['link']
    else:
        return 'No results found', ''


def load_server_data():
    try:
        with open(server_data_path, 'r') as file:
            server_data = json.load(file)
    except FileNotFoundError:
        server_data = {}

    return server_data


# JSON 파일에 정보를 저장하는 함수 (서버별 데이터 저장용)
def save_server_data(server_id, data):
    server_data = load_server_data()
    server_data[server_id] = data

    with open(server_data_path, 'w') as file:
        json.dump(server_data, file, indent=2, ensure_ascii=False)


def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

stocks = {
    'AAPL': 100,
    'GOOGL': 1500,
    'TSLA': 800,
    'AMZN': 3000,
    'MSFT': 200
}

# 각 서버별 사용자의 자본과 주식을 저장하는 JSON 파일
capital_file = '자본.json'
stocks_file = '주식.json'

# 사용자의 자본을 로드하는 함수
def load_capital():
    try:
        with open(capital_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# 사용자의 자본을 저장하는 함수
def save_capital(capital):
    with open(capital_file, 'w') as f:
        json.dump(capital, f)

# 사용자의 주식을 로드하는 함수
def load_stocks():
    try:
        with open(stocks_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# 사용자의 주식을 저장하는 함수
def save_stocks(stocks):
    with open(stocks_file, 'w') as f:
        json.dump(stocks, f)

# 메모를 저장하는 함수
def save_memo(user_id, memo_name, memo_content):
    memos = load_memos()
    if user_id not in memos:
        memos[user_id] = {}
    if memo_name not in memos[user_id]:
        memos[user_id][memo_name] = memo_content
        with open(mamo_file, 'w') as f:
            json.dump(memos, f)
        return True
    else:
        return False

# 사용자의 메모를 불러오는 함수
def load_memos():
    try:
        with open(mamo_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# 메모를 확인하는 명령어
@bot.hybrid_command(name='메모불러오기', description="쓴 메모를 불러옵니다.")
async def mamo(interaction: discord.Interaction, memo_name):
    user_id = str(interaction.message.author.id)
    memos = load_memos()
    if user_id not in memos or memo_name not in memos[user_id]:
        await interaction.send("해당 메모를 찾을 수 없습니다.")
    else:
        embed = discord.Embed(title=f"{memo_name}", description=f"{memos[user_id][memo_name]}", color=0xFFB2F5)
        await interaction.send(embed=embed)


@bot.hybrid_command(name='메모쓰기', description="새 메모를 씁니다.")
async def mamo_save1(interaction: discord.Interaction, memo_name, *, memo_content):
    user_id = str(interaction.message.author.id)
    if save_memo(user_id, memo_name, memo_content):
        await interaction.send("메모가 저장되었습니다.")
    else:
        await interaction.send("이미 같은 이름의 메모가 존재합니다.")



@bot.hybrid_command(name='애니검색', description="Kitsu api로 애니를 검색 합니다.")
async def anime(interaction: discord.Interaction, keyword: str):
    embed = search_anime(keyword)
    if embed:
        await interaction.send(embed=embed)
    else:
        embed = discord.Embed(title="해당 애니를 찾을 수 없습니다.", color=0xFF2424)
        await interaction.send(embed=embed)

# 사용자별 보유 주식 정보를 저장하는 딕셔너리
user_stocks = {}

# 실시간 주식 시장 시뮬레이션
@tasks.loop(minutes=5)
async def simulate_stock_market():
    global stocks
    for stock in stocks:
        # 랜덤하게 주식 가격 변동
        stocks[stock] += random.randint(-50, 50)
        if stocks[stock] <= 0:
            stocks[stock] = 1

        # 주식 정보 저장
        save_stocks(stocks)


# 주식 가격 조회 명령어
@bot.hybrid_command(name='가격보기', description="주식가격확인")
async def check_stock_price(interaction: discord.Interaction):
    embed = discord.Embed(title="주식 가격", color=0x00ff00)
    for stock, price in stocks.items():
        embed.add_field(name=f"{stock.upper()} 가격", value=f"${price}", inline=False)
    await interaction.send(embed=embed)

# 주식 구매 명령어
@bot.hybrid_command(name='주식매수', description="주식매수")
async def buy_stock(interaction: discord.Interaction, stock: str, quantity: int):
    server_id = str(interaction.guild.id)
    user_id = str(interaction.message.author.id)
    if stock.upper() in stocks:
        cost = stocks[stock.upper()] * quantity
        capital = load_capital()
        if server_id not in capital:
            capital[server_id] = {}
        if user_id not in capital[server_id]:
            capital[server_id][user_id] = 0
        if cost <= 0:
            await interaction.send('0개 이하의 주식을 구매할 수 없습니다.')
        elif cost <= capital[server_id][user_id]:
            if cost <= 1000000:  # 가상 자본 제한 (100만 달러)
                if server_id not in user_stocks:
                    user_stocks[server_id] = {}
                if user_id not in user_stocks[server_id]:
                    user_stocks[server_id][user_id] = {}
                if stock.upper() not in user_stocks[server_id][user_id]:
                    user_stocks[server_id][user_id][stock.upper()] = 0
                user_stocks[server_id][user_id][stock.upper()] += quantity
                capital[server_id][user_id] -= cost
                await interaction.send(f'{stock.upper()}를 ${cost}에 {quantity}주 구매했습니다.')
            else:
                await interaction.send('자본 한도를 초과하여 더 이상 주식을 구매할 수 없습니다.')
        else:
            await interaction.send('자금이 부족하여 주식을 구매할 수 없습니다.')
        save_capital(capital)
        save_stocks(user_stocks)
    else:
        await interaction.send(f'{stock.upper()}은(는) 유효한 주식 기호가 아닙니다.')

# 주식 판매 명령어
@bot.hybrid_command(name='주식매도', description="주식팔기")
async def sell_stock(interaction: discord.Interaction, stock: str, quantity: int):
    server_id = str(interaction.guild.id)
    user_id = str(interaction.message.author.id)
    if stock.upper() in stocks:
        capital = load_capital()
        if server_id not in capital or user_id not in capital[server_id]:
            await interaction.send('판매할 주식이 없습니다.')
        elif stock.upper() not in user_stocks.get(server_id, {}).get(user_id, {}):
            await interaction.send(f'{stock.upper()}의 주식을 소유하고 있지 않습니다.')
        elif user_stocks[server_id][user_id][stock.upper()] >= quantity:
            user_stocks[server_id][user_id][stock.upper()] -= quantity
            earnings = stocks[stock.upper()] * quantity
            capital[server_id][user_id] += earnings
            await interaction.send(f'{stock.upper()}를 ${earnings}에 {quantity}주 판매했습니다.')
            save_capital(capital)
            save_stocks(user_stocks)
        else:
            await interaction.send('판매할 주식이 충분하지 않습니다.')
    else:
        await interaction.send(f'{stock.upper()}은(는) 유효한 주식 기호가 아닙니다.')

# 개인 자본 확인 명령어
@bot.hybrid_command(name='자본', description="자본보기")
async def check_balance(interaction: discord.Interaction):
    server_id = str(interaction.guild.id)
    user_id = str(interaction.message.author.mention)
    capital = load_capital()
    if server_id in capital and user_id in capital[server_id]:
        await interaction.send(f'{interaction.message.author.mention}님의 현재 자본은 ${capital[server_id][user_id]} 입니다.')
    else:
        if server_id not in capital:
            capital[server_id] = {}
        capital[server_id][user_id] = 500  # 초기 자본 설정
        save_capital(capital)
        await interaction.send(f'{interaction.message.author.mention}님, 초기 자본 $500을 지급하였습니다.')

# 보유 주식 확인 명령어
@bot.hybrid_command(name='주식보기', description="보유한 주식 조회")
async def view_stocks(interaction: discord.Interaction):
    server_id = str(interaction.guild.id)
    user_id = str(interaction.message.author.id)
    user_stocks = load_stocks()  # 사용자별 보유 주식 정보를 로드합니다.

    if server_id in user_stocks and user_id in user_stocks[server_id]:
        user_stock_info = user_stocks[server_id][user_id]
        if user_stock_info:
            embed = discord.Embed(title=f"{interaction.message.author.display_name}님의 보유 주식", color=0x00ff00)
            for stock, quantity in user_stock_info.items():
                embed.add_field(name=f"{stock.upper()}", value=f"수량: {quantity}", inline=False)
            await interaction.send(embed=embed)
        else:
            await interaction.send("보유한 주식이 없습니다.")
    else:
        await interaction.send("보유한 주식이 없습니다 .")



@bot.hybrid_command(name="고양이", description="랜덤으로 고양이 사진을 불러옵니다")
async def cat(interaction: discord.Interaction):
    cat_image_url = get_random_cat()
    await interaction.send(cat_image_url)


def get_random_cat():
    response = requests.get('https://api.thecatapi.com/v1/images/search')
    data = response.json()
    return data[0]['url']



@bot.hybrid_command(name='급식', description="학교급식 2주 정보 보기")
async def school_lunch(interaction: discord.Interaction, school_name: str):
    school_code = get_school_code(school_name)

    if school_code:
        # 임베드 생성
        embed = discord.Embed(title=f"{school_name} 급식", color=0x00ff00)

        # 현재 날짜부터 30일 동안의 급식 정보 추가
        today = datetime.today()
        for i in range(14):
            date = (today + timedelta(days=i)).strftime('%m%d')
            lunch_menu = get_school_lunch(school_code, date)
            if lunch_menu:
                embed.add_field(name=f"{date}", value=lunch_menu)
            else:
                embed.add_field(name=f"{date}", value="해당 날짜의 급식 정보를 찾을 수 없습니다.")
        await interaction.send(embed=embed)
    else:
        await interaction.send(f"{school_name} 를 찾을 수 없습니다.")


@bot.hybrid_command(name='번역', description="source_lang: 원본 언어 target_lang: 번역할 언어 네이버 open api를 통한 번역(베타)")
async def translate(interaction: discord.Interaction, source_lang, target_lang, *, text: str):
    translation = papago_translate(text, source_lang, target_lang)
    embed = discord.Embed(title='번역 완료!', description="", color=0xFFB2F5)
    embed.add_field(name=translation, value=f"{source_lang}에서 {target_lang}로 번역", inline=False)
    await interaction.send(embed=embed)


@bot.hybrid_command(name='카카오검색', description="카카오를 통한 검색(베타)")
async def search_kakao(interaction: discord.Interaction, *, text: str):
    # 사용자 입력을 문자열로 결합
    query = ' '.join(text)

    # 카카오 검색 API 호출
    url = f'https://dapi.kakao.com/v2/search/web?query={query}'
    headers = {'Authorization': f'KakaoAK {KAKAO_API_KEY}'}
    response = requests.get(url, headers=headers)

    try:
        # 응답이 JSON 형식으로 파싱 가능한지 확인
        response.raise_for_status()
        data = response.json()

        # 첫 번째 검색 결과를 가져오기
        result = data['documents'][0]

        # 결과를 디스코드 채팅으로 전송
        embed = discord.Embed(title=f"**카카오 검색 결과**", color=0xFFE400)
        html_text = f'{result["title"]}'
        plain_text = remove_html_tags(html_text)
        embed.add_field(name=plain_text, value=f'URL: {result["url"]}', inline=False)
        await interaction.send(embed=embed)

    except requests.exceptions.HTTPError as e:
        await interaction.send(f'HTTP 오류: {e.response.status_code} - {e.response.text}')

    except (IndexError, KeyError):
        await interaction.send(f'검색 결과를 찾을 수 없습니다. 더 정확한 검색어를 입력하세요.')

    except requests.exceptions.RequestException as e:
        await interaction.send(f'오류 발생: {e}')


@bot.hybrid_command(name='블로그검색', description="네이버 open api를 통한 검색(베타)")
async def search(interaction: discord.Interaction, *, query):
    title, link = naver_search(query)
    html_text = title
    plain_text = remove_html_tags(html_text)
    embed = discord.Embed(title=f"검색어: {query}", description=plain_text, color=0x86E57F)
    embed.set_footer(text=link)
    await interaction.send(embed=embed)


@bot.hybrid_command(name='유튜브검색', description="유튜브 검색(베타)")
async def youtube_search(interaction: discord.Interaction, *, query: str):
    results = YoutubeSearch(query, max_results=1).to_dict()

    if results:
        video_title = results[0]['title']
        video_url = f"https://www.youtube.com/watch?v={results[0]['id']}"
        await interaction.send(f'검색 결과: {video_title}\n링크: {video_url}')
    else:
        await interaction.send('검색 결과를 찾을 수 없습니다.')



@bot.hybrid_command(name='계산', description="수식을 계산합니다.")
async def calculate_expression(ctx, *, expression):
    try:
        result = sympy.sympify(expression)
        await ctx.send(f'계산 결과: {result}')
    except Exception as e:
        await ctx.send(f'계산 중 오류가 발생했습니다: {e}')


@bot.hybrid_command(name='클리어', description="메시지 청소")
async def clear(interaction: discord.Interaction, amount: int):
    sent_message1 = await interaction.send("잠시 기다려 주세요")
    if not interaction.guild:
        sent_message2 = await interaction.send("DM에서는 사용이 불가능한 명령어입니다!")
        await asyncio.sleep(3)
        await sent_message1.delete()
        await sent_message2.delete()
        return

    channel = interaction.channel
    await channel.purge(limit=amount + 1)
    sent_message = await channel.send(f"{amount}개의 메시지를 삭제했어요!")
    print(f"{amount}개의 메시지를 삭제했어요!")
    await asyncio.sleep(3)
    await sent_message.delete()


@bot.hybrid_command(name='음성채널입장', description="음성 채널 입장(베타)")
async def start1(interaction: discord.Interaction):
    if interaction.message.author.voice and interaction.message.author.voice.channel:
        channel = interaction.message.author.voice.channel
        await interaction.send(f"봇이 {channel} 채널에 입장합니다.")
        await channel.connect()
        print(f"음성 채널 정보: {interaction.message.author.voice}")
        print(f"음성 채널 이름: {interaction.message.author.voice.channel}")
    else:
        await interaction.send("음성 채널에 유저가 존재하지 않습니다. 1명 이상 입장해 주세요.")


@bot.hybrid_command(name='임베드생성', description="임베드생성기")
async def send_server_announcement1(interaction: discord.Interaction, text: str, text1: str, text2: str, text3: str):
    embed = discord.Embed(title=text, description=text1, color=0xFFB2F5)
    embed.add_field(name=text2, value=text3, inline=False)
    await interaction.send(embed=embed)


@bot.hybrid_command(name='음성채널퇴장', description="음성 채널 퇴장(베타)")
async def stop1(interaction: discord.Interaction):
    try:
        # 음성 채널에서 봇을 내보냅니다.
        await interaction.message.voice_client.disconnect()
        await interaction.send(f"봇을 {interaction.message.author.voice.channel} 에서 내보냈습니다.")
    except IndexError as error_message:
        print(f"에러 발생: {error_message}")
        await interaction.send(f"{interaction.message.author.voice.channel}에 유저가 존재하지 않거나 봇이 존재하지 "
                                               f"않습니다.\\n다시 입장후 퇴장시켜주세요.")
    except AttributeError as not_found_channel:
        print(f"에러 발생: {not_found_channel}")
        await interaction.send("봇이 존재하는 채널을 찾는 데 실패했습니다.")


@bot.hybrid_command(name='가위바위보', description="가위바위보!")
async def game(interaction: discord.Interaction, user: str):  # user:str로 !game 다음에 나오는 메시지를 받아줌
    rps_table = ['가위', '바위', '보']
    bot = random.choice(rps_table)
    result = rps_table.index(user) - rps_table.index(bot)  # 인덱스 비교로 결과 결정
    if result == 0:
        await interaction.send(f'{user} vs {bot}  비겼당.')
        print(f'{user} vs {bot}  비겼당.')
    elif result == 1 or result == -2:
        await interaction.send(f'{user} vs {bot}  졌당.')
        print(f'{user} vs {bot}  졌당.')
    else:
        await interaction.send(f'{user} vs {bot}  내가 이겼당~.')
        print(f'{user} vs {bot}  내가 이겼당~.')



@bot.hybrid_command(name='공지사항', description="시이봇의 공지를 볼 수 있어요!")
async def announcement(interaction: discord.Interaction):
    embed = discord.Embed(title="시이봇 공지 사항", description="2024.02.15일 공지", color=0xFFB2F5)
    embed.add_field(name="시이봇 개발 안내", value="시이봇 점검(개발) 기간은 매일 약 오후2시 부터 오후 6시 입니다. 이때는 시이봇이 멈출수도 있으니 양해 부탁드립니다.",
                    inline=False)
    embed.add_field(name="/번역 관련 공지 (중요)", value="현제, /번역 커멘드는 네이버의 파파고 openapi 를 사용하여 개발하였습니다. 그러나 파파고 번역 api가 2월 29일자로 서비스가 종료되어, 2월 29일자 이후로는 /번역이 사용이 불가하여, 2월 28일자로 /번역 서비스를 종료함을 알려드립니다. 죄송합니다.",
                    inline=False)
    await interaction.send(embed=embed)


def get_timestamp():
    return int(time.time())


@bot.hybrid_command(name='핑', description="퐁!")
async def ping(interaction: discord.Interaction):
    message_latency = round(bot.latency * 1000, 2)
    start_times = interaction.message.created_at
    message5 = await interaction.send("메시지 핑 측정중...")
    end_time = message5.created_at
    await message5.delete()
    latency = (end_time - start_times).total_seconds() * 1000

    now = datetime.utcnow()
    uptime_seconds = start_time - now
    uptime_minutes = uptime_seconds // 60

    embed = discord.Embed(title="퐁!", color=0xFFB2F5)
    embed.add_field(name=f'REST ping', value=f"`{latency}ms`")
    embed.add_field(name=f'Gateway ping', value=f"`{message_latency}ms`")
    embed.add_field(name=f'업타임', value=f"`{uptime_minutes}분`")
    list_length = len(bot.guilds)
    embed.add_field(name="서버수", value=f"`{list_length}`")
    embed.set_footer(text='{}'.format(get_timestamp()))
    await interaction.send(embed=embed)


@bot.hybrid_command(name='광질', description="광질을 하자")
async def mining(interaction: discord.Interaction):
    minerals = ['다이아몬드', '루비', '에메랄드', '자수정', '철', '석탄']
    weights = [1, 3, 6, 15, 25, 50]
    results = random.choices(minerals, weights=weights, k=3)
    await interaction.send(', '.join(results) + ' 광물들을 획득하였습니다.')
    print(', '.join(results) + ' 광물들을 획득하였습니다.')


@bot.hybrid_command(name='주사위', description="주사위 굴리기")
async def roll(interaction: discord.Interaction):
    randnum = random.randint(1, 6)  # 1이상 6이하 랜덤 숫자를 뽑음
    await interaction.send(f'주사위 결과는 {randnum} 입니다.')
    print(f'주사위 결과는 {randnum} 입니다.')


@bot.hybrid_command(name='프로필', description="프로필를 봅니다")
async def dp(interaction: discord.Interaction, member: discord.Member = None):
    print(member)
    if not member:
        member = interaction.user
    embed = discord.Embed(color=0xFFB2F5)
    embed.set_image(url=member.avatar)
    await interaction.send(embed=embed)


@bot.hybrid_command(name="내정보", description='내 정보를 봅니다')
async def propill(interaction: discord.Interaction):
    member = interaction.message.author
    roles = member.roles
    role_names = [role.name for role in roles]
    server_id = str(interaction.guild.id)
    user_id = str(interaction.message.author.id)
    user_name = str(interaction.message.author.display_name)
    current_happiness = happiness_manager.get_user_happiness(server_id, user_id)
    server_id = str(interaction.guild.id)
    user_id = str(interaction.message.author.id)
    capital = load_capital()
    embed = discord.Embed(title=f"{user_name} 님의 정보", color=0xFFB2F5)
    if not member:
        member = interaction.user
    embed.set_thumbnail(url=member.avatar)
    embed.add_field(name="호감도", value=f":heart: {current_happiness}")
    embed.add_field(name="역할", value=f"`{role_names}`")
    if server_id in capital and user_id in capital[server_id]:
        embed.add_field(name="자본", value=f"${capital[server_id][user_id]}")
    else:
        embed.add_field(name="자본", value="아직 주식을 시작하지 않았습니다.")

    await interaction.send(embed=embed)


@bot.hybrid_command(name='타이머', description="타이머 실행(베타)")
async def set_time(interaction: discord.Interaction, seconds: int, message='타이머 종료!'):
    await interaction.send(f'{seconds}초 후에 알림이 옵니다.')
    await asyncio.sleep(seconds)
    await interaction.send(message)


@bot.hybrid_command(name='카피', description="시이가 따라 말해요")
async def copy(interaction: discord.Interaction, copyword: str):
    await interaction.send(copyword)


@bot.hybrid_command(name='인원통계', description="서버 인원 통계(베타)")
async def member_stats(interaction: discord.Interaction):
    guild = interaction.guild
    total_members = guild.member_count

    role_stats = {}
    for role in guild.roles:
        if role.name != '@everyone':
            role_stats[role.name] = len(role.members)
    embed = discord.Embed(title="인원통계", description=f"총 인원: {total_members}\n", color=0xFFB2F5)
    embed.add_field(name=f"각 역할별 인원: {role_stats}", value="", inline=False)
    await interaction.send(embed=embed)


@bot.hybrid_command(name='이모지', description="이모지를 크게 보기")
async def emojis(interaction: discord.Interaction, *, emojsi: discord.Emoji=None):
    for emoji in emojsi:
        # 이모지 URL을 얻어옵니다.
        emoji_url = f'https://cdn.discordapp.com/emojis/{emojsi.id}.png'
        # 임베드에 이모지를 크게 표시합니다.
        embed = discord.Embed(color=0xFFB2F5)
        embed.set_image(url=emoji_url)
        await interaction.send(embed=embed)
        break  # 첫 번째 이모지만 사용합니다.


@bot.hybrid_command(name='도움말', description="시이봇 메뉴얼")
async def help(interaction: discord.Interaction):
    embed = discord.Embed(title="안녕하세요, 시이입니다!", description="귀여운 챗봇 하나쯤, 시이\n'시이야'라고 불러주세요!", color=0xFFB2F5)
    embed.set_thumbnail(url='https://cdn.litt.ly/images/d7qircjSN5w6FNgD5Oh57blUjrfbBmCj?s=1200x1200&m=outside&f=webp')
    embed.add_field(name="**일반**", value="핑, 번역, 패치노트, 계산, 인원통계, 타이머, 프로필, 급식, 메모쓰기, 메모불러오기, 공지사항, 패치노트", inline=False)
    embed.add_field(name="**검색**", value="네이버검색, 유튜브검색, 블로그검색, 애니검색", inline=False)
    embed.add_field(name="**재미**", value="고양이, 알려주기, 급식, 호감도확인, 호감도도움말, 가위바위보, 광질, 주사위, 이모지, 골라", inline=False)
    embed.add_field(name="**주식**", value="주식매수, 주식매도, 가격보기, 자본", inline=False)
    embed.add_field(name="**보이스**", value="음성채널입장, 음성채널퇴장", inline=False)
    embed.add_field(name="**관리**", value="내정보, 프로필, 클리어, 임베드생성, 욕설필터링", inline=False)
    embed.add_field(name="", value="", inline=False)
    embed.add_field(name="시이가 궁금하다면", value="[시이 개발 서버](https://discord.gg/SNqd5JqCzU)")
    embed.add_field(name="시이를 서버에 초대하고 싶다면", value="[시이 초대하기](https://discord.com/oauth2/authorize?client_id=1197084521644961913&scope=bot&permissions=0)")
    embed.add_field(name="개발자를 응원할려면", value="[시이 하트 눌러주기](https://koreanbots.dev/bots//vote)")
    embed.add_field(name="", value="", inline=False)
    embed.add_field(name="**Developer** by <:export202402161150235581:1207881809405288538>studio boran", value="", inline=False)
    await interaction.send(embed=embed)


@bot.hybrid_command(name='호감도도움말', description="호감도 시스템 메뉴얼")
async def hhlep(interaction: discord.Interaction):
    embed = discord.Embed(title="시이봇 호감도 시스템 도움말", color=0xFFB2F5)
    embed.add_field(name="호감도 시스템 이란?", value="호감도 시스템은 시이봇과 더 잘 지내라는 바람으로 만들었습니다!, 시이봇과 놀면서 호감도를 키워 보세요!",
                    inline=False)
    embed.add_field(name="호감도 상승법", value="/시이야, /가르치기 커멘드에서 각각 한번 실행 시킬떄 마다 1,2 씩 상승합니다.", inline=False)
    await interaction.send(embed=embed)


@bot.hybrid_command(name='욕설필터링', description="욕설필터링기능을 끄고 킵니다.(관리자 권한 필요)")
async def toggle_swearing_detection(interaction: discord.Interaction):
    if interaction.message.author.guild_permissions.manage_messages:
        settings.detect_swearing = not settings.detect_swearing
        save_settings()
        await interaction.send(f"욕설 감지 기능이 {'켜졌습니다' if settings.detect_swearing else '꺼졌습니다'}.")
    else:
        await interaction.send("관리자만 욕설 감지 설정을 변경할 수 있습니다.")


@bot.hybrid_command(name="골라", description="시이가 골라줍니다")
async def ox(interaction: discord.Interaction, cho: str):
    words = cho.split()
    selected_word = random.choice(words)  # 단어 리스트에서 랜덤으로 선택
    await interaction.send(f"저는 {selected_word} 이요!")



@bot.hybrid_command(name="패치노트", description="시이봇 패치노트 보기")
async def pt(interaction: discord.Interaction):
    embed = discord.Embed(title="v2.18.11 패치노트", color=0xFFB2F5)
    embed.add_field(name="신규기능", value="없음", inline=False)
    embed.add_field(name="버그 수정", value="슬래시 커멘드 실행시 '어플리케이션이 응답하지 않았습니다'가 출력되는 버그 수정", inline=False)
    await interaction.send(embed=embed)


class MyModal(discord.ui.Modal, title="가르치기"):
    m_title = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="키워드",
        required=False,
        placeholder="시이에게 가르칠 키워드"
    )

    m_description = discord.ui.TextInput(
        style=discord.TextStyle.long,
        label="단어",
        required=False,
        placeholder="시이가 키워드에 대답할 단어"
    )

    async def on_submit(self, interaction: discord.Interaction):
        keyword = self.m_title.value
        description = self.m_description.value

        # 가르치기 코드 추가
        bot_info = load_bot_info()
        server_id = str(interaction.guild.id)
        user_id = str(interaction.user.id)
        happiness_manager.increment_user_happiness(server_id, user_id, amount=2)
        happiness_manager.save_to_file()
        print(korcen.check(keyword))
        if korcen.check(keyword) or korcen.check(description):
            embed = discord.Embed(title="그런 단어는 배우기 싫어요..", description="", color=0xFF2424)
            embed.set_footer(text="`© Korcen 을 사용하여 검열하였습니다.`")
            await interaction.response.send_message(embed=embed) # noqa
            return
        if keyword not in bot_info:
            bot_info[keyword] = {
                'description': description,
                'author_nickname': interaction.user.display_name
            }
            await interaction.response.send_message(f"오케! `{keyword}` 라고 하면\n`{description}` 라고 할게욧!") # noqa
        else:
            await interaction.response.send_message(f"`{keyword}`는 이미 알고 있다구욧!") # noqa
        # 정보 저장
        save_bot_info(bot_info)


@bot.tree.command(name='가르치기', description='시이봇에게 많은걸 알려주세요!(베타)')
async def tell(interaction: discord.Interaction):
    await interaction.response.send_modal(MyModal()) # noqa


happiness_manager = Happiness()
happiness_manager.load_from_file()


@bot.hybrid_command(name='호감도확인', description='당신과 시이간의 호감도를 확인합니다.')
async def check_happiness(interaction: discord.Interaction):
    server_id = str(interaction.guild.id)
    user_id = str(interaction.message.author.id)
    user_name = str(interaction.message.author.display_name)
    current_happiness = happiness_manager.get_user_happiness(server_id, user_id)

    # 호감도에 따라 메시지 조건 추가
    if interaction.message.author.id == :
        message = "저를 만드신 studio boran 개발자님 이시죳"
        lv = "lv.max: 개발자"
    elif 0 <= current_happiness <= 5:
        message = "누구더라...흐음.."
        lv = "lv.0: 모르는 사람"
    elif 6 <= current_happiness <= 10:
        message = "기억이 날락 말락...뭐였지"
        lv = "lv.1: 아는사람"
    elif 11 <= current_happiness <= 20:
        message = f"{user_name}, 맞죠?!"
        lv = "lv.2: 이름 외운 사람"
    elif 21 <= current_happiness <= 50:
        message = "우리 칭구 아이가?"
        lv = "lv.3: 친구친구"
    else:
        message = "베프베프!"
        lv = "lv.4: 베스트 프렌즈"
    embed = discord.Embed(title=f"시이가 보는 {user_name}", color=0xFFB2F5)
    embed.set_thumbnail(url='https://cdn.litt.ly/images/d7qircjSN5w6FNgD5Oh57blUjrfbBmCj?s=1200x1200&m=outside&f=webp')
    embed.add_field(name=":speech_balloon: 시이의 한마디", value=message, inline=False)
    embed.add_field(name=f":heart: {lv}", value=f"호감도: {current_happiness}", inline=False)
    embed.set_footer(text='{}'.format(get_time()))
    await interaction.send(embed=embed)


wordshii = ['넹!', '왜 그러세용?', '시이예용!', '필요 하신거 있으신가요?', '뭘 도와드릴까요?', '반가워용', '저 부르셨나요?', '왜요용', '잉', '...?', '네?']
baddword = ['확마', '아놔', '뭐레', '이게', '나쁜말은 싫어요ㅠ']


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if bot.user.mentioned_in(message):
        whyresponse = random.randint(0, 7)
        response = wordshii[whyresponse]
        await message.channel.send(response)
        return
    if message.content.startswith('시이야'):
        if not message.content.startswith('시이야 '):
            wordss = random.randint(0, 10)
            await message.channel.send(wordshii[wordss])
            return
        if message.content.startswith('시이야 '):
            message1 = message.content[4:]
            bot_info = load_bot_info()
            server_id = str(message.guild.id)
            user_id = str(message.author.id)
            happiness_manager.increment_user_happiness(server_id, user_id, amount=1)
            happiness_manager.save_to_file()
            info = bot_info.get(message1)
            total_member_count = 0
            for guild in bot.guilds:
                if guild.name != "한국 디스코드 리스트":
                    total_member_count += guild.member_count
            word = {
                f'{message.author.display_name}': f"저가 {message.author.display_name} 님을 모를리 없죠!",
                '정보': f'지금 시이는 `{len(bot.guilds)}` 개의 서버 에서 `{total_member_count}명` 분들을 위해 일하고 있어요!',
                'hello': '안녕하세욧!',
                '안녕': '안녕하세요. 시이 입니다!',
                '누구야': '안녕하세요. shii 입니다!',
                '요일': ':calendar: 오늘은 {}입니다'.format(get_day_of_week()),
                '시간': ':clock9: 현재 시간은 {}입니다.'.format(get_time()),
                '코딩': '코딩은 재밌어요',
                '게임': '게임하면 또 마크랑 원신을 빼놀수 없죠!',
                'ㅋㅋㅋ': 'ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ',
                '이스터에그': '아직 방장님이 말 하지 말라고 했는데....아직 비밀이예욧!',
                '패치버전': '패치버전 v2.18.11',
                '과자': '음...과자하니까 과자 먹고 싶당',
                '뭐해?': '음.....일하죠 일! 크흠',
                '음성채널': '음성채널는 현재 방장이 돈이 없어서 불가능 합니다ㅠㅠ',
                '이벤트': '흐음..이벤트는 아직 없어요ㅠㅠ',
                '웃어': '히힛 (　＾▽＾)',
                '맴매': '흐에에엥ㅠㅠㅜ방장님! 도와주세여(/´△`＼)',
                '옥에티': '옥에티가 있을것같아요? 네, 아마 있을거예요 방장님이 아직 초짜라',
                '잔소리해줘': '잔소리는 나쁜거예요 알겠어요?',
                '유튜브': '유튜브 검색 기능은 /유튜브검색 으로 실행이 가능합니다!',
                '크레딧': '전부다 보란이(그렇게 써있음 ㅇㅇ)',
                '구멍': '구멍',
                '개발자님': '개발자님이요? 좀, 쪼잔하긴해요(소곤소곤)',
                '종': '댕댕대에에엥',
                '할말없어?': '할말이요? 할말이요? 할말이요? 할말이요? 할말이요? 할말이요? 없어욧!',
                '왭연동': '사이트 및 뉴스 연동은 현재는 업데이트 일정에 없습니다',
                '애교': '이이잉...시져ㅕㅕㅕ',
                '야근': '설마...야근 시킬 생각은 아니시죠?',
                '아이싯떼루': '웩',
                '애니': '~개발자왈~ 백성녀와 흑목사는 꼭 봐라',
                '축구경기': '축구 경기 연동 기능은 현재 개발중 입니다. 빠른 시일내에 완성 하겠습니다!',
                'help': '저와 대화 하실려면 시이야 뒤에 질문을 넣어 불러주세요!',
                '음악': '우리 개발자님은 류현준님의 노래를 좋아한데요. 네, TMI네용',
                'GCP': '지금 시이봇은 GCP에서 실행되고 있습니다!',
                '뭐야': '뭐지?',
                '잘가': '잘가요!',
                '뭐들어?': '앗, 류현준님의 난간이욧!',
                '베타커멘드': '베타 커멘드는 현재 태스트 중인 커멘드 입니다! 언제 생기고 사라질지 모르죠',
                '시이이모지': "<:__:1201865120368824360>"
            }
            if message1 == '' or None:
                whyresponse = random.randint(0, 7)
                response = why[whyresponse]
                await message.channel.send(response)
                return
            elif message1 in word.keys():
                return await message.channel.send(word[message1])
            else:
                if info:
                    author_nickname = info['author_nickname']
                    description = info['description']
                    response = f"{description}\n`{author_nickname} 님이 알려주셨어요!`"
                    await message.channel.send(response)
                else:
                    whyresponse = random.randint(0, 7)
                    response = why[whyresponse]
                    await message.channel.send(response)
    else:
        if settings.detect_swearing:
            content_lower = message.content.lower()
            if korcen.check(content_lower):
                await message.delete()
                await message.channel.send(f"{message.author.mention}, 욕설이 감지되었습니다!")
    await bot.process_commands(message)


def get_day_of_week():
    weekday_list = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']

    weekday = weekday_list[datetime.today().weekday()]
    date = datetime.today().strftime("%Y년 %m월 %d일")
    result = '{}({})'.format(date, weekday)
    return result


def get_time():
    return datetime.today().strftime("%H시 %M분 %S초")


bot.run()
