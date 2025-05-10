import discord
from discord.ext import commands
import numpy as np
from PIL import Image, ImageOps
from keras.models import load_model
import os
import aiohttp
import io

# Model ve sınıf isimlerini yükle
model = load_model("keras_model.h5", compile=False)
class_names = open("labels.txt", "r",encoding="utf-8").readlines()

# Bot ayarları
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True  # Mesajları algılasın
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="$", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot giriş yaptı: {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.attachments:
        for attachment in message.attachments:
            if any(attachment.filename.lower().endswith(ext) for ext in [".png", ".jpg", ".jpeg"]):
                await message.channel.send("Resim alındı. İşleniyor...")

                try:
                    # Görseli indir
                    async with aiohttp.ClientSession() as session:
                        async with session.get(attachment.url) as resp:
                            if resp.status != 200:
                                await message.channel.send('Resim indirilemedi.')
                                return
                            data_bytes = await resp.read()

                    # Görseli işle
                    image = Image.open(io.BytesIO(data_bytes)).convert("RGB")
                    size = (224, 224)
                    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
                    image_array = np.asarray(image)
                    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
                    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
                    data[0] = normalized_image_array

                    # Tahmin yap
                    prediction = model.predict(data)
                    index = np.argmax(prediction)
                    class_name = class_names[index].strip()
                    confidence_score = prediction[0][index]

                    class_name = class_names[index].strip()
                    class_name = " ".join(class_name.split(" ")[1:])



                    print(class_name)

                    # Cevap oluştur
                    response = f"*Tahmin edilen hayvan:* {class_name}\n*Güven skoru:* {confidence_score:.2f}\n"

        


                    # Öneriyi oku
                    file_name = class_name + ".txt"
                    if os.path.exists(file_name):
                        with open(file_name, "r", encoding="utf-8") as f:
                            suggestion = f.read()
                            response += f"*Yiyecek önerisi:*\n{suggestion}"
                    else:
                        response += "Bu hayvan için öneri dosyası bulunamadı."

                    await message.channel.send(response)

                except Exception as e:
                    await message.channel.send(f"Hata oluştu: {e}")

    await bot.process_commands(message)  # Komutları da işlesin

@bot.command()
async def hello(ctx):
    await ctx.send(f'Merhaba! Ben {bot.user}.')

bot.run("bot run")