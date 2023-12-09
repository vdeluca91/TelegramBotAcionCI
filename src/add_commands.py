"""Add commands handler"""
from telegram import BotCommand
from telegram.ext import Application

import requests,json

from typing import Final
from src.lib.config import *
TOKEN: Final = BOT_CONFIG['__TOKEN']


cmd = [
        {"command":"start","description":"avvia il bot"},
        {"command":"prenota","description":"prenota un tavolo"},
        {"command":"le_mie_prenotazioni","description":"visualizza/disdici prenotazione"},
        {"command":"menu","description":"visualizza il menu"},
        {"command":"eventi","description":"visualizza gli special nights events"},
        {"command":"info","description":"visualizza le informazioni del ristorante"}
    ]
url = "https://api.telegram.org/bot"+TOKEN+"/setMyCommands?commands="+str(json.dumps(cmd))
req = requests.get(url)


async def add_commands(app: Application) -> None:

    cmd = [
        ("start","avvia il bot"),
        ("prenota","prenota un tavolo"),
        ("le_mie_prenotazioni", "visualizza/disdici prenotazione"),
        ("menu","visualizza il menu"),
        ("eventi", "visualizza gli special nights events"),
        ("info", "visualizza le informazioni del ristorante")
        ]

   
    # Setta l'immagine del bot
    # image_path = "src\\media\\logo.png"  
    # with open(image_path, 'rb') as image_file:
    #     app.bot.setBotPic(InputFile(image_file))