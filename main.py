import discord
from discord.ext import commands
import os

client = commands.Bot(command_prefix = '-')

@client.event
async def on_ready():

  await client.change_presence(status=discord.Status.online)

  await client.change_presence(activity=discord.Game(name="코딩"))
  print("봇 이름:",client.user.name,"봇 아이디:",client.user.id,"봇 버전:",discord.__version__)
  
@client.command(name='도움말')
async def show_help(ctx):
    embed = discord.Embed(title=":bulb: 도움말", description="관련된 명령어를 볼 수 있습니다", color=0x568A35)

    embed.add_field(name='`!문제추천`', value="백준 문제를 랜덤으로 추천해줍니다.", inline=False)
    embed.add_field(name='`!문제추천 (티어)`', value="해당 티어의 백준 문제를 랜덤으로 추천해줍니다\n티어는 알파벳 대문자 한 글자와 숫자 하나로 구성됩니다 (ex. Silver 3 -> S3)", inline=False)
    embed.add_field(name='`!문제찾기 (문제번호)`', value="해당 문제의 정보를 불러옵니다", inline=False)
    embed.add_field(name='`!틀린문제 (백준아이디)`', value="해당 아이디 사용자의 틀린 문제를 랜덤으로 골라 추천해줍니다", inline=False)        
    embed.add_field(name='`!알고리즘 (알고리즘)`', value="해당 알고리즘이 사용되는 문제를 랜덤으로 추천해줍니다\n알고리즘은 ' / '로 구분합니다 (ex. 수학 / 문자열)")
    #await ctx.send(embed=embed)
    await ctx.send('도오움말')

@client.command(name='주사위')
async def roll(ctx):
  await ctx.send('주사위를 굴립니다')
  
client.run(os.environ['token'])
