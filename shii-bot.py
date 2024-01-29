import discord
from discord.ext import commands, tasks
from datetime import datetime
import random
import json
import os
import asyncio
from youtube_search import YoutubeSearch
import sympy
import requests
from PIL import Image, ImageDraw, ImageFont
import io
import string


class Bot(commands.Bot):
    def __init__(self, intents: discord.Intents, **kwargs):
        super().__init__(command_prefix="/", intents=intents, case_insensitive=True)

    async def on_ready(self):
        print(f"Logged in as {self.user}")
        await self.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="류현준 난간"))
        await self.tree.sync()

        if not os.path.exists(attendance_file):
            with open(attendance_file, 'w') as file:
                json.dump({}, file)


attendance_file = 'attendance.json'
intents = discord.Intents.all()
bot = Bot(intents=intents)
NAVER_CAPTCHA_API_KEY = '1'
NAVER_CAPTCHA_SECRET_KEY = '1'
NAVER_CAPTCHA_API_URL = 'https://openapi.naver.com/v1/captcha/nkey?code='
NAVER_CAPTCHA_CHECK_URL = 'https://openapi.naver.com/v1/captcha/ncaptcha.bin?key='


def generate_captcha():
    width, height = 200, 100
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)

    font = ImageFont.load_default()  # 기본 폰트 사용
    captcha_text = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

    draw.text((10, 30), captcha_text, font=font, fill='black')

    image_bytes = io.BytesIO()
    image.save(image_bytes, format='PNG')
    return image_bytes.getvalue(), captcha_text


# Command for captcha authentication and role assignment
@bot.hybrid_command(name='캡챠인증', description="네이버 api 이미지 캡챠 인증(베타)")
async def authenticate(interaction: discord.Interaction):
    # Discord 사용자에게 DM으로 캡챠 이미지 전송
    captcha_image, captcha_text = generate_captcha()
    await interaction.send(f"DM으로 캡챠 이미지가 발송 되었습니다. 1분 내로 입력해 주시기 바랍니다.")
    await interaction.author.send(f"이미지 캡챠를 풀어주세요. 1분 내로 이미지에 보이는 문자를 입력하세요.")
    await interaction.author.send(file=discord.File(io.BytesIO(captcha_image), filename='captcha.png'))

    # 사용자로부터 응답 대기
    def check(message):
        return message.author == interaction.author and message.channel.type == discord.ChannelType.private

    try:
        user_response = await bot.wait_for('message', timeout=60.0, check=check)
    except TimeoutError:
        await interaction.author.send("시간이 초과되었습니다. 인증이 취소되었습니다.")
        return

    # 사용자 응답과 캡챠 텍스트를 네이버 API로 검증
    naver_captcha_key_response = requests.get(NAVER_CAPTCHA_API_URL + captcha_text,
                                              headers={'X-Naver-Client-Id': NAVER_CAPTCHA_API_KEY,
                                                       'X-Naver-Client-Secret': NAVER_CAPTCHA_SECRET_KEY})
    naver_captcha_key_json = naver_captcha_key_response.json()

    naver_captcha_check_response = requests.get(NAVER_CAPTCHA_CHECK_URL + naver_captcha_key_json['key'],
                                                headers={'X-Naver-Client-Id': NAVER_CAPTCHA_API_KEY,
                                                         'X-Naver-Client-Secret': NAVER_CAPTCHA_SECRET_KEY})

    if naver_captcha_check_response.status_code == 200:
        await interaction.author.send("인증이 완료되었습니다. 원하는 작업을 계속하세요(베타 태스트 중).")
    else:
        await interaction.author.send("인증에 실패했습니다. 다시 시도해주세요.")



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
    if not interaction.guild:
        await interaction.send("DM에서는 사용이 불가능한 명령어입니다!")
        return

    await interaction.purge(limit=amount)
    await interaction.send(f"{amount}개의 메시지를 삭제했어요!")
    print(f"{amount}개의 메시지를 삭제했어요!")


@bot.hybrid_command(name='음성채널입장', description="음성 채널 입장")
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
    embed = discord.Embed(title=text, description=text1, color=0xAAFFFF)
    embed.add_field(name=text2, value=text3, inline=False)
    await interaction.send(embed=embed)


@bot.hybrid_command(name='음성채널퇴장', description="음성 채널 퇴장")
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
    minerals = ['다이아몬드', '루비', '에메랄드', '자수정', '철', '석탄']
    weights = [1, 3, 6, 15, 25, 50]
    results = random.choices(minerals, weights=weights, k=3)  # 광물 3개를 가중치에 따라 뽑음
    await interaction.send(', '.join(results) + ' 광물들을 획득하였습니다.')
    print(', '.join(results) + ' 광물들을 획득하였습니다.')


