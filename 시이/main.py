import collections
import discord
from discord.app_commands import describe
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import json
import time
import os
import asyncio
from koreanbots.model import KoreanbotsBot
from youtube_search import YoutubeSearch
import sympy
import requests
from koreanbots.integrations.discord import DiscordpyKoreanbots
import random
import re
import math
from korcen import korcen
from collections import Counter
from discord import Interaction, InteractionType, embeds, mentions, ui, ButtonStyle, SelectOption
from PIL import Image

bser_api_key = ""
json_file_path = 'bot_info.json'
attendance_file = 'attendance.json'
naver_client_id = ''
KAKAO_API_KEY = ''
naver_client_secret = ''
c = 'server_data.json'
happiness_file_path = 'happiness.json'
mamo_file = 'mamo.json'
lv_file = 'lv.json'
SETTINGS_FILE = "bot_settings.json"
count_FILE = 'count.json'
mining_limit = 10
capital_file = '자본.json'
stocks_file = '주식.json'
user_stocks_file = '사용자_주식.json'
previous_value = {
    '이시가전': 0,
    '고구우글': 0,
    '아마준': 0,
    '나노소포트': 0,
    '불화': 0,
    '시이전자': 0
}
sex = []
wordshii = [
    '넹!', '왜 그러세용?', '시이예용!', '필요 하신거 있으신가요?', '뭘 도와드릴까요?', '반가워용', '저 부르셨나요?',
    '왜요용', '잉', '...?', '네?', '/가르치기로 단어를 알려 줄 수 있어요!'
]
baddword = ['확마', '아놔', '뭐레', '이게', '나쁜말은 싫어요ㅠ']
bad = [
    '씨발', '시발', '병신', '지랄', '좆', '염병', '또라이', '급식충', '닥쳐', '등신', '대가리', '싸가지',
    '찐따', '존나', '새끼'
]
catss = ['냥!', "냐앙", "냥냥!"]
tkak = [
    '네 주인님!', '주인님 왜 그러시죠?', '주인님 안녕하세요!', '주인님 필요하신거 있으신가요?', '주인님 뭘 도와드릴까요?',
    '주인님 반가워요!', '주인님 저 부르셨나요?'
]
start_time = datetime.utcnow()
why = ['으에?', '몰?루', '왜요용', '잉', '...?', '몰라여', '으에.. 그게 뭐징?', '네?']
active_polls = {}
voted_users = {}


class Bot(commands.Bot):

    def __init__(self, **kwargs):
        super().__init__(command_prefix=["/", "!", "시이 "],
                         intents=intents,
                         case_insensitive=True,
                         sync_command=True,
                         help_command=None)
        kb = DiscordpyKoreanbots(
            self,
            
            run_task=True)

    async def on_ready(self):
        print(f"Logged in as {self.user}")
        await self.change_presence(status=discord.Status.online)
        await bot.change_presence(
            activity=discord.CustomActivity(name='류현준 난간 듣는 중', type=5))
        await self.tree.sync()



        ss = self.guilds
        sss = bot.commands
        print(sss)
        print(ss)
        simulate_stock_market.start()
        if not os.path.exists(json_file_path):
            with open(json_file_path, 'w') as file:
                json.dump({}, file)


