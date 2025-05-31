import discord
from discord.ext import commands
import numpy as np
from PIL import Image, ImageOps
from keras.models import load_model
import random
import aiohttp
import io
import os

# Model ve sınıf isimlerini yükle
model = load_model("keras_Model.h5", compile=False)
class_names = open("labels.txt", "r", encoding="utf-8").readlines()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.command(name="help")
async def help_command(ctx):
    embed = discord.Embed(
        title="🛠️ One Waste Yardım Menüsü",
        description="İşte kullanabileceğin komutlar:",
        color=0x00ff00
    )
    embed.add_field(
        name="📸 !atık-bilgi (veya bir resim gönder)",
        value="Gönderdiğin atık resmini analiz eder ve türünü tahmin eder.",
        inline=False
    )
    embed.add_field(
        name="📚 !atık-facts",
        value="Geri dönüşüm hakkında ilginç ve bilinçlendirici bilgiler verir.",
        inline=False
    )
    embed.add_field(
        name="😂 !atık-joke",
        value="Geri dönüşümle ilgili soğuk ama komik fıkralar atar.",
        inline=False
    )
    embed.add_field(
        name="👋 !hello",
        value="Bot sana selam verir!",
        inline=False
    )
    embed.set_footer(text="♻️ One Waste - Doğayı birlikte koruyalım!")
    await ctx.send(embed=embed)

@bot.event
async def on_ready():
    print(f'Bot giriş yaptı: {bot.user}')
    print(f'Aktif sunucular: {[guild.name for guild in bot.guilds]}')

@bot.command()
async def atık_joke(ctx):
    jokes = [
        "Plastik şişe dedi ki: “Beni atma, ben seni ‘şişiririm’!”",
        "Kağıt çöpe neden gitti? Çünkü sayfa sayfa dertliyim dedi.",
        "“Ah, şu cam şişeler olmasa hayat daha ‘parlak’ olurdu!”",
        "Metal kutu sinirlendi: “Beni atarsan seni ‘çöpe atarım’!”",
        "Kompost kutusu her gün dua eder: “Toprağa dönmek nasip olur inşallah.”",
        "Neden geri dönüşüm kutuları iyi dosttur? Çünkü hep ‘atığı’ paylaşırlar!",
        "“Çöpü at, dünyayı ‘toparla’!”",
        "Kağıt atık birbirine dedi ki: “Hadi biraz ‘katlanalım’!”",
        "“Geri dönüşüm olmadan, dünya ‘çöpler içinde’ kalır!”",
        "Plastik torba diğerlerine kızdı: “Siz hep ‘poşet’ gibi davranıyorsunuz!”"
    ]
    joke = random.choice(jokes)
    await ctx.send(f"♻️ Geri Dönüşüm Fıkrası:\n{joke}")

