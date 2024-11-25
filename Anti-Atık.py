import discord
from discord.ext import commands
import asyncio
import os
import random

# Geri dönüşüm komutları ve mesajları
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='#', intents=intents)

# Bot açıldığında çalışacak event
@bot.event
async def on_ready():
    print(f'{bot.user} geri dönüşüm için hazır!')

# Komutlar

@bot.command()
async def selam(ctx):
    await ctx.send(f'Merhaba! Ben {bot.user}, sana sıfır atık hakkında yardımcı olmak için buradayım!')

@bot.command()
async def geridönüşüm(ctx):
    await ctx.send(f'Yeniden değerlendirilme imkanı olan atıkların çeşitli fiziksel ve/veya kimyasal işlemlerden geçirilerek ikincil hammaddeye dönüştürülüp tekrar üretim sürecine dahil edilmesine geri dönüşüm denir. Hadi sen de geri dönüşüm yaparak dünyaya katkı sağla!')

@bot.command()
async def yardım(ctx):
    """Kullanıcıya mevcut komutları gösterir."""
    await ctx.send("""
Dünyaya katkı sağlamak için kullanabileceğin komutlar:
                   
1 - #geridönüşüm
2 - #sıfıratık
3 - #öneri
4 - #atıktürü {atık}
5 - #ipucu
6 - #quiz
7 - #bilgi

[Daha fazlası için beklemede kalın!]
""")

#Sıfır Atık

@bot.command()
async def sıfıratık(ctx):
    try:
        with open('gd.png', 'rb') as f:
            picture = discord.File(f)
        await ctx.send(file=picture)
    except FileNotFoundError:
        await ctx.send('Görsel bulunamadı! Lütfen "gd.png" dosyasının doğru dizinde olduğunu kontrol et.')

#Öneri

@bot.command()
async def öneri(ctx):
    img_name = random.choice(os.listdir("dosya"))
    with open(f'dosya/{img_name}', 'rb') as f:
        images = discord.File(f)
    await ctx.send(file=images)

#Atık Türü

@bot.command()
async def atıktürü(ctx, tur=None):

    if tur is None:
        await ctx.send("Lütfen hangi atık türü hakkında bilgi istediğinizi belirtin!")
    else:
        tur = tur.lower() 
        if tur == "plastik":
            await ctx.send("Plastikler genellikle geri dönüştürülebilir. Su şişeleri, plastik poşetler ve diğer plastik malzemeler geri dönüşüme gönderilebilir. Ancak bazı plastik türleri geri dönüştürülemez.")
        elif tur == "kağıt":
            await ctx.send("Kağıtlar geri dönüştürülebilir. Gazeteler, dergiler, karton kutular ve bazı ambalajlar geri dönüşüme dahil edilebilir. Ancak, yağlı kağıtlar geri dönüştürülemez.")
        elif tur == "cam":
            await ctx.send("Cam, tamamen geri dönüştürülebilir. Şişeler, kavanozlar ve diğer cam ürünler geri dönüştürülebilir ve tekrar kullanılabilir.")
        elif tur == "metal":
            await ctx.send("Metaller, özellikle alüminyum ve çelik, geri dönüştürülebilir. İçki kutuları, eski otomobil parçaları ve mutfak eşyaları geri dönüştürülebilir.")
        elif tur == "organik":
            await ctx.send("Organik atıklar, doğaya zarar vermeden kompost haline getirilebilir. Mutfak atıkları, meyve ve sebze kabukları bu grupta yer alır.")
        elif tur == "elektronik":
            await ctx.send("Elektronik atıklar (e-atık) geri dönüştürülebilir ancak özel işleme gerektirir. Eski telefonlar, bilgisayarlar, televizyonlar ve bataryalar bu grupta yer alır.")
        elif tur == "tehlikeli":
            await ctx.send("Tehlikeli atıklar, özel geri dönüşüm süreçlerine ihtiyaç duyar. Kimyasal maddeler, ilaçlar, bataryalar ve bazı temizlik ürünleri bu türdendir.")
        elif tur == "tekstil":
            await ctx.send("Eski giysiler ve kumaşlar geri dönüştürülebilir. Ancak bazı kumaşlar, özellikle sentetikler, geri dönüşüm için uygun değildir.")
        elif tur == "ahşap":
            await ctx.send("Ahşap, geri dönüşüm için uygundur ancak ahşap işleme atıkları ve boyalı ahşaplar genellikle geri dönüştürülemez.")
        elif tur == "kapsüller":
            await ctx.send("Kapsüller (örneğin kahve kapsülleri), genellikle geri dönüştürülebilir. Ancak bu tür ürünlerin geri dönüşümü yerel tesislere bağlıdır.")
        elif tur == "dondurulmuş gıda":
            await ctx.send("Dondurulmuş gıda ambalajları genellikle geri dönüştürülebilir. Plastik veya karton ambalajlar çoğu zaman geri dönüşüme uygundur.")
        elif tur == "parfüm şişeleri":
            await ctx.send("Parfüm şişeleri cam veya plastikten yapılmış olabilir. Cam şişeler geri dönüştürülebilir, ancak plastik olanlar yerel geri dönüşüm kurallarına bağlıdır.")
        else:
            await ctx.send(f"{tur} hakkında maalesef elimde bilgi yok... Yoksa bilerek mi yanlış yazdın?🤔")

