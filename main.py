# import
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import urllib, bs4, discord, random

# 기본 설정
client = discord.Client()

# 도움말
def show_help():
    embed = discord.Embed(title=":bulb: 도움말", description="관련된 명령어를 볼 수 있습니다", color=0x568A35)

    embed.add_field(name='`!문제추천`', value="백준 문제를 랜덤으로 추천해줍니다.", inline=False)
    embed.add_field(name='`!문제추천 (티어)`', value="해당 티어의 백준 문제를 랜덤으로 추천해줍니다\n티어는 알파벳 대문자 한 글자와 숫자 하나로 구성됩니다 (ex. Silver 3 -> S3)", inline=False)
    embed.add_field(name='`!문제찾기 (문제번호)`', value="해당 문제의 정보를 불러옵니다", inline=False)
    embed.add_field(name='`!틀린문제 (백준아이디)`', value="해당 아이디 사용자의 틀린 문제를 랜덤으로 골라 추천해줍니다", inline=False)        
    embed.add_field(name='`!알고리즘 (알고리즘)`', value="해당 알고리즘이 사용되는 문제를 랜덤으로 추천해줍니다\n알고리즘은 ' / '로 구분합니다 (ex. 수학 / 문자열)")
    return embed

# 알고리즘 테이블 생성
def make_algorithm_table():
    url = 'https://www.acmicpc.net/problem/tags'

    req = Request(url)
    res = urlopen(req)
    html = res.read()
    soup = bs4.BeautifulSoup(html, 'lxml')

    target = soup.find('table')
    tbody = target.find('tbody')
    tdData = tbody.find_all('td')

    table = {}
    i = 0
    for td in tdData:
        try:
            name = td.a.get_text()
            if name != 'BOJ Book':
                tag = str(td.a['href']).split('/')[-1]
                i += 1
                table[name] = tag
        except:
            pass
    return table
table = make_algorithm_table()

# 알고리즘 목록 보기
def show_table(table):
    key = list(table.keys())
    embed = discord.Embed(title=":desktop: 알고리즘 목록", description="알고리즘의 명칭을 불러옵니다\n더 많은 알고리즘이 궁금하다면 https://www.acmicpc.net/problem/tags 를 참고해주세요", color=0x568A35)

    cnt = 0
    for i in range(0, len(key)-1, 2):
        embed.add_field(name=key[i], value=key[i+1])
    return embed

# 문제 띄워주기
def make_problem_embed(name, url, data):
    embed = discord.Embed(title=name, description=url, color=0x79ACD9)

    embed.add_field(name=data[0].text, value="시간 제한", inline=True)
    embed.add_field(name=data[1].text, value="메모리 제한", inline=True)
    embed.add_field(name=data[2].text, value="제출", inline=True)
    embed.add_field(name=data[3].text, value="정답", inline=True)
    embed.add_field(name=data[4].text, value="맞힌 사람", inline=True)
    embed.add_field(name=data[5].text, value="정답 비율", inline=True)
        
    return embed

# 백준 문제 추천 기능
def random_problem():
    x = random.randrange(1000, 25399)

    url = 'https://www.acmicpc.net/problem/'+str(x)

    req = Request(url)
    res = urlopen(req)
    html = res.read()

    soup = bs4.BeautifulSoup(html, 'html.parser')

    try:
        name = soup.find_all('span')[3].text
        
        target = soup.find('table', {'id':'problem-info', 'class':'table'})

        tbody = target.find('tbody')
        trData = tbody.find_all('tr')
        tdData = trData[0].find_all('td')
        return make_problem_embed(name, url, tdData)
    
    except:
        random_problem()

# 백준 문제 찾기
def search_problem(x):
    try:
        url = 'https://www.acmicpc.net/problem/'+str(x)

        req = Request(url)
        res = urlopen(req)
        html = res.read()

        soup = bs4.BeautifulSoup(html, 'html.parser')

        name = soup.find_all('span')[3].text
        
        target = soup.find('table', {'id':'problem-info', 'class':'table'})

        tbody = target.find('tbody')
        trData = tbody.find_all('tr')
        tdData = trData[0].find_all('td')
        return make_problem_embed(name, url, tdData)
    
    except:
        embed = discord.Embed(title="[!오류] 문제를 찾을 수 없습니다", color=0xFF0000)
        return embed