@bot.command(name="atık-facts")
async def atik_facts(ctx):
    bilgiler = [
        "♻️ Bir plastik şişe geri dönüştürüldüğünde, 3 tane yeni şişe yapılabilir!",
        "🌳 Kağıt geri dönüşümü sayesinde, bir ağaç yaklaşık 4 defa kurtarılabilir.",
        "🕰️ Cam atıklar 4000 yıldan fazla bozulmadan kalabilir, ama geri dönüştürülürse sonsuza kadar tekrar tekrar kullanılabilir.",
        "⚡ Alüminyum kutu geri dönüşümü, enerjinin %95’ini tasarruf eder.",
        "🚮 Geri dönüşüm, çöplüklerdeki atık miktarını azaltarak doğayı korur.",
        "🌍 Doğru atık ayrıştırma, karbon ayak izimizi küçültür ve gezegenimizi korur.",
        "📦 Karton kutuların geri dönüşümü sayesinde her yıl milyonlarca ağaç kesilmekten kurtuluyor.",
        "💡 Elektronik atıklar (e-atık) doğru şekilde ayrıştırılmazsa ağır metaller çevreyi kirletir.",
        "🛍️ Plastik poşetler doğada 500 yıla kadar kalabilir, onları azaltmak çok önemli.",
        "🚲 Geri dönüşüm atıkları enerji tasarrufu sağlayarak, fosil yakıt kullanımını azaltır.",
        "🍃 Organik atıklar kompost yapılarak bahçe toprağına dönüştürülebilir ve kimyasal gübre ihtiyacını azaltır.",
        "🌊 Plastik atıklar deniz canlılarının yaşamını tehdit eder, doğru ayrıştırmak onları kurtarır.",
        "♻️ Geri dönüşüm sadece atığı azaltmakla kalmaz, yeni iş imkanları da yaratır.",
        "🌱 Daha az atık, daha temiz hava ve daha sağlıklı bir çevre demektir.",
        "🚯 Dünya genelinde her dakika 1 milyon plastik poşet kullanılıyor!",
        "♻️ Metal kutular sonsuz kez geri dönüştürülebilir, yani hiç bitmezler!",
        "🌎 Dünyada üretilen atıkların sadece %9'u geri dönüştürülüyor.",
        "⚠️ Elektronik atıkların %70'i yanlış şekilde çöpe atılıyor, bu da çevreye zarar veriyor.",
        "🧴 Kozmetik ürünlerin ambalajlarının çoğu plastik, bunları geri dönüştürmek önemli.",
        "🌿 Organik atıkların çürümesiyle oluşan metan gazı, sera gazları arasında çok güçlüdür.",
        "📱 Eski telefonlarınızı geri vererek nadir metallerin tekrar kullanılmasını sağlayabilirsiniz.",
        "🚮 Geri dönüşüm sayesinde her yıl milyonlarca ton sera gazı emisyonu önleniyor.",
        "🥤 Plastik pipetler ve ambalajlar, okyanuslardaki en büyük kirlilik kaynaklarından biridir.",
        "♻️ Geri dönüşüm, doğal kaynakların tüketimini azaltır ve doğayı korur.",
        "🧹 Evde atık ayrıştırmak, dünyaya katkıda bulunmanın en kolay yollarından biridir.",
        "🌏 Plastik atıklar okyanus canlılarının midesinde parçalanıyor ve onları zehirliyor.",
        "📉 Reduce, Reuse, Recycle (Azalt, Yeniden kullan, Geri dönüştür) – atık yönetiminde en etkili üç kural!",
        "🏞️ Plastik kullanımını azaltmak, su ve toprak kirliliğini de önler.",
        "🛒 Alışverişte bez torba kullanmak, plastik atık miktarını önemli ölçüde düşürür.",
        "🚴‍♀️ Geri dönüşüm sektöründe çalışanlar, dünyayı temiz tutmaya yardımcı kahramanlardır."
    ]
    secilen_bilgi = random.choice(bilgiler)
    await ctx.send(secilen_bilgi)

@bot.command(name="atık-bilgi")
async def atik_bilgi(ctx):
    attachments = ctx.message.attachments
    if not attachments:
        await ctx.send("Lütfen analiz etmek için bir resim gönder!")
        return

    image_attachment = None
    for attachment in attachments:
        if any(attachment.filename.lower().endswith(ext) for ext in [".png", ".jpg", ".jpeg"]):
            image_attachment = attachment
            break

    if image_attachment is None:
        await ctx.send("Lütfen geçerli bir resim dosyası (.png, .jpg, .jpeg) gönder!")
        return

    await ctx.send("♻️ Atık resmi alındı, Luffy analiz ediyor...")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(image_attachment.url) as resp:
                if resp.status != 200:
                    await ctx.send('Resim indirilemedi, tekrar dene!')
                    return
                data_bytes = await resp.read()

        image = Image.open(io.BytesIO(data_bytes)).convert("RGB")
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        data[0] = normalized_image_array

        prediction = model.predict(data)
        index = np.argmax(prediction)
        class_name = class_names[index].strip()
        confidence_score = prediction[0][index]

        class_name = " ".join(class_name.split(" ")[1:]) if " " in class_name else class_name

        file_name = f"{class_name}.txt"
        if os.path.exists(file_name):
            with open(file_name, "r", encoding="utf-8") as f:
                suggestion = f.read()
        else:
            suggestion = "Bu atık için bilgi bulunmamaktadır."

        embed = discord.Embed(
            title="♻️ One Waste Atık Sınıflandırma",
            description=f"Sunucu: **{ctx.guild.name}**",
            color=0xff4500
        )
        embed.set_author(name="   🏴‍☠️ Monkey D. Luffy 🏴‍☠️",
                         icon_url="https://static.wikia.nocookie.net/onepiece/images/1/17/Monkey_D_Luffy_Anime_Post_Timeskip_Infobox.png")
        embed.add_field(name="Tahmin Edilen Atık", value=class_name, inline=False)
        embed.add_field(name="Güven Skoru", value=f"{confidence_score:.2f}", inline=False)
        embed.add_field(name="Atık Hakkında Bilgi", value=suggestion, inline=False)
        embed.set_footer(text="One Waste - Geri dönüşüm korsanları bir arada!")

        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(f"Hata oluştu: {e}")

@bot.command()
async def hello(ctx):
    await ctx.send(f'Selam! Ben {bot.user}')

bot.run("token")
