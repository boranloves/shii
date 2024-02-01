import discord
from discord.ext import commands, tasks
from datetime import datetime
import json
import os
import asyncio
from youtube_search import YoutubeSearch
import sympy
import requests
from koreanbots.integrations.discord import DiscordpyKoreanbots
import random
import re


class Bot(commands.Bot):
    def __init__(self, intents: discord.Intents, **kwargs):
        super().__init__(command_prefix="/", intents=intents, case_insensitive=True)

    async def on_ready(self):
        print(f"Logged in as {self.user}")
        await self.change_presence(status=discord.Status.online,
                                   activity=discord.Activity(type=discord.ActivityType.listening, name="류현준 난간"))
        await self.tree.sync()
        kb = DiscordpyKoreanbots(self,run_task=True)

        if not os.path.exists(attendance_file):
            with open(attendance_file, 'w') as file:
                json.dump({}, file)


json_file_path = 'bot_info.json'
attendance_file = 'attendance.json'
intents = discord.Intents.all()
bot = Bot(intents=intents)
NAVER_CAPTCHA_API_URL = 'https://openapi.naver.com/v1/captcha/nkey?code='
NAVER_CAPTCHA_CHECK_URL = 'https://openapi.naver.com/v1/captcha/ncaptcha.bin?key='
naver_client_id = ''
naver_client_secret = ''
KAKAO_API_KEY = ''
server_data_path = 'server_data.json'


def load_bot_info():
    try:
        with open(json_file_path, 'r') as file:
            bot_info = json.load(file)
    except FileNotFoundError:
        bot_info = {}

    return bot_info


def save_bot_info(bot_info):
    with open(json_file_path, 'w') as file:
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


@bot.hybrid_command(name='네이버검색', description="네이버 open api를 통한 검색(베타)")
async def search(interaction: discord.Interaction, *, query):
    title, link = naver_search(query)
    html_text = title
    plain_text = remove_html_tags(html_text)
    embed = discord.Embed(title=f"검색어: {query}", description=plain_text, color=0x86E57F)
    embed.set_footer(text=link)
    await interaction.send(embed=embed)


@bot.hybrid_command(name='hello', description="hi!")
async def hello(interaction: discord.Interaction):
    await interaction.reply(content="하이")


@bot.hybrid_command(name='bye', description="bye!")
async def bye(interaction: discord.Interaction):
    await interaction.reply(content="빠이")


@bot.hybrid_command(name='copy', description="메세지 복제")
async def copy(interaction: discord.Interaction, text1: str):
    await interaction.send(text1)


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


@bot.hybrid_command(name='clear', description="메세지 청소")
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
    if interaction.author.voice and interaction.author.voice.channel:
        channel = interaction.author.voice.channel
        await interaction.send(f"봇이 {channel} 채널에 입장합니다.")
        await channel.connect()
        print(f"음성 채널 정보: {interaction.author.voice}")
        print(f"음성 채널 이름: {interaction.author.voice.channel}")
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
        await interaction.voice_client.disconnect()
        await interaction.send(f"봇을 {interaction.author.voice.channel} 에서 내보냈습니다.")
    except IndexError as error_message:
        print(f"에러 발생: {error_message}")
        await interaction.send(f"{interaction.author.voice.channel}에 유저가 존재하지 않거나 봇이 존재하지 않습니다.\\n다시 입장후 퇴장시켜주세요.")
    except AttributeError as not_found_channel:
        print(f"에러 발생: {not_found_channel}")
        await interaction.send("봇이 존재하는 채널을 찾는 데 실패했습니다.")


@bot.hybrid_command(name='game', description="가위바위보!")
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


@bot.hybrid_command(name='mining', description="광질을 하자")
async def mining(interaction: discord.Interaction):
    server_id = str(interaction.guild.id)
    server_data = load_server_data()

    minerals = ['다이아몬드', '루비', '에메랄드', '자수정', '철', '석탄']
    weights = [1, 3, 6, 15, 25, 50]
    results = random.choices(minerals, weights=weights, k=3)
    # 개인 데이터 추가 또는 업데이트
    user_id = str(interaction.author.id)
    user_data = server_data.get(server_id, {}).get(user_id, [])
    user_data.extend(results)
    server_data.setdefault(server_id, {})[user_id] = user_data
    save_server_data(server_id, server_data)
    await interaction.send(', '.join(results) + ' 광물들을 획득하였습니다.')
    print(', '.join(results) + ' 광물들을 획득하였습니다.')


# 'myminerals' 슬래시 명령어 구현
@bot.hybrid_command(name='myminerals', description="내가 획득한 광물 확인")
async def myminerals(interaction: discord.Interaction):
    server_id = str(interaction.guild.id)
    user_id = str(interaction.author.id)
    server_data = load_server_data()

    user_data = server_data.get(server_id, {}).get(user_id, [])
    if user_data:
        await interaction.send(f"{interaction.author.display_name}님의 획득한 광물: {', '.join(user_data)}")
    else:
        await interaction.send("아직 광물을 획득하지 않았습니다.")


