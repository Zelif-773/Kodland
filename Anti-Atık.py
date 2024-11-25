import discord
from discord.ext import commands
import os
import random

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='#', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} geri dönüşüm için hazır!')

@bot.command()
async def selam(ctx):
    await ctx.send(f'Merhaba! Ben {bot.user}, sana sıfır atık hakkında yardım etmek için buradayım!')

@bot.command()
async def geridönüşüm(ctx):
    await ctx.send(f'Yeniden değerlendirilme imkanı olan atıkların çeşitli fiziksel ve/veya kimyasal işlemlerden geçirilerek ikincil hammaddeye dönüştürülerek tekrar üretim sürecine dahil edilmesine geri dönüşüm denir. Eğer sende geri dönüşüm yaparak dünyaya katkı sağlamak istiyorsan devam et!')

@bot.command()
async def yardım(ctx):
    await ctx.send(f"""Dünyaya katkı sağlamak için kullanabileceğin komutlar (sanırım)
1. #geridönüşüm
2. #sıfıratık
3. #öneri
                
[Daha fazlası için beklemede kalın, teşekkürler]""")

@bot.command()
async def sıfıratık(ctx):
    with open('gd.png', 'rb') as f:
        picture = discord.File(f)
    await ctx.send(file=picture)

@bot.command()
async def öneri(ctx):
    img_name=random.choice(os.listdir("dosya"))
    with open(f'dosya/{img_name}', 'rb') as f:
        images = discord.File(f)
    await ctx.send(file=images)


bot.run("token")
