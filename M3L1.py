from flask import Flask
import random

app = Flask(__name__)

@app.route("/")
def randomAU_link():
    return f'<a href="/randomAU"> Random AU </a>'

@app.route("/randomAU")
def hello_world():
    au_list=("SwapTale", "Swapfell", "StorySwap", "AfterTale", "XTale", "UnderSwap", "FellTale", "HorrorTale", "ErrorTale", "InkTale", "MysteryTale", "Outertale", "Glitchtale", "DoomTale", "CrossTale", "Underfell", "DustTale", "Underfresh", "Reapertale", "Epictale", "NightmareTale")
    return f'<h1>{random.choice(au_list)}</h1>'

app.run(debug=True)