@bot.hybrid_command(name='roll', description="주사위 굴리기")
async def roll(interaction: discord.Interaction):
    randnum = random.randint(1, 6)  # 1이상 6이하 랜덤 숫자를 뽑음
    await interaction.send(f'주사위 결과는 {randnum} 입니다.')
    print(f'주사위 결과는 {randnum} 입니다.')


@bot.hybrid_command(name='프로필', description="프로필")
async def embed(interaction: discord.Interaction):
    embed = discord.Embed(title=f"shii-bot <:__:1201865120368824360>", description="made by 보란이", color=0xFFB2F5)
    embed.add_field(name="사용가능 명령어", value="/say, /embed, /hello, /bye, /copy, /clear, /roll, /mining, /game 등등등...",
                    inline=False)
    embed.add_field(name="사용법", value="/를 사용하여 불러주세요!", inline=False)
    embed.add_field(name="호스팅", value="구글 클라우드 플렛폼(GCP)", inline=False)
    embed.add_field(name="패치버전", value="v2.8.2", inline=False)
    embed.set_footer(
        text="개인 정보 처리 방침: https://github.com/boranloves/shii-bot-discord/blob/main/%EA%B0%9C%EC%9D%B8%EC%A0%95%EB%B3%B4%EC%B2%98%EB%A6%AC%EB%B0%A9%EC%B9%A8.txt")
    await interaction.send(embed=embed)


@bot.hybrid_command(name='타이머', description="타이머 실행(베타)")
async def set_time(interaction: discord.Interaction, seconds: int, message='타이머 종료!'):
    await interaction.send(f'{seconds}초 후에 알림이 옵니다.')
    await asyncio.sleep(seconds)
    await interaction.send(message)


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


@bot.hybrid_command(name='help_shii', description="시이봇 메뉴얼")
async def help(interaction: discord.Interaction):
    embed = discord.Embed(title="시이봇 명령어", color=0xFFB2F5)
    embed.add_field(name="/알려주기", value="시이봇 전용 명령어 입니다. 명령어뒤에 키워드와 설명을 입력하여 시이봇을 학습시킬 수 있습니다.", inline=False)
    embed.add_field(name="시이야", value="시이봇 전용 명령어 입니다. 알려주기로 학습한 키워드와 설명을 말합니다.", inline=False)
    embed.add_field(name="/번역", value="파파고 번역기능 입니다. 앞에는 시작언어, 뒤에는 도착언어를 입력하고, 마지막에 단어를 적어주세요", inline=False)
    embed.add_field(name="/패치노트", value="시이봇의 패치노트를 볼 수 있는 명령어 입니다.", inline=False)
    embed.add_field(name="/네이버검색, /카카오검색, /유튜브검색", value="검색기능입니다. 명령어뒤 검색할 키워드를 입력해주세요.", inline=False)
    embed.add_field(name="/계산", value="간단한 계산기 입니다. 명령어뒤 수식을 입력해주세요.", inline=False)
    embed.add_field(name="/음성채널입장, /음성채널퇴장", value="음성채널 입장 및 퇴장 기능입니다. 음성채널 전용기능은 개발할 예정입니다.", inline=False)
    embed.add_field(name="/인원통계", value="서버 인원통계 기능 입니다. 현재 개발중에 있습니다.", inline=False)
    embed.add_field(name="/임베드생성", value="임베드를 생성하는 기능 입니다. 총 2줄로 1,2번째는 타이틀과 설명, 3,4번째는 2번째줄 이름과 설명입니다.", inline=False)
    embed.add_field(name="/타이머", value="간단한 타이머 기능 입니다. 명령어뒤에 초를 입력하고, 선택적으로 메세지를 입력할 수 있습니다.", inline=False)
    embed.add_field(name="/프로필", value="시이봇의 프로필을 볼 수 있는 명령어 입니다.", inline=False)
    embed.add_field(name="/hello, /bye", value="간단한 인사 입니다.", inline=False)
    embed.add_field(name="/clear", value="메세지를 지우는 기능 입니다. 명령어뒤에 지울 메세지의 수를 입력할 수 있습니다.", inline=False)
    embed.add_field(name="/copy", value="메세지를 따라 쓰는 기능입니다. 명령어뒤에 따라쓸 메세지의 내용을 입력할 수 있습니다.", inline=False)
    embed.add_field(name="/game", value="가위바위보 미니게임 입니다. 명령어뒤에 가위, 바위, 보 중 하나를 골라 쓸 수 있습니다.", inline=False)
    embed.add_field(name="/mining", value="광질 미니게임 입니다. 3개의 광물이 무작위로 나옵니다.", inline=False)
    embed.add_field(name="/roll", value="주사위 미니게임 입니다. 간단한 주사위 굴리기를 할 수 있습니다.", inline=False)
    embed.add_field(name="/say", value="개발이 중지된 구 시이봇 전용 명령어 입니다. 명령어뒤 단어를 입력해 시이봇에게 답변을 받을 수 있습니다.", inline=False)
    embed.set_footer(text="버전: v2.8.2")
    await interaction.send(embed=embed)


