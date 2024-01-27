import discord
from discord.ext import commands
from datetime import datetime
import random
import json
import os

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


@bot.hybrid_command(name='출첵', description="출첵!")
async def attendance(interaction: discord.Interaction):
    user_id = str(interaction.author.id)

    # 출석 정보 로드
    with open(attendance_file, 'r') as file:
        all_attendance_data = json.load(file)

    # 서버마다 다른 출석 데이터 가져오기
    server_attendance_data = all_attendance_data.get(str(interaction.guild.id), {})

    # 이미 출석한 경우
    if user_id in server_attendance_data:
        await interaction.send(f'{interaction.author.mention} 이미 출석하셨습니다.')
    else:
        # 출석 기록
        server_attendance_data[user_id] = True

        # 출석 메시지 전송
        await interaction.send(f'{interaction.author.mention} 출석하셨습니다!')

        # 서버마다 다른 출석 데이터 갱신
        all_attendance_data[str(interaction.guild.id)] = server_attendance_data

        # 출석 정보 저장
        with open(attendance_file, 'w') as file:
            json.dump(all_attendance_data, file)

# 누적 출석 수 확인 명령어
@bot.hybrid_command(name='누적출석수', description="출첵 현황 보기")
async def total_attendance(interaction: discord.Interaction):
    # 서버마다 다른 출석 데이터 가져오기
    with open(attendance_file, 'r') as file:
        all_attendance_data = json.load(file)

    server_attendance_data = all_attendance_data.get(str(interaction.guild.id), {})

    # 누적 출석 수 계산
    total_attendance = sum(server_attendance_data.values())

    await interaction.send(f'{interaction.author.mention} {interaction.guild.name}의 누적 출석 수: {total_attendance}')


@bot.hybrid_command(name='hello', description="hi!")
async def hello(interaction: discord.Interaction):
    await interaction.reply(content="하이")


@bot.hybrid_command(name='bye', description="bye!")
async def bye(interaction: discord.Interaction):
    await interaction.reply(content="빠이")


@bot.hybrid_command(name='copy', description="write along the message")
async def copy(interaction: discord.Interaction, text1: str):
    await interaction.send(text1)


@bot.hybrid_command(name='clear', description="message cleaning")
async def clear(interaction: discord.Interaction, amount: int):
    if not interaction.guild:
        await interaction.send("DM에서는 사용이 불가능한 명령어입니다!")
        return

    channel = interaction.channel
    await channel.purge(limit=amount)
    await interaction.channel.send(f"{amount}개의 메시지를 삭제했어요!")
    print(f"{amount}개의 메시지를 삭제했어요!")


@bot.hybrid_command(name='start', description="음성 채널 입장")
async def start(interaction: discord.Interaction):
    if interaction.author.voice and interaction.author.voice.channel:
        channel = interaction.author.voice.channel
        await interaction.send(f"봇이 {channel} 채널에 입장합니다.")
        await channel.connect()
        print(f"음성 채널 정보: {interaction.author.voice}")
        print(f"음성 채널 이름: {interaction.author.voice.channel}")
    else:
        await interaction.send("음성 채널에 유저가 존재하지 않습니다. 1명 이상 입장해 주세요.")


@bot.hybrid_command(name='stop', description="음성 채널 퇴장")
async def stop(interaction: discord.Interaction):
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


@bot.hybrid_command(name='embed', description="프로필")
async def embed(interaction: discord.Interaction):
    embed = discord.Embed(title="shii-bot", description="made by 보란이", color=0xAAFFFF)
    embed.add_field(name="사용가능 명령어", value="/say, /embed, /hello, /bye, /copy, /clear, /roll, /mining, /game, /출첵, /누적 출석 수", inline=False)
    embed.add_field(name="사용법", value="/를 사용하여 불러주세요!", inline=False)
    embed.add_field(name="호스팅", value="구글 클라우드 플렛폼(GCP)", inline=False)
    embed.add_field(name="패치버전", value="v2.2.1-aplha", inline=False)
    embed.set_footer(text="개인 정보 처리 방침: https://github.com/boranloves/shii-bot-discord/blob/main/%EA%B0%9C%EC%9D%B8%EC%A0%95%EB%B3%B4%EC%B2%98%EB%A6%AC%EB%B0%A9%EC%B9%A8.txt")
    await interaction.send(embed=embed)


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
        '버전정보': '패치버전 2.2.1',
        '패치노트': '패치노트 2.2.1 신규기능: 출석 기능 및 누석 출석 수 커멘드 추가',
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
        '뭐들어?': '앗, 류현준님의 난간이욧!'
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


bot.run(TOKEN)
