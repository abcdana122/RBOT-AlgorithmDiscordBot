from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from discord.ext import commands
import urllib, bs4, discord, random, os

client = commands.Bot(command_prefix = '!')

@client.event
async def on_ready():

  await client.change_presence(status=discord.Status.online)

  await client.change_presence(activity=discord.Game(name="코딩"))
  print("봇 이름:",client.user.name,"봇 아이디:",client.user.id,"봇 버전:",discord.__version__)

# 문제 띄워주기
def show_problem_embed(name, url, data):
    embed = discord.Embed(title=name, description=url, color=0x79ACD9)

    embed.add_field(name=data[0].text, value="시간 제한", inline=True)
    embed.add_field(name=data[1].text, value="메모리 제한", inline=True)
    embed.add_field(name=data[2].text, value="제출", inline=True)
    embed.add_field(name=data[3].text, value="정답", inline=True)
    embed.add_field(name=data[4].text, value="맞힌 사람", inline=True)
    embed.add_field(name=data[5].text, value="정답 비율", inline=True)
        
    return embed
  
@client.command(name='도움말')
async def show_help(ctx):
    embed = discord.Embed(title=":bulb: 도움말", description="관련된 명령어를 볼 수 있습니다", color=0x568A35)

    embed.add_field(name='`!문제추천`', value="백준 문제를 랜덤으로 추천해줍니다.", inline=False)
    embed.add_field(name='`!문제추천 (티어)`', value="해당 티어의 백준 문제를 랜덤으로 추천해줍니다\n티어는 알파벳 대문자 한 글자와 숫자 하나로 구성됩니다 (ex. Silver 3 -> S3)", inline=False)
    embed.add_field(name='`!문제찾기 (문제번호)`', value="해당 문제의 정보를 불러옵니다", inline=False)
    embed.add_field(name='`!틀린문제 (백준아이디)`', value="해당 아이디 사용자의 틀린 문제를 랜덤으로 골라 추천해줍니다", inline=False)        
    embed.add_field(name='`!알고리즘 (알고리즘)`', value="해당 알고리즘이 사용되는 문제를 랜덤으로 추천해줍니다\n알고리즘은 ' / '로 구분합니다 (ex. 수학 / 문자열)")
    await ctx.send(embed=embed)
    
@client.command(name='문제찾기')
async def search_problem(ctx, problem):
    try:
        url = 'https://www.acmicpc.net/problem/'+str(problem)
        
        req = Request(url)
        res = urlopen(req)
        html = res.read()
         
        soup = bs4.BeautifulSoup(html, 'html.parser')
        name = soup.find_all('span')[4].text

        target = soup.find('table', {'id':'problem-info', 'class':'table'})
        
        tbody = target.find('tbody')
        trData = tbody.find_all('tr')
        tdData = trData[0].find_all('td')
        
        await ctx.send(name)
        await ctx.send(embed=(show_problem_embed(name, url, tdData)))

    except:
        embed = discord.Embed(title="[!오류] 문제가 없습니다", color=0xFF0000)
        await ctx.send(embed=embed)
        
@client.command(name='틀린문제')
async def worng_random_problem(ctx, user_id):
    try:
        url = 'https://www.acmicpc.net/problemset?user='+user_id+'&user_solved=0'
        req = Request(url)
        res = urlopen(req)
        html = res.read()

        soup = bs4.BeautifulSoup(html, 'html.parser')

        table = soup.find('table')
        tbody = table.find('tbody')
        trData = tbody.find_all('tr')

        x = random.randrange(1, len(trData))
        target = trData[x]
        problem = target.find_all('td')[0].text
        await ctx.send(embed=search_problem(problem))
    except:
        embed = discord.Embed(title="[!오류] 틀린 문제가 없습니다", color=0xFF0000)
        return embed
  
client.run(os.environ['token'])