# 백준 틀린 문제 추천
def worng_random_problem(user_id):
    url = 'https://www.acmicpc.net/problemset?user='+user_id+'&user_solved=0'

    try:
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
        return search_problem(problem)
    
    except:
        embed = discord.Embed(title="[!오류] 틀린 문제가 없습니다", color=0xFF0000)
        return embed

# 백준 티어별 문제 추천
def random_tear_problem(tear):
    try:
        if tear == 'U':
            tear = 0
        else:
            tear_table = ['B', 'S', 'G', 'P', 'D', 'R']
            tear = (5*tear_table.index(tear[0]))+(5-int(tear[1]))+1

        url = 'https://solved.ac/problems/level/'+str(tear)

        req = Request(url)
        res = urlopen(req)
        html = res.read()

        soup = bs4.BeautifulSoup(html, 'html.parser')

        table = soup.find('table')
        tbody = table.find('tbody')
        trData = tbody.find_all('tr')

        x = random.randrange(1, len(trData))
        target = trData[x]

        problem = target.find_all('span')[0].text[1:]
        return search_problem(problem)
        
    except:
        embed = discord.Embed(title="[!오류] 티어를 찾을 수 없습니다 정확한 티어를 입력해주세요 (ex. Silver 3 -> S3)", color=0xFF0000)
        return embed

# 알고리즘 별 문제 추천
def algorithm_random_problem(a, table):
    a = a.split(' / ')
    error = 0
    url = 'https://www.acmicpc.net/problemset?sort=ac_desc&solvedac_option=xz%2Cxn&algo='
    for i in a:
        try:
            if i == a[0]:
                url += str(table[i])
            else:
                url += '%2C'+table[i]
        except:
            error = 1
            embed = discord.Embed(title="[!오류] 알고리즘을 찾을 수 없습니다\n정확한 알고리즘을 입력해주세요\n( 알고리즘의 명칭이 궁금하다면 ```!알고리즘``` )", color=0xFF0000)
            return embed
        
    if error == 0:
        url += '&algo_if=and'

    try:
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
    
        return search_problem(problem)
    
    except:
        embed = discord.Embed(title="[!오류] 조건에 맞는 알고리즘을 찾을 수 없습니다 알고리즘의 갯수를 줄여주세요", color=0xFF0000)
        return embed
    
# 봇이 준비되었을때
@client.event
async def on_ready():
    print("봇이 온라인으로 전환")
    game = discord.Game("열심히 코딩하는 중")
    await client.change_presence(status=discord.Status.online, activity=game)

# 메시지를 받았을때
@client.event
async def on_message(message):
    if message.author.bot: #봇이 보낸 메시지이면
        return

    member = str(message.author)[:-5]
    m = str(message.content)
    
    if '안녕' in message.content:
        await message.channel.send(message.author.mention+'님 안녕하세요!')

    elif m.startswith("!도움말"):
        await message.channel.send(embed=show_help())

    elif message.content.startswith("!문제추천"):
        if len(message.content) == 5:
            await message.channel.send(embed=random_problem())
        else:
            await message.channel.send(embed=random_tear_problem(m[6:]))

    elif m.startswith("!문제찾기"):
        await message.channel.send(embed=search_problem(m[6:]))

    elif m.startswith("!틀린문제"):
        await message.channel.send(embed=worng_random_problem(m[6:]))
        
    elif m.startswith("!알고리즘보기"):
        await message.channel.send(embed=show_table(table))
        
    elif m.startswith("!알고리즘"):
        await message.channel.send(embed=algorithm_random_problem(m[10:], table))
        
    elif '맞왜틀' in m or '이거 왜 틀림' in m or '분명히 맞는데' in m or '왜 틀렸지' in m:
        await message.channel.send('||코드는 거짓을 말하지 않습니다. 님이 잘못되었을... 읍읍||')
client.run(token)