#İpucu

@bot.command()
async def ipucu(ctx):
    ipucları = [
        "Tek kullanımlık plastikleri bırakın ve yeniden kullanılabilir malzemeler kullanın. Örneğin, bir metal su şişesi alabilirsiniz.",
        "Kompost yaparak organik atıkları geri kazanın. Meyve kabukları, sebze atıkları ve kahve telvesi kompost için idealdir.",
        "Atıkları azaltmak için alışverişlerinizde paketleme malzemelerini minimumda tutun. Bez çantalar ve geri dönüştürülebilir ambalajları tercih edin.",
        "Geri dönüşüm kutularınızı doğru şekilde sınıflandırın. Her tür atık için ayrı kutular kullanarak doğru bir şekilde geri dönüşüm yapabilirsiniz.",
        "Yeniden kullanılabilir kahve fincanları ve pipetler kullanarak tek kullanımlık plastikleri azaltın.",
        "Alışverişlerde daha az ambalajlanmış ürünleri tercih edin. Örneğin, sebze ve meyveleri doğrudan pazardan alabilirsiniz.",
        "Evde kullanılan enerji tüketimini azaltın. Elektronik cihazları kullanmadığınız zamanlarda kapalı tutarak enerji tasarrufu sağlayın.",
        "Plastik yerine cam, metal veya ahşap malzemeler kullanın. Bu malzemeler geri dönüştürülebilir ve doğa dostudur.",
        "Eski giysileri atmak yerine, onarın veya yeniden kullanın. Giysilerinizi bağışlayarak ihtiyacı olanlara verebilirsiniz.",
        "Sıfır atık yaşam tarzı için, ürünleri tam olarak kullanın. Örneğin, gıda atıklarını minimize etmek için doğru porsiyonlar hazırlayın.",
        "Evde doğal temizlik malzemeleri kullanın. Sirke, karbonat ve limon gibi maddelerle doğal temizleyiciler yapabilirsiniz.",
        "Dijital dosyalarınızı düzenleyerek kağıt kullanımını azaltın. E-faturalar, dijital belgeler ve notlar kullanarak kağıt israfını engelleyin.",
        "Yeniden kullanılabilir ambalajlar kullanarak, alışverişten sonra plastik poşet kullanımını azaltın.",
        "Fazla elektrikli cihazlar yerine manuel cihazlar kullanarak enerji tüketimini düşürün. Örneğin, elektrikli süpürge yerine saplı süpürge kullanın.",
        "Hızlı moda yerine uzun ömürlü ve kaliteli ürünler satın alarak, modaya uygun ama çevre dostu seçimler yapın.",
        "Çevre dostu kişisel bakım ürünleri kullanın. Plastik ambalajlı ürünler yerine, kutu veya cam ambalajlı ürünleri tercih edin."
    ]
    ipucu = random.choice(ipucları)
    await ctx.send(f"İşte bir sıfır atık ipucu geliyor! : {ipucu}")

#Quiz

