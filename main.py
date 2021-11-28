import discord
from discord.ext import commands
import os
from decouple import config
import random
import requests
import uuid
import shutil

token = os.getenv('TOKEN')
bot = commands.Bot(command_prefix='!', case_insensitive = False)

d = {}
f = open('imgURLs.txt','r+') #opens up textfile called imgURLs, 'r' means read mode
global c        #https://stackoverflow.com/questions/423379/using-global-variables-in-a-function
c = int(len(d)) #c = 0

for line in f:
    if not line.strip():     #https://stackoverflow.com/questions/40647881/skipping-blank-lines-in-read-file-python
        continue
    else:
        c += 1
        if line not in d:
            if line.endswith('\n'):
                d[c] = line[:-1] #removes '/n'
            else:
                d[c] = line
f.close()

@bot.command()
async def randimg(msg):
    if len(d) == 0:
        await msg.send('There are no images saved yet')
    else:
        n = random.randint(1, len(d))
        await msg.send(file = discord.File(d[n]))
        await msg.send('This is saved image ' + str(n) + ' in the directory')

@bot.command()
async def image(msg, num):
    if len(d) == 0:
        await msg.send('There are no images saved yet. Use the !update command to save images to the directory.')
    if num == '0':
        try:
            msg.send(file = discord.File(d[num]))
        except KeyError:
            await msg.send('The image number ranges from 1 to ' + str(c))
    else:
        num = int(num)
        await msg.send(file = discord.File(d[num]))

#Source: https://www.youtube.com/watch?v=pgmUBOV3IIs
@bot.command()
async def update(msg):
    #!update in the comment when uploading an image to save the image as a .jpg
    #exception block to check for error
    try:
        url = msg.message.attachments[0].url            # check for an image, call exception if none found
    except IndexError:
        print("Error: No attachments")
        await msg.send("No attachments detected!")
    else:
        if url[0:26] == "https://cdn.discordapp.com":   # Checks to see if url is from discord
            r = requests.get(url, stream=True)
            imgName = str(uuid.uuid4()) + '.jpg'      # uuid creates random unique id to use for image names
            with open(imgName, 'wb') as out_file:
                print('Saving image: ' + imgName)
                shutil.copyfileobj(r.raw, out_file)     # save image (goes to project directory)
                global c
                c += 1
                d[c] = imgName
                await msg.send('Saved Image' , file = discord.File(d[c]))
                inv_d = {value:key for key, value in d.items()} #https://stackoverflow.com/questions/8023306/get-key-by-value-in-dictionary?page=2&tab=votes#tab-top
                imgNum = str(inv_d[imgName])
                await msg.send('This is image ' + imgNum)
                with open('imgURLs.txt', 'a') as a_file:    #https://www.kite.com/python/answers/how-to-append-a-newline-to-a-file-in-python
                    a_file.write('\n' + str(imgName))   # writes the image name into a txt document, which can be used to recall images loaded into the dictionary

                return c

@bot.event
async def on_ready():
    print('Bot is logged in as {0.user}'.format(bot))

bot.run(token)