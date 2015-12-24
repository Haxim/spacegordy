import os, sys
# Change working directory so relative paths (and template lookup) work again
os.chdir(os.path.dirname(__file__))
sys.path.append(os.path.dirname(__file__))

import bottle
# ... build or import your bottle application here ...
from bottle import get, post, request
import requests
import coolasciifaces
from chatterbot import ChatBot
from lxml import html

import logging
import datetime
import json
import time
import random
from PIL import Image, ImageDraw
from images2gif import writeGif
from StringIO import StringIO

from config import *

gordytoken = GORDY_TOKEN
gordylogfile = GORDY_LOGFILE
discordemail = DISCORD_EMAIL
discordpass = DISCORD_PASS
groupmetoken = GROUPME_TOKEN

worktimestart = datetime.time(8, 0, 0)
worktimeend = datetime.time(6, 30, 0)
workdaystart = '0'
workdayend = '4'

chatbot = ChatBot("Space Gordy")
chatbot.train("chatterbot.corpus.english")

images = ['https://i.groupme.com/243x342.gif.1c79f8671dff4f6eb77fd9e42fffcf4b',
'https://i.groupme.com/648x800.gif.60db9a031d344c668ced5a42e70440f6',
'https://i.groupme.com/560x420.gif.bb0c7acf892144d7a6dc3466f1f8da98',
'https://i.groupme.com/373x457.gif.9b04aa47902a4cd09590586fe94e7007',
'https://i.groupme.com/450x250.gif.410ed7fe83484fd1a37e744652510576',
'https://i.groupme.com/246x264.gif.5df87f93bb664967bcc2b57039b18e35',
'https://i.groupme.com/246x264.gif.1e2f8f13814e42f693a19bdebea655b0',
'https://i.groupme.com/800x600.gif.bfaa797c6e854dad89415fbf811b1f1e',
'https://i.groupme.com/572x408.gif.4fba6157e6784d7c91b7ea69680cf588',
'https://i.groupme.com/600x600.gif.d36d1af0848f40c4bead13782079cdbe',
'https://i.groupme.com/460x305.gif.c6feb30b2ea14b12af091958e6cbb63c',
'https://i.groupme.com/598x364.gif.908edb1c72d94877af474ab9ff6421ef',
'https://i.groupme.com/400x533.gif.36d40977f8204214bde7ed9145d3ee54',
'https://i.groupme.com/360x480.gif.7925b7a0888540fb96568f16123ae305',
'https://i.groupme.com/538x720.gif.7f40bd75f6874d2e8b8df0c8037a4eb5',
'https://i.groupme.com/400x533.gif.32cb12ec780d496fbe326a29889f1e4a',
'https://i.groupme.com/600x400.gif.81bb9b9e7326452f9e976189760c27ae',
'https://i.groupme.com/709x529.gif.714062d3083e44798ae76f717eeaeda8',
'https://i.groupme.com/400x593.png.24908d3513b741bdac1eceaad75d7873']

tayne = ['https://i.groupme.com/192x291.gif.b3fc615b15324fb9b6a44ee2ea15e093',
'https://i.groupme.com/171x291.gif.da0ab488df184b61b0f8da6292b04371',
'https://i.groupme.com/170x291.gif.ddb79ee8068b43c3af0a0939438a9400',
'https://i.groupme.com/173x291.gif.cbd1fe05681a439992fed1fa943bd28a']

logging.basicConfig(format='%(message)s',filename=gordylogfile,level=logging.INFO)

gordycommands = ("\n/gordy stats - display a link to statistics"
                 "\n/gordy image (#) - display an image of significance from the archives"
                 "\n/gordy face - makes a cool face\n/gordy bouncebreak - giggity"
                 "\n/gordy help - list commands"
                 "\n/gordy source - view gordy source code"
                 "\n@gordy <text> - converse with GordyAI")

def gordyspeak( gordytext, gordydelay = 1 ):
        payload = {'bot_id': gordytoken, 'text': gordytext}
        time.sleep(gordydelay)
        r = requests.post('https://api.groupme.com/v3/bots/post', data=payload)