def open_cer_db():
    try:
        with open("cer.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_cer_db(cer):
    with open("cer.json", "w") as f:
        json.dump(cer, f, indent=4)


def ok_cer(user_id: str):
    cer = open_cer_db()
    if str(user_id) in cer:
        return True
    else:
        return False


class hogam:
    def save(self, hogam):
        with open("hogam.json", "w") as f:
            json.dump(hogam, f, indent=4)

    def load(self):
        try:
            with open("hogam.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def cheak(self, user_id: str):
        hogamdo = hogam.load(self)
        if user_id in hogamdo:
            return hogamdo[user_id]
        else:
            hogamdo[user_id] = 0
            hogam.save(self, hogamdo)
            return hogamdo[user_id]

    def add(self, user_id: str, int: int):
        hogamdo = hogam.load(self)
        user_hogamdo = hogam.cheak(self, user_id)

        hogamdo[user_id] = hogamdo[user_id] + int
        if hogamdo[user_id] < 0:
            hogamdo[user_id] = 0

        hogam.save(self, hogamdo)
        return hogamdo[user_id]



class Dropdown(discord.ui.Select):

    def __init__(self, author: str, user: str, guild: str):
        self.user_id = user
        self.guild_id = guild
        self.author = author
        options = [
            discord.SelectOption(label="상점 리뉴얼 준비중입니다!",
                                 description="coming soon"),
        ]

        super().__init__(
            placeholder="아이템 메뉴",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        if str(interaction.user.id) != str(self.author):
            await interaction.response.send_message(
                "죄송합니다. 이 명령어를 사용할 권한이 없습니다.", ephemeral=True)  # noqa
            return
        if self.values[0] == "상점 리뉴얼 준비중입니다!":
            await interaction.response.send_message(
                "상점 리뉴얼 준비중입니다!", ephemeral=True)  # noqa


class D_Dropdown(discord.ui.Select):

    def __init__(self, author: str, user: str, guild: str):
        self.user_id = user
        self.guild_id = guild
        self.author = author
        options = [
            discord.SelectOption(label="어디서 많이 본 태풍성장의 비약",
                                 description="구매시 즉시 캐릭터의 레벨이 1 증가 합니다."),
            discord.SelectOption(
                label="어디서 많이 본 성장의 비약",
                description="구매시 즉시 캐릭터의 경험치가 레벨에 비례하여 증가 합니다.")
        ]

        super().__init__(
            placeholder="아이템 메뉴",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        if str(interaction.user.id) != str(self.author):
            await interaction.response.send_message(
                "죄송합니다. 이 명령어를 사용할 권한이 없습니다.", ephemeral=True)  # noqa
            return
        if self.values[0] == "어디서 많이 본 태풍성장의 비약: 100만 시이코인":
            capital = load_capital()
            print(self.user_id)
            print(self.guild_id)
            guild_id = str(self.guild_id)
            user_id = str(self.user_id)
            print(capital)
            if guild_id in capital and user_id in capital[guild_id]:
                if 1000000 <= capital[guild_id][user_id]:
                    capital[guild_id][user_id] -= 1000000
                    await interaction.response.send_message(
                        "어디서 많이 본 태풍성장의 비약을 구매하였습니다!")  # noqa

                else:
                    await interaction.response.send_message(
                        "시이코인이 부족하여 구매할 수 없습니다.")  # noqa
            else:
                await interaction.response.send_message(
                    "/내시이코인 을 사용하여 기초자금을 받고 시작해주세요!")  # noqa

        elif self.values[0] == "어디서 많이 본 성장의 비약: 10만 시이코인":
            capital = load_capital()
            print(self.user_id)
            print(self.guild_id)
            guild_id = str(self.guild_id)
            user_id = str(self.user_id)
            print(capital)
            if guild_id in capital and user_id in capital[guild_id]:
                if 100000 <= capital[guild_id][user_id]:
                    capital[guild_id][user_id] -= 100000
                    await interaction.response.send_message(
                        "어디서 많이 본 성장의 비약을 구매하였습니다!")  # noqa

                else:
                    await interaction.response.send_message(
                        "시이코인이 부족하여 주인님체 권을 구매할 수 없습니다.")  # noqa
            else:
                await interaction.response.send_message(
                    "/내시이코인 을 사용하여 기초자금을 받고 시작해주세요!")  # noqa


class MyModal(discord.ui.Modal, title="가르치기"):
    m_title = discord.ui.TextInput(style=discord.TextStyle.short,
                                   label="키워드",
                                   required=False,
                                   placeholder="시이에게 가르칠 키워드")

    m_description = discord.ui.TextInput(style=discord.TextStyle.long,
                                         label="단어",
                                         required=False,
                                         placeholder="시이가 키워드에 대답할 말",
                                         max_length=500,
                                         min_length=1)

    async def on_submit(self, interaction: discord.Interaction):
        keyword = self.m_title.value
        description = self.m_description.value

        # 가르치기 코드 추가
        bot_info = load_bot_info()
        server_id = str(interaction.guild_id)
        user_id = str(interaction.user.id)
        asw = description
        asw.replace('.', '')
        asw.replace(',', '')
        asw.replace(';', '')
        asw.replace(':', '')
        asw.replace(' ', '')
        for i in sex:
            if i in asw:
                embed = discord.Embed(title="그런 단어는 배우기 싫어요..",
                                      description="",
                                      color=0xFF2424)
                embed.set_footer(text="© Korcen 을 사용하여 검열하였습니다.")
                await interaction.response.send_message(embed=embed)  # noqa
                return
        if korcen.check(keyword) or korcen.check(description) or korcen.check(
                f"{keyword}{description}") or korcen.check(
                    f"{description}{keyword}"):

            embed = discord.Embed(title="그런 단어는 배우기 싫어요..",
                                  description="",
                                  color=0xFF2424)
            embed.set_footer(text="© Korcen 을 사용하여 검열하였습니다.")
            await interaction.response.send_message(embed=embed)  # noqa
            return
        if korcen.check(keyword) or korcen.check(asw) or korcen.check(
                f"{keyword}{asw}") or korcen.check(f"{asw}{keyword}"):
            embed = discord.Embed(title="그런 단어는 배우기 싫어요..",
                                  description="",
                                  color=0xFF2424)
            embed.set_footer(text="© Korcen 을 사용하여 검열하였습니다.")
            await interaction.response.send_message(embed=embed)  # noqa
            return
        if '@' in description or '@' in keyword:
            embed = discord.Embed(title="@을 추가하지 말아주세요...", color=0xFF2424)
            await interaction.response.send_message(embed=embed)  # noqa
            return
        if len(description) > 500:
            embed = discord.Embed(title="설명이 너무 길어서 모르겠어요...", color=0xFF2424)
            await interaction.response.send_message(embed=embed)  # noqa
            return
        if len(keyword) > 120:
            embed = discord.Embed(title="키워드가 너무 길어서 모르겠어요...", color=0xFF2424)
            await interaction.response.send_message(embed=embed)  # noqa
            return
        if len(description) <= 0 or len(keyword) <= 0:
            embed = discord.Embed(title="뭘..말해야 하는 거죠..?", color=0xFF2424)
            await interaction.response.send_message(embed=embed)  # noqa
            return
        if 'https://' in description or 'https://' in keyword or 'discord.gg' in description or 'discord.gg' in keyword or 'http://' in description or 'http://' in keyword or 'discord.com' in description or 'discord.com' in keyword:
            embed = discord.Embed(title="링크를 포함시키지 말아주세요...", color=0xFF2424)
            await interaction.response.send_message(embed=embed)  # noqa
            return
        if keyword not in bot_info:
            bot_info[keyword] = [{
                'description':
                description,
                'author_nickname':
                interaction.user.display_name
            }]
            hogamdos.cheak(user_id)
            hogamdos.add(user_id, 1)
            print(korcen.check(keyword))
            await interaction.response.send_message(
                f"오케! `{keyword}` 라고 하면\n`{description}` 라고 할게욧!\n-# :heart: + 1")  # noqa
        else:
            if len(bot_info[keyword]) >= 3:
                await interaction.response.send_message(
                    f"`{keyword}`는 이미 잘 알고 있어요...")  # noqa
            else:
                bot_info[keyword].append({
                    'description':
                    description,
                    'author_nickname':
                    interaction.user.display_name
                })
                hogamdos.cheak(user_id)
                hogamdos.add(user_id, 1)
                print(korcen.check(keyword))
                await interaction.response.send_message(
                    f"오케! `{keyword}` 라고 하면\n`{description}` 라고 할게욧!\n-# :heart: + 1")  # noqa
        # 정보 저장
        save_bot_info(bot_info)


class book_Dropdown(discord.ui.Select):

    def __init__(self, ints: int, data):
        self.data = data
        self.number = ints
        options = []

        for i in range(ints):
            options.append(
                discord.SelectOption(
                    label=f"{i+1}번째 책",
                    description=f"{data['items'][i]['title']}"))

        super().__init__(
            placeholder="검색 결과",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        ii = 0
        for i in range(self.number):
            if self.values[0] == f"{i+1}번째 책":
                ii = i
        if len(self.data['items'][ii]['description']) > 500:
            text = self.data['items'][ii]['description'][:500] + '...'
        else:
            text = self.data['items'][ii]['description']
        text2 = f"{self.data['items'][ii]['pubdate'][:4]}년 {self.data['items'][ii]['pubdate'][:6][4:]}월 {self.data['items'][ii]['pubdate'][:8][6:]}일"
        embed = discord.Embed(
            title=f"{self.data['items'][ii]['title']}",
            description=f"저자: {self.data['items'][ii]['author']}")
        embed.set_thumbnail(url=self.data['items'][ii]['image'])
        embed.add_field(name="줄거리", value=text, inline=False)
        embed.add_field(name="출판사",
                        value=self.data['items'][ii]['publisher'],
                        inline=True)
        embed.add_field(name="출판일", value=text2, inline=True)
        embed.add_field(name="가격",
                        value=f"{self.data['items'][ii]['discount']}원",
                        inline=True)
        embed.set_author(icon_url="https://shii.me/shiisss.wepb", name="검색결과")
        print(self.data['items'][ii])
        await interaction.response.send_message(embed=embed)


class damagochi():

    def load(self):
        try:
            with open("da_db.json", "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}

        return data

    def save(self, data):
        with open("da_db.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent="\t")

    def mak_db(self, user_id, name):
        ste = self.load()
        if str(user_id) not in ste:
            data = {
                "ch_num": 1,
                "name": name,
                "lv": 1,
                "exp": 0,
                "he": 50,
                "bgp": 75,
                "kgh": 100
            }
            ste[str(user_id)] = data
            self.save(ste)

        user_data = ste[str(user_id)]
        return user_data


class make_modal(discord.ui.Modal, title="캐릭터 등록"):
    m_name = discord.ui.TextInput(style=discord.TextStyle.short,
                                  label="이름",
                                  required=False,
                                  max_length=12,
                                  placeholder="ex): 시이")

    async def on_submit(self, interaction: discord.Interaction):
        name = self.m_name.value
        if korcen.check(name):
            return await interaction.response.send_message(
                "이름에 사용이 불가한 단어가 포함되어 있습니다.")
        damagochi().mak_db(user_id=str(interaction.user.id), name=name)
        user_data = damagochi().load()
        return await interaction.response.send_message(
            f"캐릭터 {user_data[str(interaction.user.id)]['name']} (이)가 등록 되었습니다!"
        )


global culls
culls = {}


class game_Dropdown(discord.ui.Select):

    def __init__(self, user: str):
        self.user = user
        options = []

        options.append(
            discord.SelectOption(label=f"1번째 게임", description=f"보물찾기"))

        super().__init__(
            placeholder="놀기",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):

        if str(interaction.user.id) != self.user:
            return await interaction.response.send_message(
                "이 기능은 사용자만 사용할 수 있습니다.", ephemeral=True)
        if self.values[0] == "1번째 게임":
            text = thajer()
            await interaction.response.send_message(content=text['text'])
            sta = damagochi().load()

            sta[str(interaction.user.id)]['exp'] += text['exp']

            damagochi().save(sta)


intents = discord.Intents.default()
bot = Bot(intents=intents)
hogamdos = hogam()
intents.message_content = True
intents.members = True
intents.dm_messages = True
'''
# Path: shii-4.0.0.py
'''


def thajer():
    num = random.randint(1, 500)
    if num <= 5:
        exp = 500
        text = "다이아몬드를 찾았다! exp +500"
        re = {'exp': exp, 'text': text}
        return re
    elif num <= 70:
        exp = 10
        text = "금을 찾았다! exp +100"
        re = {'exp': exp, 'text': text}
        return re
    elif num <= 250:
        exp = 50
        text = "철을 찾았다! exp +50"
        re = {'exp': exp, 'text': text}
        return re
    elif num <= 450:
        exp = 10
        text = "은을 찾았다! exp +10"
        re = {'exp': exp, 'text': text}
        return re
    else:
        exp = 0
        text = "아무것도 없다.. exp +0"
        re = {'exp': exp, 'text': text}
        return re


def open_hello_log():
    try:
        with open("hello_log1.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_hello_log(hello_log):
    with open("hello_log1.json", "w") as f:
        json.dump(hello_log, f, indent=4)


@bot.event
async def on_member_join(member):
    hello_log = open_hello_log()
    if str(member.guild.id) not in hello_log:
        return
    if not hello_log[str(member.guild.id)] == 'no':
        channel = bot.get_channel(hello_log[str(member.guild.id)])
        embed = discord.Embed(title=f"입장로그",
                              description=f"{member.mention}님이 입장했습니다.",
                              color=discord.Color.green())
        member = member
        embed.set_author(name=f"{member}", icon_url=member.avatar)
        embed.set_footer(
            text=
            f"{member.guild.name} | {datetime.today().strftime('%Y년 %H시 %M분 %S초')}"
        )
        await channel.send(embed=embed)


@bot.event
async def on_member_remove(member):
    hello_log = open_hello_log()
    if str(member.guild.id) not in hello_log:
        return
    if not hello_log[str(member.guild.id)] == 'no':
        channel = bot.get_channel(hello_log[str(member.guild.id)])
        embed = discord.Embed(title=f"입장로그",
                              description=f"{member.mention}님이 퇴장했습니다.",
                              color=discord.Color.red())
        member = member
        embed.set_author(name=f"{member}", icon_url=member.avatar)
        embed.set_footer(
            text=
            f"{member.guild.name} | {datetime.today().strftime('%Y년 %H시 %M분 %S초')}"
        )
        await channel.send(embed=embed)


@bot.tree.command(name="키우기캐릭터만들기", description="키우기 캐릭터 등록 하기!")
async def make_character(interaction: discord.Interaction):
    if not ok_cer(str(interaction.user.id)):
        return await interaction.response.send_message("/가입 으로 가입을 먼저 해주세요!")
    elif not ok_re_cer(interaction.user.id):
        cer = re_cer_load()
        cer[str(interaction.user.id)] = True
        re_cer_save(cer)
        return await interaction.response.send_message("시이의 개인정보 처리방침에 개인정보의 국외 이전 항목이 업데이트 되었어요! [약관](https://shii.me/개인정보처리방침)이나 시이 프로필의 링크로 확인해주세요!")
    user_id = str(interaction.user.id)
    user_data = damagochi().load()
    if user_id in user_data:
        await interaction.response.send_message("이미 캐릭터가 있습니다.")
        return
    view = make_modal()
    await interaction.response.send_modal(view)


global voted_ok
voted_ok = {}
'''
@bot.hybrid_command(name="하트", description="하트를 눌러 응원을 보내기...")
async def heart(ctx):
    user_id = ctx.author.id

    if DiscordpyKoreanbots.get_bot_vote(ctx, user_id=user_id, bot_id=1197084521644961913) == True:
        today = datetime.now().day
        tomonth = datetime.now().month
        toyear = datetime.now().year
        if user_id in voted_ok:
            if voted_ok[user_id]["y"] <= toyear:
                if voted_ok[user_id]["m"] <= tomonth:
                    if voted_ok[user_id]["d"] < today:
                        stocks = load_stocks()
                        if str(ctx.author.id) not in stocks[str(ctx.guild.id)]:
                            await ctx.send("초보자 지원금 500 시이코인과 같이 1000 시이코인을 지급하였습니다. 감사합니다!", ephemeal=True)
                            stocks[str(ctx.guild.id)][str(ctx.message.author.mention)] = 1500
                            save_stocks(stocks)
                            voted_ok[user_id]["y"], voted_ok[user_id]["m"], voted_ok[user_id]["d"] = toyear, tomonth, today
                            return    
                        await ctx.send("보상 시이코인 1000개를 지급하였습니다. 감사합니다!", ephemeal=True)
                        stocks[str(ctx.guild.id)][str(ctx.message.author.mention)] += 1000
                        return
            await ctx.send("이미 하트 보상을 흭득하셨거나, 다른 서버에서 이미 보상을 받으셨습니다.", ephemeral=True)
        else:
            stocks = load_stocks()
            if str(ctx.author.id) not in stocks[str(ctx.guild.id)]:
                await ctx.send("초보자 지원금 500 시이코인과 같이 1000 시이코인을 지금하였습니다. 감사합니다!", ephermal=True)
                stocks[str(ctx.guild.id)][str(ctx.message.author.mention)] = 1500
                save_stocks(stocks)
                voted_ok[user_id]["y"], voted_ok[user_id]["m"], voted_ok[user_id]["d"] = toyear, tomonth, today
                return
            await ctx.send("보상 시이코인 1000개를 지급하였습니다. 감사합니다!", ephemeal=True)
            stocks[str(ctx.guild.id)][str(ctx.message.author.mention)] += 1000
            voted_ok[user_id]["y"], voted_ok[user_id]["m"], voted_ok[user_id]["d"] = toyear, tomonth, today
    else:
        await ctx.send("먼저 하트를 누르고 와주세요! https://koreanbots.dev/bots/1197084521644961913/vote", ephemeral=True)
'''

@bot.hybrid_command(name="스탯", description="캐릭터 스탯보기!")
async def kiwoge(ctx):
    if not ok_cer(ctx.message.author.id):
        return await ctx.send("/가입 으로 가입을 먼저 해주세요!")
    elif not ok_re_cer(ctx.message.author.id):
        messages = await ctx.send("시이의 개인정보 처리방침에 개인정보의 국외 이전 항목이 업데이트 되었어요! [약관](https://shii.me/개인정보처리방침)이나 시이 프로필의 링크로 확인해주세요!")
        cer = re_cer_load()
        cer[str(ctx.message.author.id)] = True
        re_cer_save(cer)
        await asyncio.sleep(5)
        await messages.delete()
    user_id = str(ctx.message.author.id)
    user_data = damagochi().load()
    if not user_id in user_data:
        return await ctx.send("캐릭터 등록을 먼저 해주세요!")

    if user_data[user_id]['lv'] == 1:
        text_lv = '영유아기'
        urls = "llv1"
        imgurl = "lv1"
    elif user_data[user_id]['lv'] == 2:
        text_lv = '유아기'
        urls = "llv2"
        imgurl = "lv2"
    elif user_data[user_id]['lv'] == 3:
        text_lv = '청소년기'
        urls = "llv3"
        imgurl = "lv3"
    elif user_data[user_id]['lv'] == 4:
        text_lv = '성인'
        urls = "llv4"
        imgurl = "lv4"
    else:
        text_lv = 'None'
        urls = "llv4"
        imgurl = "lv4"
    embed = discord.Embed(title=user_data[user_id]["name"],
                          description=text_lv)
    embed.add_field(name="레벨", value=user_data[user_id]["lv"], inline=True)
    embed.add_field(name="경험치", value=user_data[user_id]["exp"], inline=True)
    await ctx.send(embed=embed)


@bot.hybrid_command(name="키우기", description="시이 키우기 게임!")
async def keywa(ctx):
    if not ok_cer(ctx.message.author.id):
        return await ctx.send("/가입 으로 가입을 먼저 해주세요!")
    elif not ok_re_cer(ctx.message.author.id):
        messages = await ctx.send("시이의 개인정보 처리방침에 개인정보의 국외 이전 항목이 업데이트 되었어요! [약관](https://shii.me/개인정보처리방침)이나 시이 프로필의 링크로 확인해주세요!")
        cer = re_cer_load()
        cer[str(ctx.message.author.id)] = True
        re_cer_save(cer)
        await asyncio.sleep(5)
        await messages.delete()
    user_id = str(ctx.message.author.id)
    user_data = damagochi().load()
    if not user_id in user_data:
        return await ctx.send("캐릭터 등록을 먼저 해주세요!")
    if user_data[user_id]['lv'] == 1:
        text_lv = '영유아기'
        urls = "llv1"
        imgurl = "lv1"
    elif user_data[user_id]['lv'] == 2:
        text_lv = '유아기'
        urls = "llv2"
        imgurl = "lv2"
    elif user_data[user_id]['lv'] == 3:
        text_lv = '청소년기'
        urls = "llv3"
        imgurl = "lv3"
    elif user_data[user_id]['lv'] == 4:
        text_lv = '성인'
        urls = "llv4"
        imgurl = "lv4"
    else:
        text_lv = 'None'
        urls = "llv4"
        imgurl = "lv4"

    background = Image.open("background.png")
    foreground = Image.open(f"{imgurl}img.png")

    #배경이 투명한 이미지 파일의 사이즈 가져오기
    (img_h, img_w) = foreground.size
    #print(foreground.size)
    #print("img_h : " , img_h , "img_w : ", img_w)

    #합성할 배경 이미지를 위의 파일 사이즈로 resize
    resize_back = background.resize((img_h, img_w))

    #이미지 합성
    resize_back.paste(foreground, (0, 0), foreground)
    #resize_back.show()
    # 이미지 저장
    resize_back.save(f"keywa{user_id}.png")

    button1 = ui.Button(style=ButtonStyle.green, label="놀기", disabled=True)
    view = ui.View(timeout=None)
    view.add_item(button1)
    button1.disabled = False

    async def button1_callback(interaction: Interaction):
        lests_time = culls.get(interaction.user.id, 0)
        currents_time = time.time()
        coosl_time = 10
        if currents_time - lests_time < coosl_time:
            await interaction.response.send_message(
                f"쿨타임 중입니다. 10초마다 1번씩 사용이 가능합니다.", ephemeral=True)
            print(culls)
            return
        if str(interaction.user.id) == user_id:
            view = discord.ui.View()
            view.add_item(game_Dropdown(user=user_id))
            message = await interaction.response.send_message(view=view,
                                                              ephemeral=True)
        else:
            return
        currents_time = time.time()
        if interaction.user.id in culls:
            del culls[interaction.user.id]
        culls[interaction.user.id] = currents_time
        print(culls)

    button1.callback = button1_callback
    await ctx.send(file=discord.File(f"keywa{user_id}.png",
                                     filename="다마고치.png"),
                   view=view)
    os.remove(f"keywa{user_id}.png")


@bot.hybrid_command(name="입장로그설정", description="입장로그 채널을 설정합니다.")
async def set_hello_log(ctx, channel: discord.TextChannel):
    if not ok_cer(ctx.message.author.id):
        return await ctx.send("/가입 으로 가입을 먼저 해주세요!")
    elif not ok_re_cer(ctx.message.author.id):
        messages = await ctx.send("시이의 개인정보 처리방침에 개인정보의 국외 이전 항목이 업데이트 되었어요! [약관](https://shii.me/개인정보처리방침)이나 시이 프로필의 링크로 확인해주세요!")
        cer = re_cer_load()
        cer[str(ctx.message.author.id)] = True
        re_cer_save(cer)
        await asyncio.sleep(5)
        await messages.delete()
    await ctx.send(f"입장로그 채널을 {channel.mention}로 설정했습니다.")
    channels = channel.id
    hello_log = open_hello_log()
    hello_log[str(ctx.guild.id)] = channels
    save_hello_log(hello_log)
    await channel.send(
        f"{ctx.guild.name} 서버에서 입장로그 채널을 {channel.mention}로 설정했습니다.")


@bot.hybrid_command(name="가입", description="시이 서비스 가입하기")
async def join_shii(ctx):
    if ok_cer(str(ctx.message.author.id)):
        return await ctx.send("이미 가입하였습니다", ephemeral=True)
    cer = open_cer_db()

    only_user = str(ctx.message.author.id)

    button1 = ui.Button(style=ButtonStyle.green,
                        label="시이 가입 하기",
                        disabled=True)
    view = ui.View(timeout=300)
    view.add_item(button1)
    button1.disabled = False

    async def button1_callback(interaction: Interaction):
        if str(interaction.user.id) == only_user:
            await interaction.response.send_message("가입이 완료 되었습니다. 감사합니다.")
            cer[str(interaction.user.id)] = True
            save_cer_db(cer)
            re_cer = re_cer_load()
            re_cer[str(interaction.user.id)] = True
            re_cer_save(re_cer)
        else:
            return

    button1.callback = button1_callback
    embed = discord.Embed(
        title="시이 서비스 가입하기",
        description=
        "가입전 [서비스 이용약관](https://shii.me/서비스이용약관)과 [개인정보처리방침](https://shii.me/개인정보처리방침)을 확인하고 동의해주세요. 버튼이 안눌릴 경우 다시 커멘드를 사용해주세요."
    )
    await ctx.send(embed=embed, view=view)


@bot.hybrid_command(name="입장로그해제", description="입장로그 채널을 해제합니다.")
async def remove_hello_log(ctx):
    if not ok_cer(ctx.message.author.id):
        return await ctx.send("/가입 으로 가입을 먼저 해주세요!")
    elif not ok_re_cer(ctx.message.author.id):
        messages = await ctx.send("시이의 개인정보 처리방침에 개인정보의 국외 이전 항목이 업데이트 되었어요! [약관](https://shii.me/개인정보처리방침)이나 시이 프로필의 링크로 확인해주세요!")
        cer = re_cer_load()
        cer[str(ctx.message.author.id)] = True
        re_cer_save(cer)
        await asyncio.sleep(5)
        await messages.delete()
    hello_log = open_hello_log()
    hello_log[str(ctx.guild.id)] = 'no'
    save_hello_log(hello_log)
    await ctx.send("입장로그 채널을 해제했습니다.")


@bot.tree.command(name="책검색", description="책을 검색 합니다.")
async def search_book(interaction: Interaction, book_name: str):
    if not ok_cer(str(interaction.user.id)):
        return await interaction.response.send_message("/가입 으로 가입을 먼저 해주세요!")
    elif not ok_re_cer(interaction.user.id):
        cer = re_cer_load()
        cer[str(interaction.user.id)] = True
        re_cer_save(cer)
        return await interaction.response.send_message("시이의 개인정보 처리방침에 개인정보의 국외 이전 항목이 업데이트 되었어요! [약관](https://shii.me/개인정보처리방침)이나 시이 프로필의 링크로 확인해주세요!")
    url = f"https://openapi.naver.com/v1/search/book.json?query={book_name}"
    headers = {
        "X-Naver-Client-Id": naver_client_id,
        "X-Naver-Client-Secret": naver_client_secret
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    items_len = len(data['items'])
    view = discord.ui.View()
    if items_len <= 0:
        return await interaction.response.send_message("검색 결과가 없습니다.")

    view.add_item(book_Dropdown(items_len, data))
    await interaction.response.send_message(view=view)


'''커멘드 실행 횟수 저장 및 불러오기'''


def load_commmand_count():
    try:
        with open('command_count.json', 'r') as f:
            command_count = json.load(f)
    except FileNotFoundError:
        command_count = {}
    return command_count


def save_command_count(command_count):
    with open('command_count.json', 'w') as f:
        json.dump(command_count, f, indent=4)


'''시이 학습내용 저장 및 불러오기'''


def load_bot_info():
    file_path = json_file_path

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            bot_info = json.load(file)
    except FileNotFoundError:
        bot_info = {}

    return bot_info


def save_bot_info(bot_info):
    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(bot_info, file, indent=2, ensure_ascii=False)



'''메이플, 메이플m 스탯 리턴'''


def get_str_value(parsed_data, name):
    for stat in parsed_data['final_stat']:
        if stat['stat_name'] == name:
            return stat['stat_value']


def get_strs_value(parded_data, name):
    for stat in parded_data['stat']:
        if stat['stat_name'] == name:
            return stat['stat_value']


'''사용자 시이코인 저장 및 불러오기'''


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


'''주식 시세 저장 및 불러오기'''


def load_stocks():
    try:
        with open(stocks_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


# 주식을 저장하는 함수
def save_stocks(stocks):
    with open(stocks_file, 'w') as f:
        json.dump(stocks, f)


'''사용자 주식 저장 및 불러오기'''


def save_user_stocks(user_stocks):
    with open(user_stocks_file, 'w') as f:
        json.dump(user_stocks, f)


def load_user_stocks():
    try:
        with open(user_stocks_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


'''사용자 도박게임 플레이 횟수 저장 및 불러오기, 확인'''


def dobak_load():
    try:
        with open("dobak.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def dobak_save(data):
    with open("dobak.json", "w") as file:
        json.dump(data, file, indent=4)


def dobak_check(server_id, user_id):
    dobak = dobak_load()
    if not server_id in dobak:
        dobak[server_id] = {}
        dobak_save(dobak)
        return False
    if not user_id in dobak[server_id]:
        dobak[server_id][user_id] = 0
        dobak_save(dobak)
        return False
    if user_id in dobak:
        if dobak[server_id][user_id] >= 15:
            return True
        else:
            return False
    else:
        return False


def er_load():
    try:
        with open("er.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def er_save(data):
    with open("er.json", "w") as file:
        json.dump(data, file, indent=4)


'''@bot.hybrid_command(name="이터널리턴등록", description="이터널리턴 닉네임을 등록합니다.")
async def eiternal_login(ctx, nickname: str):
    if not ok_cer(str(ctx.user.id)):
        return await ctx.send("/가입 으로 가입을 먼저 해주세요!")
    eiternal = er_load()
    if str(ctx.user.id) not in eiternal:
        url = f"https://open-api.bser.io/v1/user/nickname?query={nickname}"
        headers = {
            "x-api-key": bser_api_key
        }
        response = requests.get(url, headers=headers)
        data = response.json()
        print(data)
'''
'''사용자가 보유한 아이템 저장 및 불러오기'''


def load_item():
    try:
        with open("item.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_item(item):
    with open("item.json", "w") as file:
        json.dump(item, file, indent=4)


'''사용자의 아이템 사용여부 저장 및 불러오기'''


def item_set_load():
    try:
        with open("item_set.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def item_set_save(item_set):
    with open("item_set.json", "w") as file:
        json.dump(item_set, file, indent=4)


'''사용자의 광물 채굴 횟수 저장 및 불러오기'''


def load_mining_counts():
    try:
        with open('mining_counts.json', 'r') as f:
            mining_counts = json.load(f)
    except FileNotFoundError:
        mining_counts = {}
    return mining_counts


def save_mining_counts(mining_counts):
    with open('mining_counts.json', 'w') as f:
        json.dump(mining_counts, f)


'''사용자의 광물 보유 정보 저장 및 불러오기, 삭제'''


async def save_minerals(user_id, guild_id, minerals):
    filename = 'minerals.json'
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    if str(guild_id) not in data:
        data[str(guild_id)] = {}
    if str(user_id) not in data[str(guild_id)]:
        data[str(guild_id)][str(user_id)] = []

    data[str(guild_id)][str(user_id)].extend(minerals)

    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


async def get_minerals(user_id, guild_id):
    filename = 'minerals.json'
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        return []

    return data.get(str(guild_id), {}).get(str(user_id), [])


async def clear_minerals(user_id, guild_id):
    filename = 'minerals.json'
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        return

    if str(guild_id) in data and str(user_id) in data[str(guild_id)]:
        del data[str(guild_id)][str(user_id)]

    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


'''욕설 필터링 기능 온오프 상태 저장 및 불러오기'''


def load_fuck_on_off():
    try:
        with open('fuck_on_off.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_fuck_on_off(fuck_on_off):
    with open('fuck_on_off.json', 'w') as file:
        json.dump(fuck_on_off, file, indent=4)


'''고양이 api값 리턴'''


def get_random_cat():
    response = requests.get('https://api.thecatapi.com/v1/images/search')
    data = response.json()
    return data[0]['url']


'''사용자의 메이플 아이디를 저장 및 불러오기'''


def maple_id_load():
    try:
        with open("maple_id.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def maple_id_save(maple_id):
    with open("maple_id.json", "w") as file:
        json.dump(maple_id, file, indent=4)


'''사용자의 메이플m 아이디를 저장 및 불러오기'''


def maple_m_id_load():
    try:
        with open("maple_m_id.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def maple_m_id_save(maple_m_id):
    with open("maple_m_id.json", "w") as file:
        json.dump(maple_m_id, file, indent=4)


'''봇이 들어간 서버수를 리턴'''


def get_guild_nember():
    guild = len(bot.guilds)
    guild_go = 75 - guild
    if guild_go <= 0:
        return "목표 달성!"
    else:
        return f"목표 까지 `{guild_go}` 서버"


'''현재 시간, 날짜를 리턴'''


def get_day_of_week():
    weekday_list = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']

    weekday = weekday_list[datetime.today().weekday()]
    date = datetime.today().strftime("%Y년 %m월 %d일")
    result = '{}({})'.format(date, weekday)
    return result


def get_time():
    return datetime.today().strftime("%H시 %M분 %S초")


'''학교코드 및 학교 급식 api값을 리턴'''


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


'''봇 욕설필터링 온 오프 값을 리턴'''


def load_settings():
    global settings
    try:
        with open(SETTINGS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        # 파일이 없을 경우 기본값 설정
        return {}


# 봇 설정 확인
def is_filter_enabled(server_id):
    settings = load_settings()
    return settings.get(str(server_id), False)


'''네이버 검색 결과를 리턴'''


def naver_search(query):
    url = 'https://openapi.naver.com/v1/search/blog.json'
    headers = {
        'X-Naver-Client-Id': naver_client_id,
        'X-Naver-Client-Secret': naver_client_secret
    }
    params = {'query': query}
    response = requests.get(url, headers=headers, params=params)
    result = response.json()
    if 'items' in result:
        return result['items'][0]['title'], result['items'][0]['link']
    else:
        return 'No results found', ''


'''검색 리턴 값에서 부호 제거'''


def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


'''타임스펨프 생성'''


def get_timestamp():
    return int(time.time())


'''광물 가격을 리턴'''


def calculate_price(mineral):
    mineral_prices = {
        '다이아몬드': 500,  # 다이아몬드의 가격은 100
        '루비': 250,  # 루비의 가격은 80
        '에메랄드': 100,  # 에메랄드의 가격은 70
        '자수정': 50,  # 자수정의 가격은 50
        '철': 25,  # 철의 가격은 20
        '석탄': 10  # 석탄의 가격은 10
    }
    return mineral_prices.get(mineral, 0)


'''광물 이모지를 리턴'''


def emo_re(g):
    if g == '다이아몬드':
        return '<:diamond:1238066362744705054>'
    elif g == '루비':
        return '<:ruby:1238067321365594212>'
    elif g == '에메랄드':
        return '<:emerald:1238067318890692628>'
    elif g == '철':
        return '<:iron:1238067489443807252>'
    elif g == '석탄':
        return '<:coal:1238067741760421909>'
    elif g == '자수정':
        return '<:gems:1238066158683291751>'
    else:
        return '없음'


'''이제 부터는 커멘드 입니다.'''
'''애니 검색 커멘드'''


@bot.hybrid_command(name='애니검색', description="라프텔에서 애니를 검색 합니다.")
async def anime(ctx, keyword: str):
    if not ok_cer(ctx.message.author.id):
        return await ctx.send("/가입 으로 가입을 먼저 해주세요!")
    elif not ok_re_cer(ctx.message.author.id):
        messages = await ctx.send("시이의 개인정보 처리방침에 개인정보의 국외 이전 항목이 업데이트 되었어요! [약관](https://shii.me/개인정보처리방침)이나 시이 프로필의 링크로 확인해주세요!")
        cer = re_cer_load()
        cer[str(ctx.message.author.id)] = True
        re_cer_save(cer)
        await asyncio.sleep(5)
        await messages.delete()
    url = f"https://laftel.net/api/search/v3/keyword/?keyword={keyword}"
    response = requests.get(url)
    data = response.json()
    if data["count"] == 0:
        embed = discord.Embed(title="검색 결과가 없습니다.",
                              description="",
                              color=0x816BFF)
        return await ctx.send(embed=embed)
    obj = data["results"]
    obj = obj[0]
    name = obj["name"]
    id = obj["id"]

    url = f"https://laftel.net/api/items/v2/{id}/"
    response = requests.get(url)
    data = response.json()
    img = data["img"]
    content = data["content"]
    awards = data["awards"]

    air_year_quarter = data["air_year_quarter"]
    genres = data["genres"]
    avg_rating = data["avg_rating"]
    is_viewing = data["is_viewing"]
    is_avod = data["is_avod"]
    txt3 = ""
    txt4 = ""

    if is_avod == False:
        txt = "방영중"
    else:
        txt = "방영종료"

    if is_viewing == True:
        txt2 = "(시청가능)"
    else:
        txt2 = "(시청불가)"

    for i in range(len(genres)):
        txt3 = txt3 + genres[i] + ", "
    txt3 = txt3[:-2]

    embed = discord.Embed(
        title="",
        description=f"[{name}](https://laftel.net/search?&modal={obj['id']})",
        color=0x816BFF)
    embed.set_author(
        name="laftel",
        icon_url=
        "https://cf.channel.io/thumb/200x200/file/7074/5e661af3185a0dd698b6/avatar-d652fe21a162f82ee8d60f025408b498"
    )
    embed.set_thumbnail(url=img)
    embed.add_field(name="", value=content, inline=False)
    embed.add_field(name="별점", value=f"{avg_rating}/5.0")
    embed.add_field(name="방영분기", value=air_year_quarter)
    embed.add_field(name="장르", value=txt3)
    embed.add_field(name="상태", value=f"{txt}{txt2}")

    await ctx.send(embed=embed)


'''@bot.hybrid_command(name="정보", description="유저의 정보를 불러옵니다")
async def user_info(ctx,
                    멤버: discord.Member, required=False):

    if 멤버 == None:    # 만약 멤버를 선택하지 않았다면 멤버를 본인으로 설정
        멤버 = ctx.user

    embed = discord.Embed(
        title=f'**{멤버.display_name}**님의 정보',  # display_name는 사용자의 별명
        description=f'- {멤버}',
        color=0xD3851F
    )
    embed.set_thumbnail(url=멤버.avatar)   
    # set_thumbnail를  .avatar.url을 사용하여 사용자의 프로필 링크로 설정

    embed.add_field(name=f'ID', value=f'{멤버.id}', inline=True)   # 멤버의 id

    bot_status = "🤖 **Bot**" if 멤버.bot else "👤 **User**"
    embed.add_field(name=f'Type', value=f'{bot_status}', inline=True)
    # 멤버가 봇이라면 🤖 **Bot** 유저라면 👤 **User** 봇,유저 구분은 멤버.bot을 이용

    embed.add_field(name=' ', value=' ', inline=False)  # 공백 필드 추가

    embed.add_field(name=f'가입 시기', value=f'{멤버.created_at}', inline=True) 
    embed.add_field(name=f'서버 가입 시기', value=f'{멤버.joined_at}', inline=True)
    # created_at는 디스코드 가입 시기이고 joined_at는 명령어를 입력한 서버에 가입한 날짜

    embed.add_field(name=' ', value=' ', inline=False)  # 공백 필드 추가

    role_mentions = [role.mention for role in 멤버.roles if role != ctx.guild.default_role]
    roles_str = ' '.join(role_mentions) if role_mentions else 'None'
    embed.add_field(name=f'보유 역할', value=f'{roles_str}', inline=True)
    # 멤버의 역할을 roles을 이용해서 추출하고 역할 중에서 != ctx.guild.default_role를 사용하여 에브리원 역할은 제외
    # 만약 보유한 역할이 없다면 None이라고 뜨게 함

    if 멤버.status == discord.Status.online:
        상태 = "🟢 온라인"
    elif 멤버.status == discord.Status.idle:
        상태 = "🌙 자리 비움"
    elif 멤버.status == discord.Status.dnd:
        상태 = "⛔ 방해 금지"
    else:
        상태 = "⚫ 오프라인"
    embed.add_field(name=f'상태', value=f'{상태}', inline=True)
    # 멤버의 status값을 추출하여 값에 따라 상태 변수에 저장

    user_status = 멤버.activity
    if user_status == None:
        pass
    else:
        embed.add_field(name=' ', value=' ', inline=False)  # 공백 필드 추가
        embed.add_field(name="상태메시지", value=user_status, inline=True)
    # 멤버의 activity값을 추출하여 상태메시지가 나오게 하고 상태메시지가 없다면 pass하여서 필드가 나타나지 않게 함
    await ctx.send(embed=embed)'''
'''주식 커멘드'''


@tasks.loop(minutes=5)
async def simulate_stock_market():
    stocks = load_stocks()
    for stock in stocks:
        # 랜덤하게 주식 가격 변동
        previous_value[stock] = stocks[stock]
        ran_up_down = random.randint(0, 1)
        if stocks[stock] <= 0:
            stocks[stock] = 1
        if 0 <= stocks[stock] <= 100:
            max = 300
            min = 0
        elif 101 <= stocks[stock] <= 1000:
            max = 400
            min = 0 - 100
        elif 1001 <= stocks[stock] <= 1500:
            max = 400
            min = 0 - 200
        elif 1501 <= stocks[stock] <= 1750:
            max = 450
            min = 0 - 300
        elif 1751 <= stocks[stock] <= 2000:
            max = 400
            min = 0 - 400
        else:
            max = 400
            min = 0 - 600

        stocks[stock] += random.randint(min, max)
        if stocks[stock] <= 0:
            stocks[stock] = 1
        # 주식 정보 저장
        print(f"가격변동이 성공적으로 완료되었습니다.")
    save_stocks(stocks)


# 주식 가격 조회 명령어
@bot.hybrid_command(name='가격보기', description="주식가격확인")
async def check_stock_price(ctx):
    if not ok_cer(ctx.message.author.id):
        return await ctx.send("/가입 으로 가입을 먼저 해주세요!")
    elif not ok_re_cer(ctx.message.author.id):
        messages = await ctx.send("시이의 개인정보 처리방침에 개인정보의 국외 이전 항목이 업데이트 되었어요! [약관](https://shii.me/개인정보처리방침)이나 시이 프로필의 링크로 확인해주세요!")
        cer = re_cer_load()
        cer[str(ctx.message.author.id)] = True
        re_cer_save(cer)
        await asyncio.sleep(5)
        await messages.delete()
    stocks = load_stocks()
    embed = discord.Embed(title="주식 가격", color=0xFFB2F5)
    for stock, price in stocks.items():
        if price > previous_value[stock]:
            embed.add_field(
                name=f"{stock.upper()}",
                value=
                f"{price} <:shiicoin:1211874282414673970> \n`(▲{price - previous_value[stock]})`"
            )
        elif price < previous_value[stock]:
            embed.add_field(
                name=f"{stock.upper()}",
                value=
                f"{price} <:shiicoin:1211874282414673970> \n`(▼{previous_value[stock] - price})`"
            )
        else:
            embed.add_field(
                name=f"{stock.upper()}",
                value=
                f"{price} <:shiicoin:1211874282414673970> \n`(변동 없음 {previous_value[stock] - price})`"
            )
    await ctx.send(embed=embed)


# 주식 구매 명령어
@bot.hybrid_command(name='주식매수', description="주식매수")
async def buy_stock(ctx, 주식명: str, 구매할개수: int):
    if not ok_cer(ctx.message.author.id):
        return await ctx.send("/가입 으로 가입을 먼저 해주세요!")
    elif not ok_re_cer(ctx.message.author.id):
        messages = await ctx.send("시이의 개인정보 처리방침에 개인정보의 국외 이전 항목이 업데이트 되었어요! [약관](https://shii.me/개인정보처리방침)이나 시이 프로필의 링크로 확인해주세요!")
        cer = re_cer_load()
        cer[str(ctx.message.author.id)] = True
        re_cer_save(cer)
        await asyncio.sleep(5)
        await messages.delete()
    server_id = str(ctx.guild.id)
    user_id = str(ctx.message.author.mention)
    stocks = load_stocks()
    if 주식명.upper() in stocks:
        cost = stocks[주식명.upper()] * 구매할개수
        capital = load_capital()
        user_stocks = load_user_stocks()
        if server_id not in capital:
            capital[server_id] = {}
        if user_id not in capital[server_id]:
            capital[server_id][user_id] = 500
        if cost <= 0:
            await ctx.send('0개 이하의 주식을 구매할 수 없습니다.')
        elif cost <= capital[server_id][user_id]:
            if server_id not in user_stocks:
                user_stocks[server_id] = {}
            if user_id not in user_stocks[server_id]:
                user_stocks[server_id][user_id] = {}
            if 주식명.upper() not in user_stocks[server_id][user_id]:
                user_stocks[server_id][user_id][주식명.upper()] = 0
            user_stocks[server_id][user_id][주식명.upper()] += 구매할개수
            capital[server_id][user_id] -= cost
            await ctx.send(f'{주식명.upper()}를 ${cost}에 {구매할개수}주 구매했습니다.')
        else:
            await ctx.send(
                '<:shiicoin:1211874282414673970> 시이코인이 부족하여 주식을 구매할 수 없습니다.')
        save_capital(capital)
        save_user_stocks(user_stocks)
    else:
        await ctx.send(f'{주식명.upper()}은(는) 유효한 주식 기호가 아닙니다.')


# 주식 판매 명령어
@bot.hybrid_command(name='주식매도', description="주식팔기")
async def sell_stock(ctx, 주식명: str, 판매할개수: int):
    if not ok_cer(ctx.message.author.id):
        return await ctx.send("/가입 으로 가입을 먼저 해주세요!")
    elif not ok_re_cer(ctx.message.author.id):
        messages = await ctx.send("시이의 개인정보 처리방침에 개인정보의 국외 이전 항목이 업데이트 되었어요! [약관](https://shii.me/개인정보처리방침)이나 시이 프로필의 링크로 확인해주세요!")
        cer = re_cer_load()
        cer[str(ctx.message.author.id)] = True
        re_cer_save(cer)
        await asyncio.sleep(5)
        await messages.delete()
    server_id = str(ctx.guild.id)
    user_id = str(ctx.message.author.mention)
    stocks = load_stocks()
    if 주식명.upper() in stocks:
        capital = load_capital()
        user_stocks = load_user_stocks()
        if server_id not in capital or user_id not in capital[server_id]:
            await ctx.send('판매할 주식이 없습니다.')
        elif 주식명.upper() not in user_stocks.get(server_id,
                                                {}).get(user_id, {}):
            await ctx.send(f'{주식명.upper()}의 주식을 소유하고 있지 않습니다.')
        elif user_stocks[server_id][user_id][
                주식명.upper()] >= 판매할개수 or 판매할개수 <= 0:
            user_stocks[server_id][user_id][주식명.upper()] -= 판매할개수
            earnings = stocks[주식명.upper()] * 판매할개수
            capital[server_id][user_id] += earnings
            await ctx.send(f'{주식명.upper()}를 ${earnings}에 {판매할개수}주 판매했습니다.')
            save_capital(capital)
            save_user_stocks(user_stocks)
        else:
            await ctx.send('판매할 주식이 충분하지 않습니다.')
    else:
        await ctx.send(f'{주식명.upper()}은(는) 유효한 주식 기호가 아닙니다.')


@bot.hybrid_command(name='내주식', description="보유한 주식 조회")
async def view_stocks(ctx):
    if not ok_cer(ctx.message.author.id):
        return await ctx.send("/가입 으로 가입을 먼저 해주세요!")
    elif not ok_re_cer(ctx.message.author.id):
        messages = await ctx.send("시이의 개인정보 처리방침에 개인정보의 국외 이전 항목이 업데이트 되었어요! [약관](https://shii.me/개인정보처리방침)이나 시이 프로필의 링크로 확인해주세요!")
        cer = re_cer_load()
        cer[str(ctx.message.author.id)] = True
        re_cer_save(cer)
        await asyncio.sleep(5)
        await messages.delete()
    server_id = str(ctx.guild.id)
    user_id = str(ctx.message.author.mention)
    user_stocks = load_user_stocks()
    if server_id in user_stocks and user_id in user_stocks[server_id]:
        save_user_stocks(user_stocks)
        user_stock_info = user_stocks[server_id][user_id]
        if user_stock_info:
            embed = discord.Embed(
                title=f"{ctx.message.author.display_name}님의 보유 주식",
                color=0x00ff00)
            for stock, quantity in user_stock_info.items():
                embed.add_field(name=f"{stock.upper()}",
                                value=f"수량: {quantity}",
                                inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send("보유한 주식이 없습니다.")
    else:
        await ctx.send("보유한 주식이 없습니다.")


'''시이코인 커멘드'''


@bot.hybrid_command(name='내시이코인', description="내 시이코인 보기")
async def check_balance(ctx):
    if not ok_cer(ctx.message.author.id):
        return await ctx.send("/가입 으로 가입을 먼저 해주세요!")
    elif not ok_re_cer(ctx.message.author.id):
        messages = await ctx.send("시이의 개인정보 처리방침에 개인정보의 국외 이전 항목이 업데이트 되었어요! [약관](https://shii.me/개인정보처리방침)이나 시이 프로필의 링크로 확인해주세요!")
        cer = re_cer_load()
        cer[str(ctx.message.author.id)] = True
        re_cer_save(cer)
        await asyncio.sleep(5)
        await messages.delete()
    server_id = str(ctx.guild.id)
    user_id = str(ctx.message.author.mention)
    capital = load_capital()
    if server_id in capital and user_id in capital[server_id]:
        await ctx.send(
            f'{ctx.message.author.mention}님이 보유하신 시이코인은 총 {capital[server_id][user_id]} <:shiicoin:1211874282414673970> 시이코인 입니다.'
        )
    else:
        if server_id not in capital:
            capital[server_id] = {}
        capital[server_id][user_id] = 10000  # 초기 자본 설정
        save_capital(capital)
        await ctx.send(
            f'{ctx.message.author.mention}님, 초기 자본 10000 <:shiicoin:1211874282414673970> 시이코인을 지급하였습니다.'
        )


@bot.hybrid_command(name="송금", description="서버에 있는 유저에게 시이코인을 보네요!")
async def send_money(ctx, user: discord.Member, amount: int):
    if not ok_cer(ctx.message.author.id):
        return await ctx.send("/가입 으로 가입을 먼저 해주세요!")
    elif not ok_re_cer(ctx.message.author.id):
        messages = await ctx.send("시이의 개인정보 처리방침에 개인정보의 국외 이전 항목이 업데이트 되었어요! [약관](https://shii.me/개인정보처리방침)이나 시이 프로필의 링크로 확인해주세요!")
        cer = re_cer_load()
        cer[str(ctx.message.author.id)] = True
        re_cer_save(cer)
        await asyncio.sleep(5)
        await messages.delete()
    user_id = str(ctx.message.author.mention)
    toos_id = str(user.mention)
    guild_id = str(ctx.guild.id)
    capital = load_capital()

    if guild_id not in capital:
        capital[guild_id] = {}
    if user_id not in capital[guild_id]:
        capital[guild_id][user_id] = 500
    if toos_id not in capital[guild_id]:
        capital[guild_id][toos_id] = 500

    if amount < 1000:
        await ctx.send(
            '시이코인은 1000 <:shiicoin:1211874282414673970> 부터 송금이 가능 합니다.')
        return

    if 1000 <= amount < 10000:
        toos_amount = 100
    else:
        toos_amount = round(amount * 0.01)

    if capital[guild_id][user_id] <= amount:
        await ctx.send("시이코인이 부족합니다.")
        return

    capital[guild_id][user_id] -= math.trunc(amount)
    capital[guild_id][toos_id] += math.trunc(amount - toos_amount)
    save_capital(capital)

    await ctx.send(
        f"{ctx.message.author.display_name}님이 {user.display_name}에게 {amount} <:shiicoin:1211874282414673970> 시이코인을 송금하였습니다!\n`수수료: {toos_amount}`"
    )


'''도박 및 상점 커멘드'''


@bot.hybrid_command(name='홀짝', description="2배이거나, 전부 잃거나")
async def coin_flip(ctx, bet: int, choice: str):
    if not ok_cer(ctx.message.author.id):
        return await ctx.send("/가입 으로 가입을 먼저 해주세요!")
    elif not ok_re_cer(ctx.message.author.id):
        messages = await ctx.send("시이의 개인정보 처리방침에 개인정보의 국외 이전 항목이 업데이트 되었어요! [약관](https://shii.me/개인정보처리방침)이나 시이 프로필의 링크로 확인해주세요!")
        cer = re_cer_load()
        cer[str(ctx.message.author.id)] = True
        re_cer_save(cer)
        await asyncio.sleep(5)
        await messages.delete()
    dobak = dobak_load()
    server_id = str(ctx.guild.id)
    user_id = str(ctx.message.author.mention)
    if not server_id in dobak:
        dobak[server_id] = {}
    if not user_id in dobak[server_id]:
        dobak[server_id][user_id] = 0
    if dobak_check(str(ctx.guild.id), str(ctx.message.author.mention)):
        await ctx.send("도박중독 상담은 국번 없이 1336")
        return
    if not (choice == '홀' or choice == '짝'):
        await ctx.send("홀 또는 짝을 선택하세요.")
        return
    if bet <= 0:
        await ctx.send("0 이하의 금액을 걸 수 없습니다.")
        return
    server_id = str(ctx.guild.id)
    user_id = str(ctx.message.author.mention)
    capital = load_capital()
    dobak = dobak_load()
    if server_id not in capital:
        capital[server_id] = {}
    if user_id not in capital[server_id]:
        capital[server_id][user_id] = 500
    if capital[server_id][user_id] < bet:
        await ctx.send(
            "<:shiicoin:1211874282414673970> 시이코인이 부족하여 게임을 진행할 수 없습니다.")
        return

    dobak[server_id][user_id] += 1
    capital[server_id][user_id] -= bet
    result = random.randint(1, 100)
    if result % 2 == 0:
        outcome = '짝'
    else:
        outcome = '홀'
    if outcome == choice:
        capital[server_id][user_id] += bet * 2
        await ctx.send(
            f"결과: {result} - {outcome}! 축하합니다! {bet * 2} <:shiicoin:1211874282414673970> 시이코인을 얻었습니다."
        )
        save_capital(capital)
        dobak_save(dobak)
    else:
        await ctx.send(
            f"결과: {result} - {outcome}! {bet} <:shiicoin:1211874282414673970> 시이코인을 잃었습니다."
        )
        dobak_save(dobak)


@bot.hybrid_command(name='주사위도박', description="주사위 수 맟추기")
async def rolldobak(ctx, bet: int, number: int):
    if not ok_cer(ctx.message.author.id):
        return await ctx.send("/가입 으로 가입을 먼저 해주세요!")
    elif not ok_re_cer(ctx.message.author.id):
        messages = await ctx.send("시이의 개인정보 처리방침에 개인정보의 국외 이전 항목이 업데이트 되었어요! [약관](https://shii.me/개인정보처리방침)이나 시이 프로필의 링크로 확인해주세요!")
        cer = re_cer_load()
        cer[str(ctx.message.author.id)] = True
        re_cer_save(cer)
        await asyncio.sleep(5)
        await messages.delete()
    dobak = dobak_load()
    server_id = str(ctx.guild.id)
    user_id = str(ctx.message.author.mention)
    if not server_id in dobak:
        dobak[server_id] = {}
    if not user_id in dobak[server_id]:
        dobak[server_id][user_id] = 0
    if dobak_check(str(ctx.guild.id), str(ctx.message.author.mention)):
        await ctx.send("도박중독 상담은 국번 없이 1336")
        return
    if bet <= 0:
        await ctx.send("0 이하의 금액을 걸 수 없습니다.")
        return
    server_id = str(ctx.guild.id)
    user_id = str(ctx.message.author.mention)
    capital = load_capital()
    dobak = dobak_load()
    if server_id not in capital:
        capital[server_id] = {}
    if user_id not in capital[server_id]:
        capital[server_id][user_id] = 500
    if capital[server_id][user_id] < bet:
        await ctx.send(
            "<:shiicoin:1211874282414673970> 시이코인이 부족하여 게임을 진행할 수 없습니다.")
        return

    dobak[server_id][user_id] += 1
    capital[server_id][user_id] -= bet
    result = random.randint(1, 6)
    if result == number:
        capital[server_id][user_id] += bet * 6
        await ctx.send(
            f"결과: {result}! 축하합니다! {bet * 6} <:shiicoin:1211874282414673970> 시이코인을 얻었습니다."
        )
        save_capital(capital)
        dobak_save(dobak)
    else:
        await ctx.send(
            f"결과: {result}! {bet} <:shiicoin:1211874282414673970> 시이코인을 잃었습니다."
        )
        dobak_save(dobak)


@bot.hybrid_command(name="아이템사용", description="아이템을 사용하고 해제 합니다.")
async def use_item(ctx, item_name: str):
    if not ok_cer(ctx.message.author.id):
        return await ctx.send("/가입 으로 가입을 먼저 해주세요!")
    elif not ok_re_cer(ctx.message.author.id):
        messages = await ctx.send("시이의 개인정보 처리방침에 개인정보의 국외 이전 항목이 업데이트 되었어요! [약관](https://shii.me/개인정보처리방침)이나 시이 프로필의 링크로 확인해주세요!")
        cer = re_cer_load()
        cer[str(ctx.message.author.id)] = True
        re_cer_save(cer)
        await asyncio.sleep(5)
        await messages.delete()
    item = load_item()
    item_set = item_set_load()
    user = str(ctx.message.author.mention)
    guild = str(ctx.guild.id)
    if guild in item and user in item[guild]:
        if item_name in item[guild][user]:
            if item_name == "냥체 권":
                if guild not in item_set:
                    item_set[guild] = {}
                if user not in item_set[guild]:
                    item_set[guild][user] = {}
                if "냥체" not in item_set[guild][user]:
                    item_set[guild][user]["냥체"] = False
                if item_set[guild][user]["냥체"]:
                    item_set[guild][user]["냥체"] = False
                    await ctx.send("냥체 권을 해제하였습니다.")
                else:
                    item_set[guild][user]["냥체"] = True
                    await ctx.send("냥체 권을 사용하였습니다.")

                if "주인님체" not in item_set[guild][user]:
                    item_set[guild][user]["주인님체"] = False
                if item_set[guild][user]["주인님체"]:
                    item_set[guild][user]["주인님체"] = False
                    await ctx.send("주인님체 권을 해제하고 냥체 권을 사용하였습니다.")
                item_set_save(item_set)

            elif item_name == "주인님체 권":
                if guild not in item_set:
                    item_set[guild] = {}
                if user not in item_set[guild]:
                    item_set[guild][user] = {}
                if "주인님체" not in item_set[guild][user]:
                    item_set[guild][user]["주인님체"] = False
                if item_set[guild][user]["주인님체"]:
                    item_set[guild][user]["주인님체"] = False
                    await ctx.send("주인님체 권을 해제하였습니다.")
                else:
                    item_set[guild][user]["주인님체"] = True
                    await ctx.send("주인님체 권을 사용하였습니다.")
                if "냥체" not in item_set[guild][user]:
                    item_set[guild][user]["냥체"] = False
                if item_set[guild][user]["냥체"]:
                    item_set[guild][user]["냥체"] = False
                    await ctx.send("냥체 권을 해제하고 주인님체 권을 사용하였습니다.")
                item_set_save(item_set)
            else:
                await ctx.send('해당 아이템을 사용할 수 었습니다.')
        else:
            await ctx.send("보유한 아이템이 없습니다.")
    else:
        await ctx.send("보유한 아이템이 없습니다.")


@bot.tree.command(name="상점", description="시이코인으로 아이템을 살 수 있어요!")
async def sell_shii(interaction: discord.Interaction):
    if not ok_cer(str(interaction.user.id)):
        return await interaction.response.send_message("/가입 으로 가입을 먼저 해주세요!")
    elif not ok_re_cer(interaction.user.id):
        cer = re_cer_load()
        cer[str(interaction.user.id)] = True
        re_cer_save(cer)
        return await interaction.response.send_message("시이의 개인정보 처리방침에 개인정보의 국외 이전 항목이 업데이트 되었어요! [약관](https://shii.me/개인정보처리방침)이나 시이 프로필의 링크로 확인해주세요!")
    view = discord.ui.View()
    view.add_item(
        Dropdown(str(interaction.user.id), str(interaction.user.mention),
                 str(interaction.guild_id)))
    await interaction.response.send_message("아이템을 선택하세요!", view=view)  # noqa


'''고양이 사진 커멘드'''


@bot.hybrid_command(name="고양이", description="랜덤으로 고양이 사진을 불러옵니다")
async def cat(ctx):
    if not ok_cer(ctx.message.author.id):
        return await ctx.send("/가입 으로 가입을 먼저 해주세요!")
    elif not ok_re_cer(ctx.message.author.id):
        messages = await ctx.send("시이의 개인정보 처리방침에 개인정보의 국외 이전 항목이 업데이트 되었어요! [약관](https://shii.me/개인정보처리방침)이나 시이 프로필의 링크로 확인해주세요!")
        cer = re_cer_load()
        cer[str(ctx.message.author.id)] = True
        re_cer_save(cer)
        await asyncio.sleep(5)
        await messages.delete()
    cat_image_url = get_random_cat()
    await ctx.send(cat_image_url)


'''급식 커멘드'''


@bot.hybrid_command(name='급식', description="학교급식 7일 보기")
async def school_lunch(ctx, school_name: str):
    if not ok_cer(ctx.message.author.id):
        return await ctx.send("/가입 으로 가입을 먼저 해주세요!")
    elif not ok_re_cer(ctx.message.author.id):
        messages = await ctx.send("시이의 개인정보 처리방침에 개인정보의 국외 이전 항목이 업데이트 되었어요! [약관](https://shii.me/개인정보처리방침)이나 시이 프로필의 링크로 확인해주세요!")
        cer = re_cer_load()
        cer[str(ctx.message.author.id)] = True
        re_cer_save(cer)
        await asyncio.sleep(5)
        await messages.delete()
    school_code = get_school_code(school_name)

    if school_code:
        # 임베드 생성
        embed = discord.Embed(title=f"{school_name} 급식", color=0x00ff00)

        # 현재 날짜부터 30일 동안의 급식 정보 추가
        today = datetime.today()
        for i in range(7):
            date = (today + timedelta(days=i)).strftime('%m%d')
            lunch_menu = get_school_lunch(school_code, date)
            if lunch_menu:
                embed.add_field(name=f"{date}", value=lunch_menu)
            else:
                embed.add_field(name=f"{date}",
                                value="해당 날짜의 급식 정보를 찾을 수 없습니다.")
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"{school_name} 를 찾을 수 없습니다.")


'''검색 커멘드'''


@bot.hybrid_command(name='카카오검색', description="카카오를 통한 검색(베타)")
async def search_kakao(ctx, *, text: str):
    if not ok_cer(ctx.message.author.id):
        return await ctx.send("/가입 으로 가입을 먼저 해주세요!")
    elif not ok_re_cer(ctx.message.author.id):
        messages = await ctx.send("시이의 개인정보 처리방침에 개인정보의 국외 이전 항목이 업데이트 되었어요! [약관](https://shii.me/개인정보처리방침)이나 시이 프로필의 링크로 확인해주세요!")
        cer = re_cer_load()
        cer[str(ctx.message.author.id)] = True
        re_cer_save(cer)
        await asyncio.sleep(5)
        await messages.delete()
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
        embed.add_field(name=plain_text,
                        value=f'URL: {result["url"]}',
                        inline=False)
        await ctx.send(embed=embed)

    except requests.exceptions.HTTPError as e:
        await ctx.send(f'HTTP 오류: {e.response.status_code} - {e.response.text}'
                       )

    except (IndexError, KeyError):
        await ctx.send(f'검색 결과를 찾을 수 없습니다. 더 정확한 검색어를 입력하세요.')

    except requests.exceptions.RequestException as e:
        await ctx.send(f'오류 발생: {e}')


@bot.hybrid_command(name='블로그검색', description="네이버 open api를 통한 검색(베타)")
async def search(ctx, *, query):
    if not ok_cer(ctx.message.author.id):
        return await ctx.send("/가입 으로 가입을 먼저 해주세요!")
    elif not ok_re_cer(ctx.message.author.id):
        messages = await ctx.send("시이의 개인정보 처리방침에 개인정보의 국외 이전 항목이 업데이트 되었어요! [약관](https://shii.me/개인정보처리방침)이나 시이 프로필의 링크로 확인해주세요!")
        cer = re_cer_load()
        cer[str(ctx.message.author.id)] = True
        re_cer_save(cer)
        await asyncio.sleep(5)
        await messages.delete()
    title, link = naver_search(query)
    html_text = title
    plain_text = remove_html_tags(html_text)
    embed = discord.Embed(title=f"검색어: {query}",
                          description=plain_text,
                          color=0x86E57F)
    embed.set_footer(text=link)
    await ctx.send(embed=embed)


@bot.hybrid_command(name='유튜브검색', description="유튜브 검색(베타)")
async def youtube_search(ctx, *, query: str):
    if not ok_cer(ctx.message.author.id):
        return await ctx.send("/가입 으로 가입을 먼저 해주세요!")
    elif not ok_re_cer(ctx.message.author.id):
        messages = await ctx.send("시이의 개인정보 처리방침에 개인정보의 국외 이전 항목이 업데이트 되었어요! [약관](https://shii.me/개인정보처리방침)이나 시이 프로필의 링크로 확인해주세요!")
        cer = re_cer_load()
        cer[str(ctx.message.author.id)] = True
        re_cer_save(cer)
        await asyncio.sleep(5)
        await messages.delete()
    results = YoutubeSearch(query, max_results=1).to_dict()

    if results:
        video_title = results[0]['title']
        video_url = f"https://www.youtube.com/watch?v={results[0]['id']}"
        await ctx.send(f'검색 결과: {video_title}\n링크: {video_url}')
    else:
        await ctx.send('검색 결과를 찾을 수 없습니다.')


'''메세지 청소 커멘드'''


@bot.hybrid_command(name='클리어', description="메시지 청소")
async def clear(ctx, amount: int):
    if not ok_cer(ctx.message.author.id):
        return await ctx.send("/가입 으로 가입을 먼저 해주세요!")
    elif not ok_re_cer(ctx.message.author.id):
        messages = await ctx.send("시이의 개인정보 처리방침에 개인정보의 국외 이전 항목이 업데이트 되었어요! [약관](https://shii.me/개인정보처리방침)이나 시이 프로필의 링크로 확인해주세요!")
        cer = re_cer_load()
        cer[str(ctx.message.author.id)] = True
        re_cer_save(cer)
        await asyncio.sleep(5)
        await messages.delete()
    if ctx.message.author.guild_permissions.manage_messages:
        sent_message1 = await ctx.send("잠시 기다려 주세요")
        if not ctx.guild:
            sent_message2 = await ctx.send("DM에서는 사용이 불가능한 명령어입니다!")
            await asyncio.sleep(3)
            await sent_message1.delete()
            await sent_message2.delete()
            return
        channel = ctx.channel
        await channel.purge(limit=amount + 1)
        sent_message = await ctx.send(f"{amount}개의 메시지를 삭제했어요!")
        print(f"{amount}개의 메시지를 삭제했어요!")
        await asyncio.sleep(3)
        await sent_message.delete()
    else:
        await ctx.send("권한이 없습니다.")
        return


'''욕설 필터링 기능 온오프 커멘드'''


@bot.hybrid_command(name="욕설필터링", description="욕설 필터링 기능을 온 오프 합니다.")
async def fuck_on_off_set(ctx):
    if not ok_cer(ctx.message.author.id):
        return await ctx.send("/가입 으로 가입을 먼저 해주세요!")
    elif not ok_re_cer(ctx.message.author.id):
        messages = await ctx.send("시이의 개인정보 처리방침에 개인정보의 국외 이전 항목이 업데이트 되었어요! [약관](https://shii.me/개인정보처리방침)이나 시이 프로필의 링크로 확인해주세요!")
        cer = re_cer_load()
        cer[str(ctx.message.author.id)] = True
        re_cer_save(cer)
        await asyncio.sleep(5)
        await messages.delete()
    fuck_on_off = load_fuck_on_off()
    guild_id = str(ctx.guild.id)
    if not guild_id in fuck_on_off:
        fuck_on_off[guild_id] = False

    if fuck_on_off[guild_id]:
        fuck_on_off[guild_id] = False
        await ctx.send(f'욕설 필터링 설정이 {fuck_on_off[guild_id]}로 변경 되었습니다.')
    else:
        fuck_on_off[guild_id] = True
        await ctx.send(f'욕설 필터링 설정이 {fuck_on_off[guild_id]}로 변경 되었습니다.')
    save_fuck_on_off(fuck_on_off)


'''찬반투표 커멘드'''


@bot.hybrid_command(name='찬반투표', description="투표를 시작합니다.")
async def start_poll(ctx, title: str, description: str):
    if not ok_cer(ctx.message.author.id):
        return await ctx.send("/가입 으로 가입을 먼저 해주세요!")
    elif not ok_re_cer(ctx.message.author.id):
        messages = await ctx.send("시이의 개인정보 처리방침에 개인정보의 국외 이전 항목이 업데이트 되었어요! [약관](https://shii.me/개인정보처리방침)이나 시이 프로필의 링크로 확인해주세요!")
        cer = re_cer_load()
        cer[str(ctx.message.author.id)] = True
        re_cer_save(cer)
        await asyncio.sleep(5)
        await messages.delete()
    embed = discord.Embed(title=title, description=description, color=0xFFB2F5)
    embed.set_footer(text=f"투표를 종료하려면 ❌ 이모지를 클릭하세요.")
    message = await ctx.send(embed=embed)
    await message.add_reaction("👍")
    await message.add_reaction("👎")
    await message.add_reaction("❌")
    active_polls[message.id] = {
        "question": title,
        "author_id": ctx.author.id,
        "votes": {
            "👍": [],
            "👎": []
        }
    }


@bot.event
async def on_reaction_add(reaction, user):
    if user == bot.user:
        return
    message_id = reaction.message.id
    if message_id in active_polls:
        if reaction.emoji == "❌" and (
                user.guild_permissions.administrator
                or user.id == active_polls[message_id]["author_id"]):
            await show_poll_result(reaction.message)
            await reaction.message.delete()
            del active_polls[message_id]
        elif reaction.emoji in ["👍", "👎"]:
            poll = active_polls[message_id]
            if user.id not in poll["votes"][reaction.emoji]:
                for vote in poll["votes"].values():
                    if user.id in vote:
                        vote.remove(user.id)
                poll["votes"][reaction.emoji].append(user.id)
                await update_poll_embed(reaction.message)


@bot.event
async def on_reaction_remove(reaction, user):
    if user == bot.user:
        return
    message_id = reaction.message.id
    if message_id in active_polls:
        if reaction.emoji in ["👍", "👎"]:
            poll = active_polls[message_id]
            if user.id in poll["votes"][reaction.emoji]:
                poll["votes"][reaction.emoji].remove(user.id)
                await update_poll_embed(reaction.message)


async def update_poll_embed(message):
    poll_id = message.id
    question = active_polls[poll_id]["question"]
    embed = message.embeds[0]
    embed.clear_fields()
    for e, voters in active_polls[poll_id]["votes"].items():
        mentions = [f"<@{voter}>" for voter in voters]
        voters_text = ", ".join(mentions)
        embed.add_field(name=e,
                        value=voters_text if voters else "",
                        inline=True)
    await message.edit(embed=embed)


async def show_poll_result(message):
    reactions = message.reactions
    poll_id = message.id
    question = active_polls[poll_id]["question"]
    result = {}
    for reaction in reactions:
        if reaction.emoji != "❌":
            result[reaction.emoji] = reaction.count - 1
    result_message = discord.Embed(title=f"{question}\n투표 결과:", color=0xFFB2F5)
    for emoji, count in result.items():
        result_message.add_field(name=f"{emoji}", value=f"{count} 표")
    await message.channel.send(embed=result_message)


'''보이스 커멘드'''


@bot.hybrid_command(name='음성채널입장', description="음성 채널 입장(베타)")
async def start1(ctx):
    if not ok_cer(ctx.message.author.id):
        return await ctx.send("/가입 으로 가입을 먼저 해주세요!")
    elif not ok_re_cer(ctx.message.author.id):
        messages = await ctx.send("시이의 개인정보 처리방침에 개인정보의 국외 이전 항목이 업데이트 되었어요! [약관](https://shii.me/개인정보처리방침)이나 시이 프로필의 링크로 확인해주세요!")
        cer = re_cer_load()
        cer[str(ctx.message.author.id)] = True
        re_cer_save(cer)
        await asyncio.sleep(5)
        await messages.delete()

    if ctx.message.author.voice and ctx.message.author.voice.channel:
        channel = ctx.message.author.voice.channel
        await ctx.send(f"봇이 {channel} 채널에 입장합니다.")
        await channel.connect()
        print(f"음성 채널 정보: {ctx.message.author.voice}")
        print(f"음성 채널 이름: {ctx.message.author.voice.channel}")
    else:
        await ctx.send("음성 채널에 유저가 존재하지 않습니다. 1명 이상 입장해 주세요.")


@bot.hybrid_command(name='음성채널퇴장', description="음성 채널 퇴장(베타)")
async def stop1(ctx):
    try:
        # 음성 채널에서 봇을 내보냅니다.
        await ctx.message.voice_client.disconnect()
        await ctx.send(f"봇을 {ctx.message.author.voice.channel} 에서 내보냈습니다.")
    except IndexError as error_message:
        print(f"에러 발생: {error_message}")
        await ctx.send(
            f"{ctx.message.author.voice.channel}에 유저가 존재하지 않거나 봇이 존재하지 "
            f"않습니다.\\n다시 입장후 퇴장시켜주세요.")
    except AttributeError as not_found_channel:
        print(f"에러 발생: {not_found_channel}")
        await ctx.send("봇이 존재하는 채널을 찾는 데 실패했습니다.")


'''게임 커멘드'''


@bot.hybrid_command(name='주사위', description="주사위 굴리기")
async def roll(ctx):
    if not ok_cer(ctx.message.author.id):
        return await ctx.send("/가입 으로 가입을 먼저 해주세요!")
    elif not ok_re_cer(ctx.message.author.id):
        messages = await ctx.send("시이의 개인정보 처리방침에 개인정보의 국외 이전 항목이 업데이트 되었어요! [약관](https://shii.me/개인정보처리방침)이나 시이 프로필의 링크로 확인해주세요!")
        cer = re_cer_load()
        cer[str(ctx.message.author.id)] = True
        re_cer_save(cer)
        await asyncio.sleep(5)
        await messages.delete()
    randnum = random.randint(1, 6)  # 1이상 6이하 랜덤 숫자를 뽑음
    await ctx.send(f'주사위 결과는 {randnum} 입니다.')
    print(f'주사위 결과는 {randnum} 입니다.')


'''도움말 및 공지사항 커멘드'''


@bot.hybrid_command(name='공지사항', description="시이봇의 공지를 볼 수 있어요!")
async def announcement(ctx):
    if not ok_cer(ctx.message.author.id):
        return await ctx.send("/가입 으로 가입을 먼저 해주세요!")
    elif not ok_re_cer(ctx.message.author.id):
        messages = await ctx.send("시이의 개인정보 처리방침에 개인정보의 국외 이전 항목이 업데이트 되었어요! [약관](https://shii.me/개인정보처리방침)이나 시이 프로필의 링크로 확인해주세요!")
        cer = re_cer_load()
        cer[str(ctx.message.author.id)] = True
        re_cer_save(cer)
        await asyncio.sleep(5)
        await messages.delete()
    embed = discord.Embed(title="시이 공지 사항",
                          description="2024.11.22 공지",
                          color=0xFFB2F5)
    embed.add_field(name="시이 1주년",
                    value="2025.1.17 시이 1주년 기대하시라",
                    inline=False)
    await ctx.send(embed=embed)


@bot.hybrid_command(name='help', description="시이봇 메뉴얼")
async def helps(ctx):
    embed = discord.Embed(title="안녕하세요, 시이입니다!",
                          description="귀여운 챗봇 하나쯤, 시이\n'시이야'라고 불러주세요!",
                          color=0xFFB2F5)
    embed.set_thumbnail(url='https://shii.me/shiiss.png')
    embed.add_field(name="다마고치(beta)",
                    value="키우기, 키우기캐릭터만들기, 스탯",
                    inline=False)
    embed.add_field(name="**<:icons8home144:1223867614221307965> 일반**",
                    value="핑, 패치노트, 인원통계, 타이머, 프로필, 급식, 메모쓰기, 메모불러오기, 공지사항",
                    inline=False)
    embed.add_field(name="**<:icons8search104:1223868341173882962> 검색**",
                    value="네이버검색, 유튜브검색, 블로그검색, 애니검색",
                    inline=False)
    embed.add_field(
        name="**<:icons8gamepad64:1223867175161303040> 재미**",
        value=
        "고양이, 알려주기, 급식, 호감도확인, 호감도도움말, 가위바위보, 광질, 주사위, 이모지, 골라, 메이플등록, 내메이플, 메이플m등록, 내메이플m",
        inline=False)
    embed.add_field(
        name="**<:icons8dollarcoin96:1223867173450158171> 시이코인**",
        value="주식매수, 주식매도, 가격보기, 내시이코인, 광질, 광물확인, 광물판매, 홀짝, 주사위도박, 상점, 아이템사용",
        inline=False)
    embed.add_field(name="**<:icons8mike96:1223868339919654922> 보이스**",
                    value="음성채널입장, 음성채널퇴장",
                    inline=False)
    embed.add_field(name="**<:icons8setting144:1223867437368344717> 관리**",
                    value="찬반투표, 내정보, 프로필, 클리어, 임베드생성, 욕설필터링",
                    inline=False)
    embed.add_field(
        name=
        "**Developer** by <:export202402161150235581:1207881809405288538> studio boran",
        value="",
        inline=False)
    await ctx.send(embed=embed)


@bot.hybrid_command(name='도움말', description="시이봇 메뉴얼")
async def helpss(ctx):
    embed = discord.Embed(title="안녕하세요, 시이입니다!",
                          description="귀여운 챗봇 하나쯤, 시이\n'시이야'라고 불러주세요!",
                          color=0xFFB2F5)
    embed.set_thumbnail(url='https://shii.me/shiiss.png')
    embed.add_field(name="다마고치(beta)",
                    value="키우기, 키우기캐릭터만들기, 스탯",
                    inline=False)
    embed.add_field(name="**<:icons8home144:1223867614221307965> 일반**",
                    value="핑, 패치노트, 인원통계, 타이머, 프로필, 급식, 메모쓰기, 메모불러오기, 공지사항",
                    inline=False)
    embed.add_field(name="**<:icons8search104:1223868341173882962> 검색**",
                    value="네이버검색, 유튜브검색, 블로그검색, 애니검색",
                    inline=False)
    embed.add_field(
        name="**<:icons8gamepad64:1223867175161303040> 재미**",
        value=
        "고양이, 알려주기, 급식, 호감도확인, 호감도도움말, 가위바위보, 광질, 주사위, 이모지, 골라, 메이플등록, 내메이플, 메이플m등록, 내메이플m",
        inline=False)
    embed.add_field(
        name="**<:icons8dollarcoin96:1223867173450158171> 시이코인**",
        value="주식매수, 주식매도, 가격보기, 내시이코인, 광질, 광물확인, 광물판매, 홀짝, 주사위도박, 상점, 아이템사용",
        inline=False)
    embed.add_field(name="**<:icons8mike96:1223868339919654922> 보이스**",
                    value="음성채널입장, 음성채널퇴장",
                    inline=False)
    embed.add_field(name="**<:icons8setting144:1223867437368344717> 관리**",
                    value="찬반투표, 내정보, 프로필, 클리어, 임베드생성, 욕설필터링",
                    inline=False)
    embed.add_field(
        name=
        "**Developer** by <:export202402161150235581:1207881809405288538> studio boran",
        value="",
        inline=False)
    await ctx.send(embed=embed)

global cullss
cullss = {}

@bot.hybrid_command(name='광질', description="광질을 하자")
async def mining(ctx):
    if not ok_cer(ctx.message.author.id):
        return await ctx.send("/가입 으로 가입을 먼저 해주세요!")
    elif not ok_re_cer(ctx.message.author.id):
        messages = await ctx.send("시이의 개인정보 처리방침에 개인정보의 국외 이전 항목이 업데이트 되었어요! [약관](https://shii.me/개인정보처리방침)이나 시이 프로필의 링크로 확인해주세요!")
        cer = re_cer_load()
        cer[str(ctx.message.author.id)] = True
        re_cer_save(cer)
        await asyncio.sleep(5)
        await messages.delete()
    user_id = str(ctx.message.author.id)
    server_id = str(ctx.guild.id)
    current_date = datetime.today().strftime("%Y-%M-%D")
    ttt = time.time()
    if user_id not in cullss:
        cullss[user_id] = {
            'time': ttt - 30
        }
    lests_time = cullss[user_id]['time']
    print(cullss)
    currents_time = time.time()
    coosl_time = 20
    if currents_time - lests_time < coosl_time:
        await ctx.send(
            f"쿨타임 중입니다. 20초마다 1번씩 사용이 가능합니다.", ephemeral=True)
        print(culls)
        return

    # 광질 가능한 경우 광질을 실행하고 광질 횟수를 증가시킴
    a = await ctx.send('광질을 시작합니다...')
    await asyncio.sleep(1)

    # 광질 실행 코드
    minerals = ['다이아몬드', '루비', '에메랄드', '자수정', '철', '석탄']
    weights = [1, 2, 12, 30, 50, 80]
    results = random.choices(minerals, weights=weights, k=3)
    g = results
    text1 = ''
    for i in range(0, 3):
        text = emo_re(g[i])
        text1 = f'{text} × 1' + f' {text1}'
    await ctx.send(f'{text1}' + ' 광물들을 획득하였습니다.')
    print(', '.join(results) + ' 광물들을 획득하였습니다.')
    cullss[user_id]['time'] = time.time()
    await save_minerals(str(ctx.message.author.id), ctx.guild.id, results)


@bot.hybrid_command(name='광물판매', description="광물을 판매합니다.")
async def sell(ctx):
    if not ok_cer(ctx.message.author.id):
        return await ctx.send("/가입 으로 가입을 먼저 해주세요!")
    elif not ok_re_cer(ctx.message.author.id):
        messages = await ctx.send("시이의 개인정보 처리방침에 개인정보의 국외 이전 항목이 업데이트 되었어요! [약관](https://shii.me/개인정보처리방침)이나 시이 프로필의 링크로 확인해주세요!")
        cer = re_cer_load()
        cer[str(ctx.message.author.id)] = True
        re_cer_save(cer)
        await asyncio.sleep(5)
        await messages.delete()
    minerals = await get_minerals(str(ctx.message.author.id), ctx.guild.id)
    if not minerals:
        await ctx.send("보유한 광물이 없습니다.")
        return

    total_price = 0
    for mineral in minerals:
        mineral_price = calculate_price(mineral)  # 각 광물 가격 계산 함수 필요
        total_price += mineral_price

    await clear_minerals(str(ctx.message.author.id), ctx.guild.id)
    element_counts = Counter(minerals)
    output_list = [
        f"{element}: {count}" for element, count in element_counts.items()
    ]
    await ctx.send(
        f"{', '.join(output_list)}을(를) 판매하여 총 {total_price} <:shiicoin:1211874282414673970> 시이코인을 획득하였습니다."
    )
    capital = load_capital()
    user = str(ctx.message.author.mention)
    guild = str(ctx.guild.id)
    if guild not in capital:
        capital[guild] = {}
    if user not in capital[guild]:
        capital[guild][user] = 0
    capital[guild][user] += total_price
    save_capital(capital)


@bot.hybrid_command(name='광물확인', description="보유한 광물을 확인합니다.")
async def check_minerals(ctx):
    if not ok_cer(ctx.message.author.id):
        return await ctx.send("/가입 으로 가입을 먼저 해주세요!")
    elif not ok_re_cer(ctx.message.author.id):
        messages = await ctx.send("시이의 개인정보 처리방침에 개인정보의 국외 이전 항목이 업데이트 되었어요! [약관](https://shii.me/개인정보처리방침)이나 시이 프로필의 링크로 확인해주세요!")
        cer = re_cer_load()
        cer[str(ctx.message.author.id)] = True
        re_cer_save(cer)
        await asyncio.sleep(5)
        await messages.delete()
    minerals = await get_minerals(str(ctx.message.author.id), ctx.guild.id)
    if not minerals:
        await ctx.send("보유한 광물이 없습니다.")
        return
    element_counts = Counter(minerals)
    output_list = [
        f"{element}: {count}" for element, count in element_counts.items()
    ]
    await ctx.send(f"{', '.join(output_list)}을(를) 보유하고 있습니다.")


'''메이플, 메이플m 정보 커멘드'''


@bot.hybrid_command(name="메이플등록", description="내 메이플 아이디를 등록합니다")
async def maple_register(ctx, maple_name: str):
    if not ok_cer(ctx.message.author.id):
        return await ctx.send("/가입 으로 가입을 먼저 해주세요!")
    elif not ok_re_cer(ctx.message.author.id):
        messages = await ctx.send("시이의 개인정보 처리방침에 개인정보의 국외 이전 항목이 업데이트 되었어요! [약관](https://shii.me/개인정보처리방침)이나 시이 프로필의 링크로 확인해주세요!")
        cer = re_cer_load()
        cer[str(ctx.message.author.id)] = True
        re_cer_save(cer)
        await asyncio.sleep(5)
        await messages.delete()
    headers = {
        "x-nxopen-api-key":
        ""
    }
    url_maple = f"https://open.api.nexon.com/maplestory/v1/id?character_name={maple_name}"
    response = requests.get(url_maple, headers=headers)
    data = response.json()
    if not "error" in data:
        id = data['ocid']
        maple_id = maple_id_load()
        server_id = str(ctx.guild.id)
        user_id = str(ctx.message.author.mention)
        if server_id not in maple_id:
            maple_id[server_id] = {}
        if user_id not in maple_id[server_id]:
            maple_id[server_id][user_id] = {}
        maple_id[server_id][user_id] = id

        maple_id_save(maple_id)
        await ctx.send("메이플 아이디 등록이 완료되었습니다.")
    else:
        await ctx.send("메이플 아이디가 존재하지 않습니다.")


@bot.hybrid_command(name="메이플m등록", description="내 메이플m 정보를 봅니다")
async def maple_m_character_name_d(ctx, maple_m_name: str, world_name: str):
    if not ok_cer(ctx.message.author.id):
        return await ctx.send("/가입 으로 가입을 먼저 해주세요!")
    elif not ok_re_cer(ctx.message.author.id):
        messages = await ctx.send("시이의 개인정보 처리방침에 개인정보의 국외 이전 항목이 업데이트 되었어요! [약관](https://shii.me/개인정보처리방침)이나 시이 프로필의 링크로 확인해주세요!")
        cer = re_cer_load()
        cer[str(ctx.message.author.id)] = True
        re_cer_save(cer)
        await asyncio.sleep(5)
        await messages.delete()
    headers = {
        "x-nxopen-api-key":
        ""
    }
    url_maple = f"https://open.api.nexon.com/maplestorym/v1/id?character_name={maple_m_name}&world_name={world_name}"
    response = requests.get(url_maple, headers=headers)
    data = response.json()
    if not "error" in data:
        id = data['ocid']
        maple_id = maple_m_id_load()
        server_id = str(ctx.guild.id)
        user_id = str(ctx.message.author.mention)
        if server_id not in maple_id:
            maple_id[server_id] = {}
        if user_id not in maple_id[server_id]:
            maple_id[server_id][user_id] = {}
        maple_id[server_id][user_id] = id

        maple_m_id_save(maple_id)
        await ctx.send("메이플 아이디 등록이 완료되었습니다.")
    else:
        await ctx.send("메이플 아이디가 존재하지 않습니다.")


@bot.hybrid_command(name="내메이플", description="내 메이플 정보를 봅니다")
async def maple_character_name(ctx):
    if not ok_cer(ctx.message.author.id):
        return await ctx.send("/가입 으로 가입을 먼저 해주세요!")
    elif not ok_re_cer(ctx.message.author.id):
        messages = await ctx.send("시이의 개인정보 처리방침에 개인정보의 국외 이전 항목이 업데이트 되었어요! [약관](https://shii.me/개인정보처리방침)이나 시이 프로필의 링크로 확인해주세요!")
        cer = re_cer_load()
        cer[str(ctx.message.author.id)] = True
        re_cer_save(cer)
        await asyncio.sleep(5)
        await messages.delete()
    maple_id = maple_id_load()
    server_id = str(ctx.guild.id)
    user_id = str(ctx.message.author.mention)
    if server_id in maple_id and user_id in maple_id[server_id]:
        headers = {
            "x-nxopen-api-key":
            ""
        }
        url_maple = f"https://open.api.nexon.com/maplestory/v1/character/basic?ocid={maple_id[server_id][user_id]}"
        url_stats = f"https://open.api.nexon.com/maplestory/v1/character/stat?ocid={maple_id[server_id][user_id]}"

        response = requests.get(url_maple, headers=headers)
        response_stats = requests.get(url_stats, headers=headers)

        data = response.json()
        data_stats = response_stats.json()

        if not "error" in data and not "error" in data_stats:
            STR = get_str_value(data_stats, 'STR')
            DEX = get_str_value(data_stats, 'DEX')
            INT = get_str_value(data_stats, 'INT')
            LUK = get_str_value(data_stats, 'LUK')
            HP = get_str_value(data_stats, 'HP')
            MP = get_str_value(data_stats, 'MP')
            DM = get_str_value(data_stats, '데미지')
            EDM = get_str_value(data_stats, '최종 데미지')
            IDM = get_str_value(data_stats, '최소 스텟공격력')
            MDM = get_str_value(data_stats, '최대 스텟공격력')
            K = get_str_value(data_stats, '공격력')
            KK = get_str_value(data_stats, '전투력')
            M = get_str_value(data_stats, '마력')
            MS1 = get_str_value(data_stats, '무기 숙련도')
            MS2 = get_str_value(data_stats, '방어률 무시')
            MS3 = get_str_value(data_stats, '크리티컬 확률')
            MS4 = get_str_value(data_stats, '크리티컬 데미지')
            MS5 = get_str_value(data_stats, '상태이상 내성')
            MS6 = get_str_value(data_stats, '버프 지속시간')

            embed = discord.Embed(title=f"{data['world_name']}",
                                  color=0xFFB2F5)
            embed.set_thumbnail(url=data['character_image'])
            embed.add_field(
                name=":white_small_square: 기본 정보",
                value=
                f":white_medium_small_square: **이름**: {data['character_name']}\n:white_medium_small_square: **레벨**: {data['character_level']}lv\n:white_medium_small_square: **직업**: {data['character_class']}\n:white_medium_small_square: **길드**: {data['character_guild_name']}",
                inline=False)
            embed.add_field(
                name=":white_small_square: 스탯",
                value=
                f":white_medium_small_square: **STR**: {STR}\n:white_medium_small_square: **DEX**: {DEX}\n:white_medium_small_square: **INT**: {INT}\n:white_medium_small_square: **LUK**: {LUK}\n:white_medium_small_square: **HP**: {HP}\n:white_medium_small_square: **MP**: {MP}",
                inline=False)
            embed.add_field(
                name=":white_small_square: 전투 스텟",
                value=
                f":white_medium_small_square: **데미지**: {DM}\n:white_medium_small_square: **최종 데미지**: {EDM}\n:white_medium_small_square: **최소 스텟공격력**: {IDM}\n:white_medium_small_square: **최대 스텟공격력**: {MDM}\n:white_medium_small_square: **공격력**: {K}\n:white_medium_small_square: **전투력**: {KK}\n:white_medium_small_square: **마력**: {M}\n:white_medium_small_square: **무기 숙련도**: {MS1}\n:white_medium_small_square: **방어률 무시**: {MS2}\n:white_medium_small_square: **크리티컬 확률**: {MS3}\n:white_medium_small_square: **크리티컬 데미지**: {MS4}\n:white_medium_small_square: **상태이상 내성**: {MS5}\n:white_medium_small_square: **버프 지속시간**: {MS6}",
                inline=False)
            embed.set_footer(text="Data based on NEXON Open API")
            await ctx.send(embed=embed)
        else:
            await ctx.send("메이플 아이디가 존재하지 않거나, 일시적인 오류가 발생하였습니다. 다시 시도해주세요.")
    else:
        await ctx.send("메이플 아이디를 등록해주세요.")


@bot.hybrid_command(name="내메이플m", description="내 메이플 정보를 봅니다")
async def maple_m_character_name(ctx):
    if not ok_cer(ctx.message.author.id):
        return await ctx.send("/가입 으로 가입을 먼저 해주세요!")
    elif not ok_re_cer(ctx.message.author.id):
        messages = await ctx.send("시이의 개인정보 처리방침에 개인정보의 국외 이전 항목이 업데이트 되었어요! [약관](https://shii.me/개인정보처리방침)이나 시이 프로필의 링크로 확인해주세요!")
        cer = re_cer_load()
        cer[str(ctx.message.author.id)] = True
        re_cer_save(cer)
        await asyncio.sleep(5)
        await messages.delete()
    maple_id = maple_m_id_load()
    server_id = str(ctx.guild.id)
    user_id = str(ctx.message.author.mention)
    if server_id in maple_id and user_id in maple_id[server_id]:
        headers = {
            "x-nxopen-api-key":
            ""
        }
        url_maple = f"https://open.api.nexon.com/maplestorym/v1/character/basic?ocid={maple_id[server_id][user_id]}"
        url_stats = f"https://open.api.nexon.com/maplestorym/v1/character/stat?ocid={maple_id[server_id][user_id]}"

        response = requests.get(url_maple, headers=headers)
        response_stats = requests.get(url_stats, headers=headers)

        data = response.json()
        data_stats = response_stats.json()

        if not "error" in data and not "error" in data_stats:
            STR = get_strs_value(data_stats, '전투력')
            DEX = get_strs_value(data_stats, '물리 공격력')
            INT = get_strs_value(data_stats, '마법 공격력')
            MBB = get_strs_value(data_stats, '물리 방어력')
            MB = get_strs_value(data_stats, '마법 방어력')
            HP = get_strs_value(data_stats, 'HP')
            MP = get_strs_value(data_stats, 'MP')

            embed = discord.Embed(title=f"{data['world_name']}",
                                  color=0xFFB2F5)
            embed.add_field(
                name=":white_small_square: 기본 정보",
                value=
                f":white_medium_small_square: **이름**: {data['character_name']}\n:white_medium_small_square: **레벨**: {data['character_level']}lv\n:white_medium_small_square: **직업**: {data['character_job_name']}",
                inline=False)
            embed.add_field(
                name=":white_small_square: 스텟",
                value=
                f":white_medium_small_square: **전투력**: {STR}\n:white_medium_small_square: **물리 공격력**: {DEX}\n:white_medium_small_square: **마법 공격력**: {INT}\n:white_medium_small_square: **물리 방어력**: {MBB}\n:white_medium_small_square: **마법 방어력**: {MB}\n:white_medium_small_square: **HP**: {HP}\n:white_medium_small_square: **MP**: {MP}",
                inline=False)
            embed.set_footer(text="Data based on NEXON Open API")
            await ctx.send(embed=embed)
        else:
            await ctx.send("메이플 아이디가 존재하지 않거나, 일시적인 오류가 발생하였습니다. 다시 시도해주세요.")
    else:
        await ctx.send("메이플 아이디를 등록해주세요.")


'''서버관리 커멘드'''


@bot.hybrid_command(name='프로필', description="프로필를 봅니다")
async def dp(ctx, member: discord.Member):
    if not ok_cer(ctx.message.author.id):
        return await ctx.send("/가입 으로 가입을 먼저 해주세요!")
    elif not ok_re_cer(ctx.message.author.id):
        messages = await ctx.send("시이의 개인정보 처리방침에 개인정보의 국외 이전 항목이 업데이트 되었어요! [약관](https://shii.me/개인정보처리방침)이나 시이 프로필의 링크로 확인해주세요!")
        cer = re_cer_load()
        cer[str(ctx.message.author.id)] = True
        re_cer_save(cer)
        await asyncio.sleep(5)
        await messages.delete()
    print(member)
    if not member:
        member = ctx.user
    embed = discord.Embed(color=0xFFB2F5)
    embed.set_image(url=member.avatar)
    await ctx.send(embed=embed)


'''@bot.hybrid_command(name="내정보", description='내 정보를 봅니다')
async def propill(ctx):
    if not ok_cer(ctx.message.author.id):
        return await ctx.send("/가입 으로 가입을 먼저 해주세요!")
    elif not ok_re_cer(ctx.message.author.id):
        messages = await ctx.send("시이의 개인정보 처리방침에 개인정보의 국외 이전 항목이 업데이트 되었어요! [약관](https://shii.me/개인정보처리방침)이나 시이 프로필의 링크로 확인해주세요!")
        cer = re_cer_load()
        cer[str(ctx.message.author.id)] = True
        re_cer_save(cer)
        await asyncio.sleep(5)
        await messages.delete()
    member = ctx.message.author
    roles = member.roles
    role_names = [role.name for role in roles]
    role_namess = [role.name for role in roles]
    server_id = str(ctx.guild.id)
    user_id = str(ctx.message.author.id)
    user_name = str(ctx.message.author.display_name)
    current_happiness = happiness_manager.get_user_happiness(server_id, user_id)
    server_id = str(ctx.guild.id)
    user_id = str(ctx.message.author.id)
    capital = load_capital()
    embed = discord.Embed(title=f"{user_name} 님의 정보", color=0xFFB2F5)
    if not member:
        member = ctx.user
    embed.set_thumbnail(url=member.avatar)
    embed.add_field(name="호감도", value=f":heart: {current_happiness}")
    list_length = len(role_names)
    for i in range(list_length):
        role_namess[i] = f'{role_names[i]}'
    embed.add_field(name="상태", value=member.status)
    embed.add_field(name="역할", value=f"`{role_namess}`")
    if server_id in capital and str(ctx.message.author.mention) in capital[server_id]:
        embed.add_field(name="시이코인 <:shiicoin:1211874282414673970>", value=f"{capital[server_id][str(ctx.message.author.mention)]}")
    else:
        embed.add_field(name="시이코인 <:shiicoin:1211874282414673970>", value="아직 주식을 시작하지 않았습니다.")

    await ctx.send(embed=embed)'''
'''bot.hybrid_command(name='인원통계', description="서버 인원 통계(베타)")
async def member_stats(ctx):
    if not ok_cer(ctx.message.author.id):
        return await ctx.send("/가입 으로 가입을 먼저 해주세요!")
    elif not ok_re_cer(ctx.message.author.id):
        messages = await ctx.send("시이의 개인정보 처리방침에 개인정보의 국외 이전 항목이 업데이트 되었어요! [약관](https://shii.me/개인정보처리방침)이나 시이 프로필의 링크로 확인해주세요!")
        cer = re_cer_load()
        cer[str(ctx.message.author.id)] = True
        re_cer_save(cer)
        await asyncio.sleep(5)
        await messages.delete()
    guild = ctx.guild
    total_members = guild.member_count

    role_stats = {}
    for role in guild.roles:
        if role.name != '@everyone':
            role_stats[role.name] = len(role.members)
    embed = discord.Embed(title="인원통계", description=f"총 인원: {total_members}\n", color=0xFFB2F5)
    embed.add_field(name=f"각 역할별 인원: {role_stats}", value="", inline=False)
    await ctx.send(embed=embed)'''

global coolt
coolt = {}
'''학습 챗봇 기능 및 호감도, 욕설필터링 커멘드'''


@bot.tree.command(name='가르치기', description='시이봇에게 많은걸 알려주세요!')
async def tell(interaction: discord.Interaction):
    lest_time = coolt.get(interaction.user.id, 0)
    current_time = time.time()
    cool_time = 25
    if current_time - lest_time < cool_time:
        await interaction.response.send_message(
            f"쿨타임 중입니다. 25초마다 1번씩 사용이 가능합니다.", ephemeral=True)
        print(coolt)
        return
    if not ok_cer(str(interaction.user.id)):
        return await interaction.response.send_message("/가입 으로 가입을 먼저 해주세요!")
    elif not ok_re_cer(interaction.user.id):
        cer = re_cer_load()
        cer[str(interaction.user.id)] = True
        re_cer_save(cer)
        return await interaction.response.send_message("시이의 개인정보 처리방침에 개인정보의 국외 이전 항목이 업데이트 되었어요! [약관](https://shii.me/개인정보처리방침)이나 시이 프로필의 링크로 확인해주세요!")

    black_list = black_list_load()
    if str(interaction.user.id) in black_list:
        return await interaction.response.send_message(
            f"유저님은 현제 시이 시스템을 고의로 악용한것이 확인 되어 블랙리스트에 등록 되었습니다. boran@shii.me로 문의 바랍니다."
        )

    await interaction.response.send_modal(MyModal())  # noqa
    current_time = time.time()
    if interaction.user.id in coolt:
        del coolt[interaction.user.id]
    coolt[interaction.user.id] = current_time
    print(coolt)

def re_cer_load():
    try:
        with open("cer_db.json", "r", encoding="utf-8") as f:
         return json.load(f)
    except FileNotFoundError:
        return {}

def re_cer_save(data):
    with open("cer_db.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def ok_re_cer(user):
    cer = re_cer_load()
    if str(user) in cer:
        return True
    else:
        return False



@bot.hybrid_command(name='호감도확인', description='당신과 시이간의 호감도를 확인합니다.')
async def check_happiness(ctx):
    if not ok_cer(ctx.message.author.id):
        return await ctx.send("/가입 으로 가입을 먼저 해주세요!")
    elif not ok_re_cer(ctx.message.author.id):
        messages = await ctx.send("시이의 개인정보 처리방침에 개인정보의 국외 이전 항목이 업데이트 되었어요! [약관](https://shii.me/개인정보처리방침)이나 시이 프로필의 링크로 확인해주세요!")
        cer = re_cer_load()
        cer[str(ctx.message.author.id)] = True
        re_cer_save(cer)
        await asyncio.sleep(5)
        await messages.delete()

    server_id = str(ctx.guild.id)
    member = ctx.message.author
    user_id = str(ctx.message.author.id)
    user_name = str(ctx.message.author.name)
    user_name = user_name.replace("@", "")
    user_hogam = hogamdos.cheak(user_id)
    all_ha = len(el_text_cl)
    ha_hogam = 0
    for i in range(len(el_text_num)):
        if user_hogam >= el_text_num[i]["nn"]:
            ha_hogam = ha_hogam + el_text_num[i]["n"]

    # 호감도에 따라 메시지 조건 추가
    if ctx.message.author.id == :
        message = "아버지?"
        lv = "개발자"
    elif 0 <= user_hogam <= 5:
        message = "누구더라...흐음.."
        lv = "잘 모르는 사람"
    elif 6 <= user_hogam <= 20:
        message = f"{user_name}님 이죠?"
        lv = "아는사람"
    elif 21 <= user_hogam <= 50:
        message = f"{user_name}님 방가워요~"
        lv = "같이 노는 친구"
    elif 51 <= user_hogam <= 99:
        message = f"{user_name}님!"
        lv = "편하게 부르는 사이"
    elif 100 <= user_hogam:
        message = f"{user_name}님! 반가워여~"
        lv = "매우 편한 사이"
    else:
        message = "누구더라...흐음.."
        lv = "잘 모르는 사람"
    embed = discord.Embed(title=f"시이가 보는 {user_name}", color=0xFFB2F5)
    embed.set_thumbnail(url=member.avatar)
    embed.add_field(name=":speech_balloon: 시이의 한마디",
                    value=message,
                    inline=False)
    embed.add_field(name=f":heart: {lv}",
                    value=f"호감도: {user_hogam}",
                    inline=False)
    embed.add_field(name=f"해금된 단어", value=f"{ha_hogam}/{all_ha}개")
    embed.add_field(name="도전과제", value="coming soon!")
    await ctx.send(embed=embed)


@bot.hybrid_command(name='다시배우기',
                    description="시이가 이상한걸 배웠다면 이 커멘드로 알려주세요!")
async def learn(ctx, *, message):
    if not ok_cer(ctx.message.author.id):
        return await ctx.send("/가입 으로 가입을 먼저 해주세요!")
    elif not ok_re_cer(ctx.message.author.id):
        messages = await ctx.send("시이의 개인정보 처리방침에 개인정보의 국외 이전 항목이 업데이트 되었어요! [약관](https://shii.me/개인정보처리방침)이나 시이 프로필의 링크로 확인해주세요!")
        cer = re_cer_load()
        cer[str(ctx.message.author.id)] = True
        re_cer_save(cer)
        await asyncio.sleep(5)
        await messages.delete()
    word = load_bot_info()
    if message in word:
        await ctx.send("개발자에게 DM을 성공적으로 보냈습니다! 감사합니다!")
        user = await bot.fetch_user()
        await user.send(f"신고!!!\n신고 키워드: {message}, 신고 설명:{word[message]}")
    else:
        await ctx.send("시이가 배운 내용이 아닙니다.")


def load_g_g():
    try:
        with open('goog_gu.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_g_g(g_g):
    with open('goog_gu.json', 'w') as f:
        json.dump(g_g, f)


def check_black_list(user_id: str):  # 블랙리스트 여부 확인
    black_list = black_list_load()
    if user_id in black_list:
        return True
    else:
        return False


el_text_num = {
    0: {"nn":10, "n": 1},
    1: {"nn":30, "n": 5},
    2: {"nn":50, "n": 1},
    3: {"nn":100, "n": 1},
    4: {"nn":150, "n": 1},
}
black_text = "유저님은 현제 시이 시스템을 고의로 악용한것이 확인 되어 블랙리스트에 등록 되었습니다. boran@shii.me로 문의 바랍니다."
gudok_text = "/가입으로 시이 서비스 가입을 먼저 해주세요!"
el_text_cl = {
    "반가워": {
        "t": ":unlock: 앗! 반가워요~ 히히",
        "n": 10
    },
    "게임": {
        "t": ':unlock: 아! 혹시 같이 게임하실레요?',
        "n": 30
    },
    "음성채널": {
        "t": ':unlock: 아.... /음성채널입장 이거 왜 있냐고요.... 하하 그냥 개발자님이 귀찮아서 방치 중이레요',
        "n": 30
    },
    "유튜브": {
        "t": ':unlock: 앗! 가치 유튜브 보실레여?',
        "n": 30
    },
    "애교": {
        "t": ':unlock:네?.. 어.. 이이잉...시져ㅕㅕㅕ',
        "n": 30
    },
    "뭐들어?": {
        "t": ':unlock: 앗, 류현준님의 난간이욧!',
        "n": 50
    },
    "사귀자": {
        "t": ':unlock: 앗... 조아여.. 히히',
        "n": 100
    },
    "이스터에그": {
        "t": "와... 대단해요 이걸 보시네요.... 시이가 칭찬 해드릴게여 히히",
        "n": 150
    },
    "놀자": {
        "t": "앗... 저도 심심할 찰나였는데.. 조아여!",
        "n": 30
    }
}
el_text_k = {"루아", "왜요용", "잉", "루아야", "오케이구글", "크시", "크시야"}

@bot.event
async def on_message(message):
    # 기본 정보 받아오기
    user_id = str(message.author.id)  # 유저 id
    user_id_int = message.author.id  # 유저 id(int)
    guild_id = str(message.guild.id)  # 길드 id
    fuck_on_off = load_fuck_on_off()  # 서버 욕설 필터링
    user_name = message.author.display_name  # 유저 닉네임

    if message.author.bot:
        return  # 봇이면 무시

    if guild_id not in fuck_on_off:
        fuck_on_off[guild_id] = False  # 필터링 설정 생성


    if message.content.startswith('# 시이야'):
        g_g = load_g_g()
        if str(message.guild.id) not in g_g:
            g_g[str(message.guild.id)] = True
            save_g_g(g_g)
            embed = discord.Embed(title="시이 v4.6.18 업데이트 안내", color=0xFFB2F5)
            embed.add_field(name='1. 주식 변동폭 조정 및 보유주식, 시이코인 초기화', value="너무 급격했던 주식의 변동폭이 조정됩니다. 또한 보유한 주식과 시이코인이 초기화 되었으니 이 점 참고해주세요")
            embed.add_field(name="2. 호감도확인 커멘드 리뉴얼", value="/호감도확인 커멘드의 리뉴얼이 이루어졌습니다. 시이와의 호감도를 확인해보세요!")
            embed.set_footer(text='이 메세지는 서버당 한번씩만 전해져요!')
            await message.channel.send('잠시만요.. 새 소식이 있어요')
            await message.channel.send(embed=embed)

        if not ok_cer(message.author.id):
            return await message.channel.send("/가입 으로 가입을 먼저 해주세요!")
        elif not ok_re_cer(message.author.id):
            messages = await message.channel.send("시이의 개인정보 처리방침에 개인정보의 국외 이전 항목이 업데이트 되었어요! [약관](https://shii.me/개인정보처리방침)이나 시이 프로필의 링크로 확인해주세요!")
            cer = re_cer_load()
            cer[str(message.author.id)] = True
            re_cer_save(cer)
            await asyncio.sleep(5)
            await messages.delete()

        if check_black_list(user_id):  # 블랙리스트 확인
            return await message.channel.send(black_text)
        return await message.channel.send("아아ㅏ아앜 으에에에에ㅔ ㄱ..귀 아파여..")

    if message.content.startswith('## 시이야'):
        g_g = load_g_g()
        if str(message.guild.id) not in g_g:
            g_g[str(message.guild.id)] = True
            save_g_g(g_g)
            embed = discord.Embed(title="시이 v4.6.18 업데이트 안내", color=0xFFB2F5)
            embed.add_field(name='1. 주식 변동폭 조정 및 보유주식, 시이코인 초기화', value="너무 급격했던 주식의 변동폭이 조정됩니다. 또한 보유한 주식과 시이코인이 초기화 되었으니 이 점 참고해주세요")
            embed.add_field(name="2. 호감도확인 커멘드 리뉴얼", value="/호감도확인 커멘드의 리뉴얼이 이루어졌습니다. 시이와의 호감도를 확인해보세요!")
            embed.set_footer(text='이 메세지는 서버당 한번씩만 전해져요!')
            await message.channel.send('잠시만요.. 새 소식이 있어요')
            await message.channel.send(embed=embed)
        if not ok_cer(message.author.id):
            return await message.channel.send("/가입 으로 가입을 먼저 해주세요!")
        elif not ok_re_cer(message.author.id):
            messages = await message.channel.send("시이의 개인정보 처리방침에 개인정보의 국외 이전 항목이 업데이트 되었어요! [약관](https://shii.me/개인정보처리방침)이나 시이 프로필의 링크로 확인해주세요!")
            cer = re_cer_load()
            cer[str(message.author.id)] = True
            re_cer_save(cer)
            await asyncio.sleep(5)
            await messages.delete()


        if check_black_list(user_id):
            return await message.channel.send(black_text)
        return await message.channel.send("으아아ㅏ아아아앜 갑자기 크게 말하니까 놀랐잔ㅎ아요")

    if message.content.startswith('시이야'):
        g_g = load_g_g()
        if str(message.guild.id) not in g_g:
            g_g[str(message.guild.id)] = True
            save_g_g(g_g)
            embed = discord.Embed(title="시이 v4.6.18 업데이트 안내", color=0xFFB2F5)
            embed.add_field(name='1. 주식 변동폭 조정 및 보유주식, 시이코인 초기화', value="너무 급격했던 주식의 변동폭이 조정됩니다. 또한 보유한 주식과 시이코인이 초기화 되었으니 이 점 참고해주세요")
            embed.add_field(name="2. 호감도확인 커멘드 리뉴얼", value="/호감도확인 커멘드의 리뉴얼이 이루어졌습니다. 시이와의 호감도를 확인해보세요!")
            embed.set_footer(text='이 메세지는 서버당 한번씩만 전해져요!')
            await message.channel.send('잠시만요.. 새 소식이 있어요')
            await message.channel.send(embed=embed)
        if not ok_cer(message.author.id):
            return await message.channel.send("/가입 으로 가입을 먼저 해주세요!")
        elif not ok_re_cer(message.author.id):
            messages = await message.channel.send("시이의 개인정보 처리방침에 개인정보의 국외 이전 항목이 업데이트 되었어요! [약관](https://shii.me/개인정보처리방침)이나 시이 프로필의 링크로 확인해주세요!")
            cer = re_cer_load()
            cer[str(message.author.id)] = True
            re_cer_save(cer)
            await asyncio.sleep(5)
            await messages.delete()

        if check_black_list(user_id):
            return await message.channel.send(black_text)
        if not message.content.startswith('시이야 '):
            random_text = random.choice(wordshii)
            await message.channel.send(random_text)
        if message.content.startswith('시이야 '):
            message_content = message.content[4:]
            bot_info = load_bot_info()  # 단어 파일

            hogam_user = hogamdos.cheak(user_id)
            info = bot_info.get(message_content)
            info_num = len(bot_info)
            total_member_count = 0
            for guild in bot.guilds:  # 서버수 불러오기
                if guild.name != "한국 디스코드 리스트":
                    total_member_count += guild.member_count
            ## 단어 추가시 word와 word_v2에 단어를 똑같이 추가하기!!!!
            word = {
                '얼마나 알아?': f'저는 `{info_num}`개의 단어를 알고 있어요!',
                '정보':
                f'지금 시이는 `{len(bot.guilds)}` 개의 서버 에서 `{total_member_count}명` 분들을 위해 일하고 있어요. 그리고 `{info_num}` 개의 단어를 알고 있어요!',
                'hello': '안녕하세욧!',
                '안녕': '안녕하세요. 시이 입니다!',
                '누구야': '안녕하세요. 시이 입니다!',
                '요일': ':calendar: 오늘은 {}입니다'.format(get_day_of_week()),
                '시간': ':clock9: 현재 시간은 {}입니다.'.format(get_time()),
                '코딩': '코딩은 재밌어요. 아마요',
                '시이':
                f'귀여운 챗봇 하나쯤, 시이\n시이는 {len(bot.commands) - 2} 개의 기능이 있고 {len(bot.guilds)} 서버에서 일하고 있어요!',
                '게임': f':lock: 잠만요 지금 보스전ㅇ... 아아아앜 죽었잖아요오오오오!\n-# 호감도가 {30 - hogam_user}이 모자라요! 시이와 같이 놀며 호감도를 더 쌓아보세요',
                '루아': '.....(총 장전하는 소리) 그 놈 어디 있어요?^^ 아 이미 사라졌구나... 죄송해요 :broken_heart:',
                '과자': '왜요? 사주시게요? 그럼 새우깡 하나만...',
                '뭐해?': '일하죠 일! 크흠',
                '음성채널': f':lock: 아.... /음성채널입장 이거 왜 있냐고요.... 하하\n-# 호감도가 {30 - hogam_user}이 모자라요! 시이와 같이 놀며 호감도를 더 쌓아보세요',
                '웃어': '히힛 하하하',
                '맴매': '흐에에엥ㅠㅜㅜ',
                '유튜브': f':lock: 지금 유튜브 보냐구요? 아뇨... 저 소리는 뭐냐고요? 어.. 그게요....\n-# 호감도가 {30 - hogam_user}이 모자라요! 시이와 같이 놀며 호감도를 더 쌓아보세요',
                '개발자님': '개발자님이요? 좀, 쪼잔하긴해요(소곤소곤)',
                '할말없어?': '할말이요? 할말이요? 할말이요? 할말이요? 할말이요? 할말이요? 없어요!',
                '애교': f':lock: ....네?\n-# 호감도가 {30 - hogam_user}이 모자라요! 시이와 같이 놀며 호감도를 더 쌓아보세요',
                '야근': '설마...야근 시킬 생각은 아니시죠?',
                'help': '저와 대화 하실려면 시이야 뒤에 질문을 넣어 불러주세요!',
                '음악': '우리 개발자님은 류현준님의 노래를 좋아한데요. 네, TMI네용',
                'GCP': '지금 시이봇은 GCP에서 실행되고 있습니다!',
                '뭐야': '뭐지?',
                '잘가': '잘가요!',
                '뭐들어?': f':lock: 앗, 음... 비밀이예요!\n-# 호감도가 {50 - hogam_user}이 모자라요! 시이와 같이 놀며 호감도를 더 쌓아보세요',
                '일어나': '흠냐... 으헤헤... ㅓ? 끼야ㅑㅑㅑ약 ㄴ..놀랐잖아요',
                '몇살?': '이제... 만 나이로 1살?',
                '사귀자': f':lock: ....? 어.... 아직은..\n-# 호감도가 {75 - hogam_user}이 모자라요! 시이와 같이 놀며 호감도를 더 쌓아보세요',
                '반가워': f':lock: .. 앗 안녕하세여! ㅎㅎ..\n-# 호감도가 {10 - hogam_user}이 모자라요! 시이와 같이 놀며 호감도를 더 쌓아보세요',
                '왜요용': '따라하지 마세요! :broken_heart:',
                '아니': '죄송해요...',
                '잉': '따라하지 마세요!! :broken_heart:',
                'rm -rf/': '저... 저기요?? 그건 아주 **위험한** 단어라고요..',
                '루아야': '루.아.야? 각오하세요 그건 아주 아주 **위험한** 선택이니깐요. :broken_heart:',
                '시아야': '자 따라해보세요 시.이.야 참 쉽죠?',
                '사이야': '자 따라해보세요 시.이.야 참 쉽죠? 그쵸?',
                '시리야': '아.. 그 알림 맟춰주는 얘? 자 따라해보세요 시.이.야',
                '오케이구글': '일부로 그러는거죠? 그쵸? :broken_heart:',
                '크시': '자! 따.라.해.보.세.요! 시.이.야 참 쉽죠!? :broken_heart:',
                '크시야': '자! 따.라.해.보.세.요! 시.이.야 참 쉽죠!? :broken_heart:',
                'HTML': '잘 아시죠? 이건 프로그래밍 언어가 아닌거',
                'JS': '`console.log("Hello World")`',
                '이시': '시!이!',
                '호감도': f'저랑 같이 대화하거나 /가르치기로 얻을 수 있으며 자세한 정보는 /호감도확인 에서 확인이 가능해요. 그리고 호감도를 쌓으면 볼 수 있는 **비밀 단어**들도 있으니 이 점 참고하세요!\n-# 현재 호감도: {hogam_user}',
                '이스터에그': f'음.. 아직은 이를 것 같네요.. 근데 진짜 별거 없어요...\n-# 호감도가 {150 - hogam_user}이 모자라요! 시이와 같이 놀며 호감도를 더 쌓아보세요',
                '놀자': f'앗.. 저 지금은 바빠서..\n-# 호감도가 {30 - hogam_user}이 모자라요! 시이와 같이 놀며 호감도를 더 쌓아보세요'
            }

            if message_content == '' or None:
                ran_nums = random.randint(0, len(why) - 1)
                response = why[ran_nums]
                async with message.channel.typing():
                    await asyncio.sleep(1)
                await message.channel.send(response)
                hogamdos.add(user_id, 1)
                return
            elif message_content in word.keys():
                if message_content in el_text_cl or message_content in el_text_k:
                    if message_content in el_text_k:
                        async with message.channel.typing():
                            await asyncio.sleep(1)
                        await message.channel.send(word[message_content])
                        hogamdos.add(user_id, -1)
                    else:
                        if el_text_cl[message_content]["n"] > hogam_user:
                            texts = word[message_content]
                        else:
                            texts = el_text_cl[message_content]["t"]
                        async with message.channel.typing():
                            await asyncio.sleep(1)
                        await message.channel.send(texts)
                        hogamdos.add(user_id, 1)

                else:
                    async with message.channel.typing():
                        await asyncio.sleep(1)
                    await message.channel.send(word[message_content])
                    hogamdos.add(user_id, 1)


            else:
                if info:
                    ran_num = random.randint(0, len(info) - 1)
                    author_nickname = info[ran_num]['author_nickname']
                    description = info[ran_num]['description']
                    response = f"{description}\n`{author_nickname} 님이 알려주셨어요!`"
                    async with message.channel.typing():
                        await asyncio.sleep(0.5)
                    await message.channel.send(response)
                    hogamdos.add(user_id, 1)
                else:
                    ran_nums = random.randint(0, len(why) - 1)
                    response = why[ran_nums]
                    tp_time = len(response) * 0.1
                    if tp_time >= 2.5:
                        tp_time = 2.5
                    async with message.channel.typing():
                        await asyncio.sleep(tp_time)
                    await message.channel.send(response)
                    hogamdos.add(user_id, 1)
    else:
        if fuck_on_off[guild_id]:
            content_lower = message.content.lower()
            if not message.channel.nsfw:
                if korcen.check(content_lower):
                    await message.delete()
                    message8 = await message.channel.send(
                        f"{message.author.mention}님! 욕하시면 안돼요!")
                    await asyncio.sleep(3)
                    await message8.delete()

    await bot.process_commands(message)


'''재미 커멘드'''


@bot.hybrid_command(name="골라", description="시이가 골라줍니다', '으로 후보를 나눕니다,")
async def ox(ctx, cho: str):
    if not ok_cer(ctx.message.author.id):
        return await ctx.send("/가입 으로 가입을 먼저 해주세요!")
    elif not ok_re_cer(ctx.message.author.id):
        messages = await ctx.send("시이의 개인정보 처리방침에 개인정보의 국외 이전 항목이 업데이트 되었어요! [약관](https://shii.me/개인정보처리방침)이나 시이 프로필의 링크로 확인해주세요!")
        cer = re_cer_load()
        cer[str(ctx.message.author.id)] = True
        re_cer_save(cer)
        await asyncio.sleep(5)
        await messages.delete()
    words = cho.split()
    selected_word = random.choice(words)  # 단어 리스트에서 랜덤으로 선택
    await ctx.send(f"저는 {selected_word} 이요!")


@bot.hybrid_command(name='이모지', description="이모지를 크게 보기")
async def emojis(ctx, *, emojsi: discord.Emoji):
    if not ok_cer(ctx.message.author.id):
        return await ctx.send("/가입 으로 가입을 먼저 해주세요!")
    elif not ok_re_cer(ctx.message.author.id):
        messages = await ctx.send("시이의 개인정보 처리방침에 개인정보의 국외 이전 항목이 업데이트 되었어요! [약관](https://shii.me/개인정보처리방침)이나 시이 프로필의 링크로 확인해주세요!")
        cer = re_cer_load()
        cer[str(ctx.message.author.id)] = True
        re_cer_save(cer)
        await asyncio.sleep(5)
        await messages.delete()
    for emoji in emojsi:
        # 이모지 URL을 얻어옵니다.
        emoji_url = f'https://cdn.discordapp.com/emojis/{emojsi.id}.png'
        # 임베드에 이모지를 크게 표시합니다.
        embed = discord.Embed(color=0xFFB2F5)
        embed.set_image(url=emoji_url)
        await ctx.send(embed=embed)
        break  # 첫 번째 이모지만 사용합니다.


'''기타 커멘드'''


@bot.hybrid_command(name='누적커멘드', description="누적커멘드 실행 수")
async def command_ch(ctx):
    if not ok_cer(ctx.message.author.id):
        return await ctx.send("/가입 으로 가입을 먼저 해주세요!")
    elif not ok_re_cer(ctx.message.author.id):
        messages = await ctx.send("시이의 개인정보 처리방침에 개인정보의 국외 이전 항목이 업데이트 되었어요! [약관](https://shii.me/개인정보처리방침)이나 시이 프로필의 링크로 확인해주세요!")
        cer = re_cer_load()
        cer[str(ctx.message.author.id)] = True
        re_cer_save(cer)
        await asyncio.sleep(5)
        await messages.delete()
    count = load_commmand_count()
    await ctx.send(f"{count['카운트']} 번")


@bot.event
async def on_command(ctx):
    command_count = load_commmand_count()
    if not '카운트' in command_count:
        command_count['카운트'] = 0
    command_count['카운트'] += 1
    save_command_count(command_count)


@bot.hybrid_command(name='핑', description="퐁!")
async def ping(ctx):
    message_latency = round(bot.latency * 1000, 2)
    start_times = ctx.message.created_at
    message5 = await ctx.send("메시지 핑 측정중...")
    end_time = message5.created_at
    await message5.delete()
    latency = (end_time - start_times).total_seconds() * 1000

    now = datetime.utcnow()
    uptime_seconds = now - start_time
    uptime_minutes = uptime_seconds // 60

    embed = discord.Embed(title="퐁!", color=0xFFB2F5)
    embed.add_field(name=f'REST ping', value=f"`{latency}ms`")
    embed.add_field(name=f'Gateway ping', value=f"`{message_latency}ms`")
    embed.add_field(name=f'업타임', value=f"`{uptime_minutes}`")
    list_length = len(bot.guilds)
    embed.add_field(name="서버수", value=f"`{list_length}`")
    embed.set_footer(
        text=
        f"{ctx.guild.name} | {datetime.today().strftime('%Y년 %H시 %M분 %S초')}")
    await ctx.send(embed=embed)


@bot.hybrid_command(name='타이머', description="타이머 실행")
async def set_time(ctx, seconds: int, message='타이머 종료!'):
    if not ok_cer(ctx.message.author.id):
        return await ctx.send("/가입 으로 가입을 먼저 해주세요!")
    elif not ok_re_cer(ctx.message.author.id):
        messages = await ctx.send("시이의 개인정보 처리방침에 개인정보의 국외 이전 항목이 업데이트 되었어요! [약관](https://shii.me/개인정보처리방침)이나 시이 프로필의 링크로 확인해주세요!")
        cer = re_cer_load()
        cer[str(ctx.message.author.id)] = True
        re_cer_save(cer)
        await asyncio.sleep(5)
        await messages.delete()
    if seconds >= 300:
        return await ctx.send("300초 이상은 타이머가 안됩니다!")
    await ctx.send(f'{seconds}초 후에 알림이 옵니다.')
    await asyncio.sleep(seconds)
    await ctx.send(message)


@bot.command()
async def wordlist(ctx):
    if not ctx.author.id == :
        return
    file = discord.File("bot_info.json")
    user = await bot.fetch_user()
    await user.send("파일", file=file)


@bot.hybrid_command(name="wordda", description="div only")
async def wordda(ctx, word: str):
    if not ctx.author.id == :
        return
    words = load_bot_info()
    if word in words:
        del words[word]
        save_bot_info(words)
        await ctx.send(f'{word} 삭제됨')


@bot.command()
async def userlist(ctx):
    cer = open_cer_db()
    if not ctx.author.id == :
        return
    await ctx.send(f"{len(cer)}명")


def black_list_save(black_list):
    with open("black_list.json", "w", encoding="utf-8") as make_file:
        json.dump(black_list, make_file, indent=4)


def black_list_load():
    try:
        with open("black_list.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


@bot.command()
async def bl(ctx, *, user: int):
    black_list = black_list_load()
    if not ctx.author.id == :
        return

    black_list[user] = True
    await ctx.send(f"{user} 블랙리스트에 추가됨")

    black_list_save(black_list)


@bot.command()
async def blda(ctx, *, user: int):
    black_list = black_list_load()
    if not ctx.author.id == :
        return
    if user in black_list:
        black_list[user] = False
        await ctx.send(f"{user} 블랙리스트에서 제거됨")

    black_list_save(black_list)


'''버그 발생시 예외처리'''


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.BadArgument):
        message = await ctx.send('뭔가...이상해요 다시 입력해주세요!')
        await asyncio.sleep(5)
        await message.delete()
    elif isinstance(error, ValueError):
        message = await ctx.send('뭔가...이상해요 다시 입력해주세요!')
        await asyncio.sleep(5)
        await message.delete()
    elif isinstance(error, commands.MissingRequiredArgument):
        message = await ctx.send('필요한 정보가 빠졌어요!')
        await asyncio.sleep(5)
        await message.delete()
    elif isinstance(error, commands.MissingPermissions):
        message = await ctx.send('권한이 없어요!')
        await asyncio.sleep(5)
        await message.delete()
    elif isinstance(error, commands.BotMissingPermissions):
        message = await ctx.send('시이봇의 권한이 없어요!')
        await asyncio.sleep(5)
        await message.delete()
    elif isinstance(error, commands.CommandOnCooldown):
        message = await ctx.send(
            f'쿨다운 중입니다. {error.retry_after:.2f}초 후에 다시 시도해주세요.')
        await asyncio.sleep(5)
        await message.delete()
    else:
        message = discord.Embed(title='알 수 없는 오류가 발생했어요ㅠㅠ', color=0xFF0000)
        message.set_footer(text=f'오류 로그를 개발자에게 전송하였습니다! {error}')
        message2 = await ctx.send(embed=message)
        user = await bot.fetch_user()
        await user.send(f"{error}")
        await asyncio.sleep(5)
        await message2.delete()
        raise error


'''작동'''
bot.run()
'''개발자 보란'''
'''Code by studio boran'''
