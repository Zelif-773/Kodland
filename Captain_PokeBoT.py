import discord
from discord.ext import commands
from discord.ui import View, Button
import sqlite3
import json
import random
import asyncio

# JSON dosyasından Pokémon verilerini yükleme
with open("Kodland\Others\sea_pokemons.json", "r") as json_file:
    pokemon_data = json.load(json_file)

# Bot prefixleri
prefixes = ["poke ", "p ", "$"]
bot = commands.Bot(command_prefix=prefixes, intents=discord.Intents.all())

# Veritabanı bağlantısı (her komut için açılacak)
def get_db_connection():
    return sqlite3.connect('pokemon_bot.db')

# Bot hazır olduğunda
@bot.event
async def on_ready():
    print("CaptainPokeBoT hizmetinizde efendim!")

# Kullanıcı bakiyesini kontrol etme
def get_balance(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM players WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

# Kullanıcıyı veritabanına ekleme
def add_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO players (user_id, balance) VALUES (?, ?)", (user_id, 100))
    conn.commit()
    conn.close()

# Veritabanında yeni Pokémon ekleme
def add_pokemon(user_id, pokemon_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO inventory (user_id, pokemon_id) VALUES (?, ?)", (user_id, pokemon_id))
    conn.commit()
    conn.close()

@bot.command(name="catch")
@commands.cooldown(1, 10, commands.BucketType.user)  # 10 saniye bekleme süresi
async def catch(ctx):
    user_id = str(ctx.author.id)

    # Kullanıcı veritabanında mı?
    balance = get_balance(user_id)
    if balance is None:
        add_user(user_id)
        balance = 100

    # Yeterli PokéCash kontrolü
    if balance < 10:
        await ctx.send("Yeterli PokéCash'iniz yok. Bir Pokémon yakalamak için en az 10 PokéCash'e ihtiyacınız var.")
        return

    # PokéCash azaltma
    new_balance = balance - 10
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE players SET balance = ? WHERE user_id = ?", (new_balance, user_id))
    conn.commit()

    # Rastgele bir Pokémon yakala
    pokemon = random.choice(pokemon_data)

    # Pokémon'u envantere ekle
    add_pokemon(user_id, pokemon["id"])

    # Yakalanan Pokémon bilgisi
    embed = discord.Embed(
        title=f"{ctx.author.display_name} bir Pokémon yakaladı!",
        description=f"**Pokémon**: {pokemon['name']}\n"
                    f"**Tür**: {', '.join(pokemon['types'])}",
        color=discord.Color.blue()
    )
    embed.set_image(url=pokemon["sprite"])
    await ctx.send(embed=embed)

# AutoCatch komutu
@bot.command(name="autocatch")
async def autocatch(ctx, poke_cash: int):
    user_id = str(ctx.author.id)

    # Kullanıcı veritabanında mı?
    balance = get_balance(user_id)
    if balance is None:
        await ctx.send("Henüz oyunda değilsiniz. Bir Pokémon yakalayarak başlayabilirsiniz!")
        return

    # Minimum PokéCash kontrolü
    if poke_cash < 50:
        await ctx.send("AutoCatch başlatmak için en az 50 PokéCash harcamalısınız.")
        return

    if balance < poke_cash:
        await ctx.send("Yeterli PokéCash'iniz yok.")
        return

    # PokéCash azaltma
    new_balance = balance - poke_cash
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE players SET balance = ? WHERE user_id = ?", (new_balance, user_id))
    conn.commit()

    # Yakalama miktarı ve süresi
    num_pokemons = poke_cash // 20
    time_to_complete = (poke_cash // 50) * 5  # Her 50 PokéCash için 5 dakika

    # Pokémonları yakala ve ekle
    caught_pokemons = random.sample(pokemon_data, num_pokemons)
    for pokemon in caught_pokemons:
        add_pokemon(user_id, pokemon["id"])

    # Yakalanan Pokémon bilgisi
    embed = discord.Embed(
        title=f"{ctx.author.display_name} AutoCatch başlattı!",
        description=f"{time_to_complete} dakika içinde {num_pokemons} Pokémon yakalanacak.",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

    # Yakalama işlemini bekle
    await asyncio.sleep(time_to_complete * 60)

    # İşlem tamamlandıktan sonra bilgilendirme
    embed = discord.Embed(
        title=f"{ctx.author.display_name}, AutoCatch tamamlandı!",
        description=f"Yakalanan Pokémon sayısı: {num_pokemons}",
        color=discord.Color.gold()
    )
    await ctx.send(embed=embed)

@bot.command(name="pokedesk")
async def pokedesk(ctx):
    user_id = str(ctx.author.id)

    # Kullanıcının envanterindeki Pokémonları al
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT pokemon_id, COUNT(pokemon_id) FROM inventory WHERE user_id = ? GROUP BY pokemon_id", (user_id,))
    inventory = cursor.fetchall()
    conn.close()

    if not inventory:
        await ctx.send("Envanterinizde hiçbir Pokémon yok!")
        return

    # Pokémon bilgilerini oluştur
    pokedesk_pages = []
    pokedesk_page = discord.Embed(title=f"{ctx.author.display_name}'s Pokedesk", color=discord.Color.purple())
    
    sprite_count = 0  # Sprite sayısını saymak için bir sayaç

    for index, (pokemon_id, count) in enumerate(inventory, start=1):
        pokemon = next((p for p in pokemon_data if p["id"] == pokemon_id), None)
        if not pokemon:
            continue

        # Eğer 1-3 Pokémon varsa, sprite'ı ekle ve her sprite için altına açıklama ekle
        if count <= 3:
            sprite_url = pokemon["sprite"]
            if sprite_count < 3:  # 3 Pokémon'dan fazla resim eklenmesin
                pokedesk_page.set_image(url=sprite_url)  # Resmi ekle
                sprite_count += 1

        # Pokémon bilgilerini sayfada göster
        pokedesk_page.add_field(
            name=f"ID: {pokemon['id']} - {pokemon['name']} (x{count})",
            value=f"**Tür**: {', '.join(pokemon['types'])}\n**Nadirlik**: {pokemon['rarity']}",
            inline=False
        )

        # Her 25 Pokémon'da yeni bir sayfa oluştur
        if index % 25 == 0:
            pokedesk_pages.append(pokedesk_page)
            pokedesk_page = discord.Embed(title=f"{ctx.author.display_name}'s Pokedesk (Devam)", color=discord.Color.purple())

    # Kalan Pokémonlar için sayfa ekle
    if len(pokedesk_page.fields) > 0:
        pokedesk_pages.append(pokedesk_page)

    # Sayfaları gönder
    for page in pokedesk_pages:
        await ctx.send(embed=page)

# Pokémon satma komutu
@bot.command(name="sell")
async def sell(ctx, pokemon_id: str):
    user_id = str(ctx.author.id)

    if pokemon_id.lower() == "all":
        # Kullanıcının tüm Pokémon'larını satma işlemi
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT pokemon_id FROM inventory WHERE user_id = ?", (user_id,))
        all_pokemons = cursor.fetchall()

        if not all_pokemons:
            await ctx.send("Satacak Pokémon'unuz yok!")
            return

        total_cash = 0
        for (pokemon_id,) in all_pokemons:
            pokemon = next((p for p in pokemon_data if p["id"] == pokemon_id), None)
            if pokemon:
                rarity = pokemon["rarity"]
                if rarity == "Common":
                    total_cash += 10
                elif rarity == "Uncommon":
                    total_cash += 20
                elif rarity == "Rare":
                    total_cash += 50
                elif rarity == "Legendary":
                    total_cash += 100
                elif rarity == "Mythical":
                    total_cash += 200

        # Pokémon'ları veritabanından sil
        cursor.execute("DELETE FROM inventory WHERE user_id = ?", (user_id,))
        conn.commit()

        # Kullanıcı bakiyesine ekleme
        cursor.execute("SELECT balance FROM players WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        new_balance = result[0] + total_cash
        cursor.execute("UPDATE players SET balance = ? WHERE user_id = ?", (new_balance, user_id))
        conn.commit()

        await ctx.send(f"Tüm Pokémon'larınızı sattınız ve toplamda {total_cash} PokéCash kazandınız!")
        conn.close()
        return

    # Belirli bir Pokémon'u satma işlemi
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventory WHERE user_id = ? AND pokemon_id = ?", (user_id, int(pokemon_id)))
    pokemon = cursor.fetchone()

    if not pokemon:
        await ctx.send("Bu Pokémon sizde bulunmuyor!")
        conn.close()
        return

    pokemon_details = next((p for p in pokemon_data if p["id"] == int(pokemon_id)), None)
    if not pokemon_details:
        await ctx.send("Geçersiz Pokémon ID'si!")
        conn.close()
        return

    rarity = pokemon_details["rarity"]
    if rarity == "Common":
        cash_earned = 10
    elif rarity == "Uncommon":
        cash_earned = 20
    elif rarity == "Rare":
        cash_earned = 50
    elif rarity == "Legendary":
        cash_earned = 100
    elif rarity == "Mythical":
        cash_earned = 200

    # Pokémon'u veritabanından sil
    cursor.execute("DELETE FROM inventory WHERE user_id = ? AND pokemon_id = ?", (user_id, int(pokemon_id)))
    conn.commit()

    # Kullanıcı bakiyesine ekleme
    cursor.execute("SELECT balance FROM players WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    new_balance = result[0] + cash_earned
    cursor.execute("UPDATE players SET balance = ? WHERE user_id = ?", (new_balance, user_id))
    conn.commit()

    await ctx.send(f"{pokemon_details['name']} adlı Pokémon'unuzu sattınız ve {cash_earned} PokéCash kazandınız!")
    conn.close()

# Kullanıcı bakiyesini gösterme
@bot.command(name="balance")
async def balance(ctx):
    user_id = str(ctx.author.id)
    balance = get_balance(user_id)
    if balance is None:
        # Yeni kullanıcıya 100 PokéCash ekle
        add_user(user_id)
        await ctx.send(f"Yeni bir eğitmen görüyorum! İşe bak ki havadan 100 PokéCash indi! Başarılar, {ctx.author.display_name}!")
        balance = 100

    await ctx.send(f"{ctx.author.display_name}, şu anki bakiyen: {balance} PokéCash.")

# Sadece detemmienati0n yetkilendirilir
def is_owner(ctx):
    return ctx.author.id == 1296512620966187049 # detemmienati0n ID'si

# Kullanıcıya para ekleme
@bot.command(name="addcash")
@commands.check(is_owner)
async def add_cash(ctx, user_id: str, amount: int):
    if amount < 0:
        await ctx.send("Negatif bir miktar ekleyemezsin.")
        return

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT balance FROM players WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()

    if result:
        new_balance = result[0] + amount
        cursor.execute("UPDATE players SET balance = ? WHERE user_id = ?", (new_balance, user_id))
    else:
        cursor.execute("INSERT INTO players (user_id, balance) VALUES (?, ?)", (user_id, amount))

    conn.commit()
    conn.close()
    await ctx.send(f"Kullanıcı {user_id}'e {amount} PokéCash eklendi.")

# Kullanıcıdan para alma
@bot.command(name="removecash")
@commands.check(is_owner)
async def remove_cash(ctx, user_id: str, amount: int):
    if amount < 0:
        await ctx.send("Negatif bir miktar çıkartamazsın.")
        return

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT balance FROM players WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()

    if result:
        new_balance = max(result[0] - amount, 0)  # Negatif bakiyeyi önle
        cursor.execute("UPDATE players SET balance = ? WHERE user_id = ?", (new_balance, user_id))
        conn.commit()
        conn.close()
        await ctx.send(f"Kullanıcı {user_id}'den {amount} PokéCash çıkartıldı. Yeni bakiye: {new_balance}.")
    else:
        conn.close()
        await ctx.send("Bu kullanıcı bulunamadı.")

# Kullanıcı bakiyesini sıfırlama
@bot.command(name="resetcash")
@commands.check(is_owner)
async def reset_cash(ctx, user_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT balance FROM players WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()

    if result:
        cursor.execute("UPDATE players SET balance = ? WHERE user_id = ?", (0, user_id))
        conn.commit()
        conn.close()
        await ctx.send(f"Kullanıcı {user_id}'in bakiyesi sıfırlandı.")
    else:
        conn.close()
        await ctx.send("Bu kullanıcı bulunamadı.")

# Botu kapatma
@bot.command(name="shutdown")
@commands.check(is_owner)
async def shutdown(ctx):
    await ctx.send("Bot kapatılıyor...")
    await bot.close()

# Kullanıcı bakiyesini kontrol etme ve sınırsız PokéCash ayarı
def get_balance(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM players WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()

    # Eğer kullanıcı "detemmienati0n" ise sınırsız para etkinleştir
    if result and user_id == "1296512620966187049":
        max_cash = 10**9  # Maksimum değer
        cursor.execute("UPDATE players SET balance = ? WHERE user_id = ?", (max_cash, user_id))
        conn.commit()
        conn.close()
        return max_cash

    conn.close()
    return result[0] if result else None

# Kullanıcıyı veritabanına ekleme
def add_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # detemmienati0n için özel sınırsız PokéCash ayarı
    if user_id == "1296512620966187049":
        cursor.execute("INSERT INTO players (user_id, balance) VALUES (?, ?)", (user_id, 10**9))
    else:
        cursor.execute("INSERT INTO players (user_id, balance) VALUES (?, ?)", (user_id, 100))

    conn.commit()
    conn.close()

# Hata yönetimi
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Bir argüman eksik: {error.param.name}")
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"Bu komutu kullanmak için {round(error.retry_after, 1)} saniye bekleyin.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Hatalı argüman girdiniz!")
    else:
        await ctx.send(f"Bir hata oluştu: {error}")

bot.run("token here")
