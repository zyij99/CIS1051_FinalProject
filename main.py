import discord
from discord.ext import commands
import os
import random
import requests
import uuid
import shutil

token = os.getenv('TOKEN')
bot = commands.Bot(command_prefix='!', case_insensitive = False)

d = {}   #stores everything
pet_dict = {} #stores pets
meme_dict = {} #stores memes

global c        #https://stackoverflow.com/questions/423379/using-global-variables-in-a-function
c = int(len(d)) #var for dictionary count

global p
p = int(len(pet_dict)) #var for pets img count

global me
me = int(len(meme_dict)) #var for memes img count

f = open('imgURLs.txt','r') #opens up textfile called imgURLs, 'r' means read mode
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

f = open('petsURLs.txt','r')
for line in f:
    if not line.strip():    
        continue
    else:
        p += 1
        if line not in pet_dict:
            if line.endswith('\n'):
                pet_dict[p] = line[:-1]
            else:
                pet_dict[p] = line
f.close()

f = open('memeURLs.txt','r')
for line in f:
    if not line.strip():    
        continue
    else:
        me += 1
        if line not in meme_dict:
            if line.endswith('\n'):
                meme_dict[me] = line[:-1]
            else:
                meme_dict[me] = line
f.close()

@bot.command()
async def randimg(msg):
    if len(d) == 0:
        await msg.send('There are no images saved yet')
    else:
        n = random.randint(1, len(d))
        await msg.send(file = discord.File(d[n]))
        await msg.send('This image is saved as image ' + str(n) + ' in the uncategorized directory')
        f = open('memeURLs.txt', 'r')
        for line in f:
            if line == d[n]:
                inv_meme = {value:key for key, value in meme_dict.items()} 
                memeNum = str(inv_meme[line])
                await msg.send('This image is saved as image ' + str(memeNum) + ' in the memes directory')
        f.close()
        f = open('petsURLs.txt', 'r')
        for line in f:
            if line == d[n]:
                inv_pets = {value:key for key, value in pet_dict.items()} 
                petNum = str(inv_pets[line])
                await msg.send('This image is saved as image ' + str(petNum) + ' in the pets directory')
        f.close()
        
@bot.command()
async def image(msg, num):
    if len(d) == 0:
        await msg.send('There are no images saved yet. Use the !s_img, !s_pet_img, or !s_memes command to save images to the directory.')
    if num == '0':
        try:
            msg.send(file = discord.File(d[num]))
        except KeyError:
            await msg.send('The image number ranges from 1 to ' + str(c))
    else:
        num = int(num)
        await msg.send(file = discord.File(d[num]))

@bot.command()
async def pet(msg, num):
    if len(pet_dict) == 0:
        await msg.send('There are no images saved yet. Use the !s_pet_img command to save images to the directory.')
    if num == '0':
        try:
            msg.send(file = discord.File(pet_dict[num]))
        except KeyError:
            await msg.send('The image number ranges from 1 to ' + str(p))
    else:
        num = int(num)
        await msg.send(file = discord.File(pet_dict[num]))

@bot.command()
async def memes(msg, num):
    if len(meme_dict) == 0:
        await msg.send('There are no images saved yet. Use the !s_memes command to save images to the directory.')
    if num == '0':
        try:
            msg.send(file = discord.File(meme_dict[num]))
        except KeyError:
            await msg.send('The image number ranges from 1 to ' + str(me))
    else:
        num = int(num)
        await msg.send(file = discord.File(meme_dict[num]))


#Source: https://www.youtube.com/watch?v=pgmUBOV3IIs
@bot.command()
async def s_img(msg):
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

@bot.command()
async def s_pet(msg):
    try:
        url = msg.message.attachments[0].url           
    except IndexError:
        print("Error: No attachments")
        await msg.send("No attachments detected!")
    else:
        if url[0:26] == "https://cdn.discordapp.com":   
            r = requests.get(url, stream=True)
            imgName = str(uuid.uuid4()) + '.jpg'      
            with open(imgName, 'wb') as out_file:
                print('Saving image: ' + imgName)
                shutil.copyfileobj(r.raw, out_file)     
                global c
                c += 1
                global p
                p += 1
                d[c] = imgName
                pet_dict[p] = imgName
                await msg.send('Saved Image' , file = discord.File(d[c]))
                inv_d = {value:key for key, value in d.items()} 
                imgNum = str(inv_d[imgName])
                inv_pet = {value:key for key, value in pet_dict.items()} 
                petNum = str(inv_pet[imgName])
                await msg.send('This is image ' + imgNum + ' of the unsorted directory and is image ' + petNum + ' of the pets directory.')
                with open('petsURLs.txt', 'a') as a_file:  
                    a_file.write('\n' + str(imgName))
                with open('imgURLs.txt', 'a') as a_file:  
                    a_file.write('\n' + str(imgName))    
                return c and p

@bot.command()
async def s_memes(msg):
    try:
        url = msg.message.attachments[0].url           
    except IndexError:
        print("Error: No attachments")
        await msg.send("No attachments detected!")
    else:
        if url[0:26] == "https://cdn.discordapp.com":   
            r = requests.get(url, stream=True)
            imgName = str(uuid.uuid4()) + '.jpg'      
            with open(imgName, 'wb') as out_file:
                print('Saving image: ' + imgName)
                shutil.copyfileobj(r.raw, out_file)     
                global c
                c += 1
                global me
                me += 1
                d[c] = imgName
                meme_dict[me] = imgName
                await msg.send('Saved Image' , file = discord.File(d[c]))
                inv_d = {value:key for key, value in d.items()} 
                imgNum = str(inv_d[imgName])
                inv_meme = {value:key for key, value in meme_dict.items()} 
                memeNum = str(inv_meme[imgName])
                await msg.send('This is image ' + imgNum + ' of the unsorted directory and is image ' + memeNum + ' of the memes directory.')
                with open('memeURLs.txt', 'a') as a_file:  
                    a_file.write('\n' + str(imgName))
                with open('imgURLs.txt', 'a') as a_file:  
                    a_file.write('\n' + str(imgName))    
                return c and me

@bot.event
async def on_ready():
    print('Bot is logged in as {0.user}'.format(bot))

bot.run(token)
