import discord
import requests
import time
from config import *

gordytoken = GORDY_TOKEN
gordylogfile = GORDY_LOGFILE
discordemail = DISCORD_EMAIL
discordpass = DISCORD_PASS

def gordyspeak( gordytext, gordydelay = 1 ):
        payload = {'bot_id': gordytoken, 'text': gordytext}
        time.sleep(gordydelay)
        r = requests.post('https://api.groupme.com/v3/bots/post', data=payload)

client = discord.Client()
client.login(discordemail, discordpass)

@client.event
def on_ready():
    print('Connected!')
    print('Username: ' + client.user.name)
    print('ID: ' + client.user.id)

@client.event
def on_message(message):
    if message.author.id != client.user.id:
        #client.send_message(message.channel, message.content + message.author)
        discordmessage = str(message.author) + ": " + str(message.content)
        gordyspeak( gordytext = discordmessage )

client.run()
