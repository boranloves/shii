import discord 
from datetime import datetime
import discord
from discord.ext import commands
from datetime import datetime
import os
import random




TOKEN = os.environ['TOKEN']


intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("/"),
    description='Relatively simple music bot example',
    intents=intents,
)


@bot.event
async def on_ready():
    print(f'{bot.user}이(가) 로그인했습니다.')
    keep_alive()


# /embed 명령어에 대한 코드
@bot.command()
async def embed(ctx):
    embed = discord.Embed(title="shii-bot", description="made by 보란이", color=0xAAFFFF)
    embed.add_field(name="사용가능 명령어", value="/s, /embed, /hello, /bye, /c, /clear, /roll, /mining, /game", inline=False)
    embed.add_field(name="사용법", value="/를 사용하여 불러주세요!", inline=False)
    embed.set_footer(text="개발중")
    embed.set_footer(text="패치버전: 1.1.0")
    await ctx.send(embed=embed)


@bot.command()
async def roll(ctx):
    randnum = random.randint(1, 6)  # 1이상 6이하 랜덤 숫자를 뽑음
    await ctx.send(f'주사위 결과는 {randnum} 입니다.')


@bot.command()
async def mining(ctx):
    minerals = ['다이아몬드', '루비', '에메랄드', '자수정', '철', '석탄']
    weights = [1, 3, 6, 15, 25, 50]
    results = random.choices(minerals, weights=weights, k=1)  # 광물 5개를 가중치에 따라 뽑음
    await ctx.send(', '.join(results) + ' 광물들을 획득하였습니다.')


# 음성채널입장 명령어에 대한 코드
@bot.command()
async def start(ctx):
    if ctx.author.voice and ctx.author.voice.channel:
        channel = ctx.author.voice.channel
        await ctx.send(f"봇이 {channel} 채널에 입장합니다.")
        await channel.connect()
        print(f"음성 채널 정보: {ctx.author.voice}")
        print(f"음성 채널 이름: {ctx.author.voice.channel}")
    else:
        await ctx.send("음성 채널에 유저가 존재하지 않습니다. 1명 이상 입장해 주세요.")


@bot.command()
async def game(ctx, user: str):  # user:str로 !game 다음에 나오는 메시지를 받아줌
    rps_table = ['가위', '바위', '보']
    bot = random.choice(rps_table)
    result = rps_table.index(user) - rps_table.index(bot)  # 인덱스 비교로 결과 결정
    if result == 0:
        await ctx.send(f'{user} vs {bot}  비겼당.')
    elif result == 1 or result == -2:
        await ctx.send(f'{user} vs {bot}  졌당.')
    else:
        await ctx.send(f'{user} vs {bot}  내가 이겼당~.')


# 음성채널퇴장 명령어에 대한 코드
@bot.command()
async def stop(ctx):
    try:
        # 음성 채널에서 봇을 내보냅니다.
        await ctx.voice_client.disconnect()
        await ctx.send(f"봇을 {ctx.author.voice.channel} 에서 내보냈습니다.")
    except IndexError as error_message:
        print(f"에러 발생: {error_message}")
        await ctx.send(f"{ctx.author.voice.channel}에 유저가 존재하지 않거나 봇이 존재하지 않습니다.\\n다시 입장후 퇴장시켜주세요.")
    except AttributeError as not_found_channel:
        print(f"에러 발생: {not_found_channel}")
        await ctx.send("봇이 존재하는 채널을 찾는 데 실패했습니다.")


# clear 명령어에 대한 코드
@bot.command()
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f"{amount}개의 메시지를 삭제했어요!")


# c 명령어에 대한 코드
@bot.command()
async def c(ctx, text2):
    await ctx.send(text2)


# hello 명령어에 대한 코드
@bot.command()
async def hello(ctx):
    await ctx.reply('하이!')


# bye 명령어에 대한 코드
@bot.command()
async def bye(ctx):
    await ctx.reply('ㅃ2')


# s 명령어에 대한 코드
@bot.command()
async def s(ctx, text1):
    print(ctx, text1)
    question = text1
    # 사용자 정의 함수 get_answer를 사용하여 답변을 받아옵니다.
    answer = get_answer(question)
    await ctx.send(answer)
    print(answer)


# 일부 유틸리티 함수
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
        '버전정보': '패치버전 1.1.0',
        '패치노트': '패치노트 1.1.0 신규기능: 코드 구조 교체 작업 밎 명령어 변경, 명령어 추가 및 대화 추가',
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
        '음악': '우리 개발자님은 류현준님의 노래를 좋아한데요. 네, TMI네용'
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



if __name__ == "__main__":
    bot.run(TOKEN)