@bot.hybrid_command(name="패치노트", description="시이봇 패치노트 보기")
async def pt(interaction: discord.Interaction):
    embed = discord.Embed(title="v2.8.2 패치노트", color=0xFFB2F5)
    embed.add_field(name="신규기능", value="베타 커멘드 시이야, 알려주기 추가 및 say 커멘드 개발 종료, 기타 버그 수정", inline=False)
    embed.add_field(name="버그 수정", value="DM에서 /clear 사용시 '잠시만 기다려주세요','DM에서는 사용할 수 없는 명령어 입니다!' 문구가 3초뒤 안 지워지는 버그 수정", inline=False)
    await interaction.send(embed=embed)


@bot.hybrid_command(name='알려주기', description='시이봇에게 많은걸 알려주세요!(베타)')
async def tell(interaction: discord.Interaction, keyword: str, *, description: str):
    bot_info = load_bot_info()

    # 이미 존재하는 키워드인지 확인 후 저장
    if keyword not in bot_info:
        bot_info[keyword] = {
            'description': description,
            'author_nickname': interaction.author.display_name
        }
        await interaction.send(f"{keyword}에 대한 설명이 저장되었습니다.")
    else:
        await interaction.send(f"{keyword}는 이미 존재하는 키워드입니다. 저장되지 않았습니다.")
    # 정보 저장
    save_bot_info(bot_info)


@bot.hybrid_command(name='시이야', description='shii-bot 전용 명령어(베타)')
async def say1(interaction: discord.Interaction, keyword: str):
    bot_info = load_bot_info()
    info = bot_info.get(keyword)

    if info:
        author_nickname = info['author_nickname']
        description = info['description']
        response = f"{description}\n```{keyword}의 답변이예욧! {author_nickname}이(가) 알려줬어요!```"
    else:
        response = "그 키워드에 대한 설명을 찾을 수 없어요."

    await interaction.send(response)


@bot.hybrid_command(name='say', description="shii-bot 전용 명령어(구)")
async def say(interaction: discord.Interaction, text: str):
    print(interaction, text)
    question = text
    answer = get_answer(question)
    await interaction.send(answer)
    print(answer)


def get_day_of_week():
    weekday_list = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']

    weekday = weekday_list[datetime.today().weekday()]
    date = datetime.today().strftime("%Y년 %m월 %d일")
    result = '{}({})'.format(date, weekday)
    return result


def get_time():
    return datetime.today().strftime("%H시 %M분 %S초")


def get_answer(text):
    trim_text = text.replace(" ", "")

    answer_dict = {
        'hello': '안녕하세욧!',
        '안녕': '안녕하세요. 시이입니다!',
        '누구야': '안녕하세요. shii입니다!',
        '요일': ':calendar: 오늘은 {}입니다'.format(get_day_of_week()),
        '시간': ':clock9: 현재 시간은 {}입니다.'.format(get_time()),
        '코딩': '코딩은 재밌어요',
        '게임': '게임하면 또 마크랑 원신을 빼놀수 없죠!',
        'ㅋㅋㅋ': 'ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ',
        '이스터에그': '아직 방장님이 말 하지 말라고 했는데....아직 비밀이예욧!',
        '버전정보': '패치버전 v2.7.1',
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
        '1+1은?': 'ㅏ? ERROR 시스탬을 정지합니다아(삐삐삐삐삐)',
        '왭연동': '사이트 및 뉴스 연동은 현재는 업데이트 일정에 없습니다',
        '애교': '이이잉...시져ㅕㅕㅕ',
        '야근': '설마...야근 시킬 생각은 아니시죠?',
        '아이싯떼루': '웩',
        '애니': '~개발자왈~ 백성녀와 흑목사는 꼭 봐라',
        '축구경기': '축구 경기 연동 기능은 현재 개발중 입니다. 빠른 시일내에 완성 하겠습니다!',
        'help': '저와 대화 하실려면 /say 뒤에 질문을 넣어 불러주세요!',
        '음악': '우리 개발자님은 류현준님의 노래를 좋아한데요. 네, TMI네용',
        'GCP': '지금 시이봇은 GCP에서 실행되고 있습니다!',
        '뭐야': '뭐지?',
        '잘가': '잘가요!',
        '뭐들어?': '앗, 류현준님의 난간이욧!',
        '베타커멘드': '베타 커멘드는 현재 태스트 중인 커멘드 입니다! 언제 생기고 사라질지 모르죠',
        '시이이모지': "<:__:1201865120368824360>"
    }

    if trim_text == '' or None:
        return "알 수 없는 단어입니다. 답변을 드릴 수 없을 것 같아요ㅠ"
    elif trim_text in answer_dict.keys():
        return answer_dict[trim_text]
    else:
        for key in answer_dict.keys():
            if key.find(trim_text) != -1:
                return "연관 단어 [" + key + "]에 대한 답변이에요.\n" + answer_dict[key]

        for key in answer_dict.keys():
            if answer_dict[key].find(trim_text) != -1:
                return "질문과 가장 유사한 질문 [" + key + "]에 대한 답변이에요.\n" + answer_dict[key]

    return text + "은(는) 없는 질문입니다."


bot.run()
