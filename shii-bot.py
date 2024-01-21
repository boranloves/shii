import discord 
from datetime import datetime
from discord import message
import os
import sys

print("Starting...")

TOKEN = os.environ['TOKEN']

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Login bot: {self.user}')
        print(sys.version)
        await self.change_presence(status=discord.Status.online, activity=discord.Game("출근"))
        keep_alive()
        print('keep_alive() started')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('!'):
            # '!'로 시작하는 메시지 처리
            question = message.content[1:].strip()
            answer = self.get_answer(question)
            await message.channel.send(answer)

    def get_day_of_week(self):
        weekday_list = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']

        weekday = weekday_list[datetime.today().weekday()]
        date = datetime.today().strftime("%Y년 %m월 %d일")
        result = '{}({})'.format(date, weekday)
        return result

    def get_time(self):
        return datetime.today().strftime("%H시 %M분 %S초")

    def get_answer(self, text):
        trim_text = text.replace(" ", "")

        answer_dict = {
            '안녕': '안녕하세요. shii입니다!',
            '요일': ':calendar: 오늘은 {}입니다'.format(self.get_day_of_week()),
            '시간': ':clock9: 현재 시간은 {}입니다.'.format(self.get_time()),
            '유엔': '병신새끼',
            '코딩': '코딩은 재밌어요',
            '쿠키런:모험의탑': '지금 방장님이 쿠키런:모험의탑 CBT 초대권을 뿌리고 있어요! 3개 뿐이니 빨리빨리 DM보내주세요^~^',
            '게임': '게임하면 또 마크랑 원신을 빼놀수 없죠!',
            'ㅋㅋㅋ': 'ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ',
            '이스터에그': '아직 방장님이 말 하지 말라고 했는데....아직 비밀이예욧!',
            '버전정보': '패치버전 1.0.2',
            '패치노트': '패치노트 1.0.2 신규기능: 오프라인 기능 추가, 단어 추가',
            '과자': '음...과자하니까 과자 먹고 싶당',
            '뭐해?': '음.....일하죠 일! 크흠',
            '음성채널': '음성채널 지원 여부는 현재 검토중 입니다!',
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
            '애니': '애니는 못참죠!'

        }

        if trim_text == '' or None:
            return "알 수 없는 질의입니다. 답변을 드릴 수 없을것같아요ㅠ"
        elif trim_text in answer_dict.keys():
            return answer_dict[trim_text]
        else:
            for key in answer_dict.keys():
                if key.find(trim_text) != -1:
                    return "연관 단어 [" + key + "]에 대한 답변이예요.\n" + answer_dict[key]

            for key in answer_dict.keys():
                if answer_dict[key].find(text[1:]) != -1:
                    return "질문과 가장 유사한 질문 [" + key + "]에 대한 답변이예요.\n" + answer_dict[key]

        return text + "은(는) 없는 질문입니다."


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(TOKEN)