@bot.hybrid_command(name='roll', description="주사위 굴리기")
async def roll(interaction: discord.Interaction):
    randnum = random.randint(1, 6)  # 1이상 6이하 랜덤 숫자를 뽑음
    await interaction.send(f'주사위 결과는 {randnum} 입니다.')
    print(f'주사위 결과는 {randnum} 입니다.')


@bot.hybrid_command(name='프로필', description="프로필")
async def embed(interaction: discord.Interaction):
    embed = discord.Embed(title="shii-bot", description="made by 보란이", color=0xAAFFFF)
    embed.add_field(name="사용가능 명령어", value="/say, /embed, /hello, /bye, /copy, /clear, /roll, /mining, /game 등등등...", inline=False)
    embed.add_field(name="사용법", value="/를 사용하여 불러주세요!", inline=False)
    embed.add_field(name="호스팅", value="구글 클라우드 플렛폼(GCP)", inline=False)
    embed.add_field(name="패치버전", value="v2.5.0", inline=False)
    embed.set_footer(text="개인 정보 처리 방침: https://github.com/boranloves/shii-bot-discord/blob/main/%EA%B0%9C%EC%9D%B8%EC%A0%95%EB%B3%B4%EC%B2%98%EB%A6%AC%EB%B0%A9%EC%B9%A8.txt")
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

    await interaction.send(f'총 인원: {total_members}\n각 역할별 인원: {role_stats}')


@bot.hybrid_command(name='say', description="shii-bot 전용 명령어")
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
        '안녕': '안녕하세요. shii입니다!',
        '누구야': '안녕하세요. shii입니다!',
        '요일': ':calendar: 오늘은 {}입니다'.format(get_day_of_week()),
        '시간': ':clock9: 현재 시간은 {}입니다.'.format(get_time()),
        '코딩': '코딩은 재밌어요',
        '게임': '게임하면 또 마크랑 원신을 빼놀수 없죠!',
        'ㅋㅋㅋ': 'ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ',
        '이스터에그': '아직 방장님이 말 하지 말라고 했는데....아직 비밀이예욧!',
        '버전정보': '패치버전 v2.5.0',
        '패치노트': '패치노트 v2.5.0 신규기능: 캡챠인증 베타 커멘드 추가',
        '과자': '음...과자하니까 과자 먹고 싶당',
        '뭐해?': '음.....일하죠 일! 크흠',
        '음성채널': '음성채널는 현재 방장이 돈이 없어서 불가능 합니다ㅠㅠ',
        '이벤트': '흐음..이벤트는 아직 없어요ㅠㅠ',
        '웃어': '히힛 (　＾▽＾)',
        '맴매': '흐에에엥ㅠㅠㅜ방장님! 도와주세여(/´△`＼)',
        '아재게그': '(방장님은 이걸 왜 시킨거야)왕이 넘어지면? 킹콩!',
        '옥에티': '옥에티가 있을것같아요? 네, 아마 있을거예요 방장님이 아직 초짜라',
        '잔소리해줘': '잔소리는 나쁜거예요 알겠어요?',
        '유튜브': '현재 유튜브 연동 기능은 검토중 입니다!',
        '크레딧': '전부다 보란이(그렇게 써있음 ㅇㅇ)',
        'GPT': '시험 태스트 결과 현재로썬 적용이 불가 합니다 ㅠㅠ',
        '구멍': '구멍',
        '자가복제': '!자가복제!',
        '방장님': '방장님이요? 좀, 쪼잔하긴해요(소곤소곤)',
        '종': '댕댕대에에엥',
        '할말없어?': '할말이요? 할말이요? 할말이요? 할말이요? 할말이요? 할말이요? 없어욧!',
        '1+1은?': 'ㅏ? ERROR 시스탬을 정지합니다아(삐삐삐삐삐)',
        '왭연동': '사이트 및 뉴스 연동은 현재는 업데이트 일정에 없습니다',
        '애교': '이이잉...시져ㅕㅕㅕ',
        '야근': '설마...야근 시킬 생각은 아니시죠?',
        '아이싯떼루': '웩',
        '애니': '~개발자왈~ 백성녀와 흑목사는 꼭 봐라',
        '축구경기': '축구 경기 연동 기능은 현재 개발중 입니다. 빠른 시일내에 완성 하겠습니다!',
        'help': '저와 대화 하실려면 /s 뒤에 질문을 넣어 불러주세요!',
        '음악': '우리 개발자님은 류현준님의 노래를 좋아한데요. 네, TMI네용',
        'GCP': '드.디.어! shii-bot이 24시간 돌아간답니다!',
        '뭐야': '뭐지?',
        '잘가': '잘가요!',
        '뭐들어?': '앗, 류현준님의 난간이욧!',
        '베타커멘드': '베타 커멘드는 현재 태스트 중인 커멘드 입니다! 언제 생기고 사라질지 모르죠'
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


bot.run(토큰)