@bot.command()
async def quiz(ctx):

    sorular = [
        {
            "soru": "Hangisi geri dönüştürülebilir?",
            "şıklar": ["Alüminyum kutular", "Plastik poşetler", "Yemek atıkları", "Cam kırıkları"],
            "doğrucevap": "Alüminyum kutular"
        },
        {
            "soru": "Sıfır atık yaşam tarzına geçmek için hangi alışkanlık daha faydalıdır?",
            "şıklar": ["Yeniden kullanılabilir su şişeleri kullanmak", "Her gün tek kullanımlık plastik kullanmak", "Geri dönüşüme atık bırakmamak", "Evde enerji tüketimini artırmak"],
            "doğrucevap": "Yeniden kullanılabilir su şişeleri kullanmak"
        },
        {
            "soru": "Aşağıdakilerden hangisi geri dönüştürülemez?",
            "şıklar": ["Kağıt", "Plastik şişeler", "Yıkanmış cam şişeler", "Yağlı pizza kutusu"],
            "doğrucevap": "Yağlı pizza kutusu"
        },
        {
            "soru": "Kompost yapmak için hangi malzeme kullanılabilir?",
            "şıklar": ["Meyve ve sebze kabukları", "Plastik poşetler", "Metal parçalar", "Kimyasal temizlik malzemeleri"],
            "doğrucevap": "Meyve ve sebze kabukları"
        },
        {
            "soru": "Geri dönüşümde hangi plastik türü en sık kullanılır?",
            "şıklar": ["PET (Polietilen Tereftalat)", "PVC (Polivinil Klorür)", "PS (Polistiren)", "HDPE (Yüksek Yoğunluklu Polietilen)"],
            "doğrucevap": "PET (Polietilen Tereftalat)"
        },
        {
            "soru": "Sıfır atık hareketinin temel amacı nedir?",
            "şıklar": ["Atıkları en aza indirmek", "Geri dönüşümü teşvik etmek", "Çevreyi korumak", "Tüm seçenekler doğru"],
            "doğrucevap": "Tüm seçenekler doğru"
        },
        {
            "soru": "Sıfır atık felsefesi ile ilgili aşağıdakilerden hangisi yanlıştır?",
            "şıklar": ["Atık üretmek gereksizdir", "Geri dönüşüm her zaman çözümdür", "Atıkları azaltmak çevreye yardımcı olur", "Sıfır atık hedefi, tek kullanımlık ürünlerin kullanımını en aza indirmeyi amaçlar"],
            "doğrucevap": "Geri dönüşüm her zaman çözümdür"
        },
        {
            "soru": "Hangi madde plastik yerine kullanılabilir?",
            "şıklar": ["Ahşap", "Metal", "Cam", "Tüm seçenekler"],
            "doğrucevap": "Tüm seçenekler"
        },
        {
            "soru": "Sıfır atık alışveriş için hangi malzeme daha uygundur?",
            "şıklar": ["Plastik torba", "Kağıt poşet", "Bez çanta", "Alüminyum kutu"],
            "doğrucevap": "Bez çanta"
        },
        {
            "soru": "Hangi ürün geri dönüşüme gönderilmemelidir?",
            "şıklar": ["Açık meyve ve sebzeler", "Boya kutuları", "Eski kitaplar", "Büzgülü şişeler"],
            "doğrucevap": "Boya kutuları"
        }
    ]

    soru = random.choice(sorular)
    cevaplar = soru["şıklar"]
    random.shuffle(cevaplar)
    
    await ctx.send(f"Soru: {soru['soru']}\n" + "\n".join([f"{i+1}. {cevaplar[i]}" for i in range(len(cevaplar))]))
    
    def check(m):
        return m.author == ctx.author and m.content.isdigit()
    
    try:
        msg = await bot.wait_for('message', check=check, timeout=30.0)
        if cevaplar[int(msg.content) - 1] == soru['doğrucevap']:
            await ctx.send("Doğru! Başarabileceğini biliyordum🎉 (hayır bilmiyordum)")
        else:
            await ctx.send(f"Yanlış! Bir dahakine doğru yap👍 (bu bir rica değil): {soru['doğrucevap']}")
    except asyncio.TimeoutError:
        await ctx.send("Zaman doldu! Biraz daha hızlı olman gerek yoksa bu iş olmaz😑")

# İstatistik / Bilgi

@bot.command()
async def bilgi(ctx):

    istatistikler = [
        "Dünyada geri dönüşüm oranı yalnızca %9'dur. Bu, geri dönüşüm için büyük bir potansiyel olduğunu gösteriyor!",
        "Bir ton alüminyum geri dönüştürülerek 14,000 kWh enerji tasarrufu sağlanabilir.",
        "Geri dönüşüm, karbon ayak izini %30 oranında azaltabilir.",
        "Sıfır atık yaşam tarzı, atıkların %90'ından fazlasının yeniden kullanılmasını veya geri dönüştürülmesini sağlar.",
        "Her yıl okyanuslara 8 milyon ton plastik atık bırakılmaktadır.",
        "Geri dönüşümde en çok karışan maddeler cam, plastik, metal ve kağıttır. Ancak bazı kirli ve karışık atıklar geri dönüşüm sürecini engelleyebilir.",
        "Bir ton kağıt geri dönüştürmek, 17 ağacın kesilmesini engeller.",
        "Bir plastik şişenin doğada çözünmesi 450 yıl sürebilir.",
        "Geri dönüşüm, her yıl milyonlarca ton atığın depolama alanlarına gitmesini engeller.",
        "Yeniden kullanılabilir su şişeleri kullanarak, her yıl tonlarca plastik atık birikmesini engelleyebilirsiniz.",
        "Plastik şişelerin geri dönüşümü, orijinal plastik şişe üretiminden %75 daha az enerji harcar."
    ]
    
    istatistik = random.choice(istatistikler) 
    await ctx.send(istatistik)


# Botu çalıştırma
bot.run("token")