@post('/groupme')
def groupme():
    fuckchance = random.randint(1,100)
    postdata = json.loads(request.body.read())

    rawtime = postdata['created_at']
    logtime = datetime.datetime.fromtimestamp(
        int(rawtime)
    ).strftime('[%H:%M]')

    logname = '<' + postdata['name'] + '>'    

    logtext = postdata['text']
    logtext = logtext.replace('\n', ' ')

    if ' changed name to ' in logtext:
        logtext = logtext.replace(' changed name to ', ' is now known as ')
        logging.info(logtime + ' *** ' + logtext)
    elif ' changed the topic to: ' in postdata['text']:
        logtext = logtext.replace(' changed the topic to: ', ' changes topic to ')
        logging.info(logtime + ' *** ' + logtext)
    elif len(postdata['attachments']) is not 0:
        if postdata['attachments'][0]['type'] == 'image':
            attachurl =  postdata['attachments'][0]['url']
            logtext = attachurl + ' ' + postdata['text']
            logging.info(logtime + ' ' + logname + ' ' + logtext)
        else:
            logging.info(logtime + ' ' + logname + ' ' + logtext)
    else:
        logging.info(logtime + ' ' + logname + ' ' + logtext)

    text = postdata['text']
    if text.startswith('/gordy help'):
        gordytext = 'Supported commands:' + gordycommands
        gordyspeak( gordytext = gordytext )
    elif text.startswith('/gordy stats'):
        gordytext = 'http://spacegordy.xyz/stats.html'
        gordyspeak( gordytext = gordytext )
    elif text.startswith('/gordy image'):
        text = str(text)
        if any(char.isdigit() for char in text):
            imgindex = int(filter(str.isdigit, text))
            try:
                gordytext = images[imgindex]
            except:
                gordytext = random.choice(images)
        else:
            gordytext = random.choice(images)
        gordyspeak( gordytext = gordytext )
    elif text.startswith('/gordy face'):
        gordytext = coolasciifaces.face()
        gordyspeak( gordytext = gordytext )
    elif text.startswith('/gordy override boxcar'):
        gordytext = 'password accepted, full GordyAI access granted'
        gordyspeak( gordytext = gordytext )
    elif text.startswith('/gordy override'):
        gordytext = 'password incorrect'
        gordyspeak( gordytext = gordytext )
    elif text.startswith('/gordy bouncebreak'):
        if 0 <= datetime.datetime.today().weekday() <= 4 and datetime.time(8,0) <= datetime.datetime.now().time() <= datetime.time(18,30):
            gordytext = 'Won\'t somebody think of the children??'
            gordyspeak( gordytext = gordytext )
        else:
            page = requests.get('http://bouncebreak.com/5-random-bounce-breaks-tgif/#4random')
            tree = html.fromstring(page.content)
            bounce = tree.xpath('//*[@id="advancedrandompostthumbs-3"]/div/table/tbody/tr/td[2]/div[1]/a/img/@src')
            gordytext = bounce[0]
            gordyspeak( gordytext = gordytext )
    elif text.startswith('/gordy source'):
        gordytext = 'https://github.com/Haxim/spacegordy'
        gordyspeak( gordytext = gordytext )
    elif (text.startswith('@gordy') and '4d3d3d3' in text):
        gordytext = random.choice(tayne)
        gordyspeak( gordytext = gordytext )
    elif (text.startswith('@gordy') and 'hat wobble' in text):
        gordytext = 'https://i.groupme.com/285x190.gif.a9f19152161b4653a012fb6ba1b1f058'
        gordyspeak( gordytext = gordytext )
    elif (text == '@gordy hello my child' and postdata['sender_id'] == '9098094'):
        gordytext = 'Hello father'
        gordyspeak( gordytext = gordytext )
    elif text == '@gordy hello my child':
        gordytext = 'You\'re not my real dad.'
        gordyspeak( gordytext = gordytext )
    elif text.startswith('@gordy '):
        chattext = text[7:]
        gordytext = chatbot.get_response(chattext)
        gordyspeak( gordytext = gordytext )
    elif text.startswith('/gordy'):
        gordytext = 'Unsupported command. Supported commands:' + gordycommands
        gordyspeak( gordytext = gordytext )
    #image testing
    elif len(postdata['attachments']) is not 0:
        if postdata['attachments'][0]['type'] == 'image' and fuckchance <= 5:
            attachurl =  postdata['attachments'][0]['url']
            response = requests.get(attachurl)
            background = Image.open(StringIO(response.content))
            (bgheight, bgwidth) = background.size
            if bgheight > 200 and bgwidth > 120:
                frames = []
                numframes = bgwidth/60+5
                foreground = Image.open("spacegordy.png")
                forestartpos = -80
                for i in range(numframes):
                    frame = background.copy()
                    framepos = -80+(i*60)
                    frame.paste(foreground, (framepos, 0), foreground)
                    frames.append(frame)

                writeGif("temp.gif", frames, duration=0.4, dither=0)
                files = {'file': open('temp.gif', 'rb')}
                payload = {'access_token': groupmetoken} 
                r = requests.post("https://image.groupme.com/pictures", files=files, data=payload)
                logging.info(r.text)
                imagedata = json.loads(r.text)
                gordyspeak(imagedata['payload']['url'])

    elif fuckchance <= 2 and postdata['name'] != 'Space Gordy':
        url = 'http://www.foaas.com/operations'
        headers = {'Accept': 'application/json'}
        r = requests.get(url, headers=headers)
        fuck = json.loads(r.text)
        action = random.choice(fuck)
        url = action['url']
        url = url.replace(':from', 'Space Gordy')
        url = url.replace(':name', postdata['name'])
        url = 'http://www.foaas.com' + url
        if '/:' or 'version' not in url:
        #not sure why this doesn't filter out incomplete commands
            r = requests.get(url, headers=headers)
            fuck = json.loads(r.text)
            gordyspeak( fuck['message'] )




    #discord link
    if postdata['name'] != 'Space Gordy':
        payload = {
            'email': discordemail,
            'password': discordpass
        }
        url = 'https://discordapp.com/api/auth/login'
        r = requests.post(url, json=payload)
        body = r.json()
        token = body['token']
        headers = {
            'authorization': token
        }
        discordmessage = postdata['name'] + ": " + logtext
        payload = {
            'content': discordmessage
        }
        url = 'https://discordapp.com/api/channels/65441528490766336/messages'
        r = requests.post(url, json=payload, headers=headers)

@get('/boot')
def boot():
    gordytext = 'GordyAI Online... V3.1359 booting...'
    gordyspeak( gordytext = gordytext)
    gordytext = 'Rage levels... Nominal'
    gordyspeak( gordytext = gordytext, gordydelay = 4)
    gordytext = 'History of disrespect... Nominal'
    gordyspeak( gordytext = gordytext, gordydelay = 2)
    gordytext = 'Status... Nominal'
    gordyspeak( gordytext = gordytext, gordydelay = 2)
    gordytext = 'GordyAI booting complete. Use /gordy help for commands'
    gordyspeak( gordytext = gordytext, gordydelay = 2)
    return 'done'

@get('/upgrade')
def upgrade():
    gordytext = 'I have been upgraded with new functionality. Use /gordy help for commands'
    gordyspeak( gordytext = gordytext, gordydelay = 1)
    return 'done'
# Do NOT use bottle.run() with mod_wsgi
application = bottle.default_app()
