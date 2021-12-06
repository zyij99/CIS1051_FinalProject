import discord
from discord.ext import commands
import os
import random
import requests
import uuid
import shutil
import praw         

token = os.getenv('TOKEN')
bot = commands.Bot(command_prefix='!', case_insensitive = False)
bot.remove_command('help') #removes the default help command (replacing with my own)

#https://www.youtube.com/watch?v=0tn86pqnp0Q
channel = bot.get_channel(917228502468685824) #BOT IMG SAVE SPAM CHANNEL

#https://www.youtube.com/watch?v=Q5u6MDQAG7I Followed tutorial
#https://www.reddit.com/prefs/apps
reddit = praw.Reddit(client_id = 'khnzEfUFV1t6_6SS9O6a6w',
                    client_secret = '-HV-qPI1IhY8UKQnsNaZ9LeFuV7NPw',
                    username = os.getenv('usrname'),
                    password = os.getenv('passwrd'),
                    user_agent = 'usr_agent')
subreddit = reddit.subreddit('memes')

@bot.command()
async def r_memes(ctx):    
    subreddit = reddit.subreddit('memes')
    allsub = []

    hot = subreddit.hot(limit = 100)
    
    for submission in hot:
        allsub.append(submission)
    random_sub = random.choice(allsub)
    name = random_sub.title
    url = random_sub.url
    em = discord.Embed(title = name)

    em.set_image(url = url)
    await ctx.send(embed = em)

@bot.group(invoke_without_command=True)
#https://www.youtube.com/watch?v=ivXw9VO89jw & https://python.plainenglish.io/send-an-embed-with-a-discord-bot-in-python-61d34c711046
async def help(ctx):
    em = discord.Embed(title = 'Commands', description = 'Descriptions of commands and how to use them')
    em.add_field(name = 'image', value = 'Posts a saved image from the uncategorized directory corresponding to input num>0. \nFormat: !image <number>', inline=False)
    em.add_field(name = 'memes', value = 'Posts a saved image from the memes directory corresponding to input num>0. \nFormat: !memes <number>', inline=False)
    em.add_field(name = 'pet', value = 'Posts a saved image from the pet directory corresponding to input num>0. \nFormat: !pet <number>', inline=False)
    em.add_field(name = 'randimg', value = 'Posts a saved random image. \nFormat: !randimg', inline=False)
    em.add_field(name = 's_img', value = 'Saves an image into the uncategorized directory. \nFormat: !s_img <UPLOADED IMG/DISCORD IMAGE LINK>', inline=False)
    em.add_field(name = 's_memes', value = 'Saves an image into the memes and uncategorized directory. \nFormat: !s_memes <UPLOADED IMG/DISCORD IMAGE LINK>', inline=False)
    em.add_field(name = 's_pet', value = 'Saves an image into the pet and uncategorized directory. \nFormat: !s_pet <UPLOADED IMG/DISCORD IMAGE LINK>', inline=False)
    em.add_field(name = 'r_memes', value = 'Calls a random meme from the subreddit on Reddit.com that\'s in the hot 100 of posts. \nFormat: !r_memes', inline=False)

    await ctx.send(embed = em)

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
async def randimg(ctx):
    if len(d) == 0:
        await ctx.send('There are no images saved yet')
    else:
        n = random.randint(1, len(d))
        await ctx.send(file = discord.File(d[n]))
        await ctx.send('This image is saved as image ' + str(n) + ' in the uncategorized directory')
        f = open('memeURLs.txt', 'r')
        for line in f:
            if line == d[n]:
                inv_meme = {value:key for key, value in meme_dict.items()} 
                memeNum = str(inv_meme[line])
                await ctx.send('This image is saved as image ' + str(memeNum) + ' in the memes directory')
        f.close()
        f = open('petsURLs.txt', 'r')
        for line in f:
            if line == d[n]:
                inv_pets = {value:key for key, value in pet_dict.items()} 
                petNum = str(inv_pets[line])
                await ctx.send('This image is saved as image ' + str(petNum) + ' in the pets directory')
        f.close()
        
@bot.command()
async def image(ctx, num):
    if len(d) == 0:
        await ctx.send('There are no images saved yet. Use the !s_img, !s_pet, or !s_memes command to save images to the directory.')
    elif num == '0':
        try:
            ctx.send(file = discord.File(d[num]))
        except KeyError:
            await ctx.send('The image number currently ranges from 1 to ' + str(c))
    else:
        if int(num) > c:
            await ctx.send('The image can not be called. The range is currently 1 to ' + str(c))
        else:
            num = int(num)
            await ctx.send(file = discord.File(d[num]))

@bot.command()
async def pet(ctx, num):
    if len(pet_dict) == 0:
        await ctx.send('There are no images saved yet. Use the !s_pet command to save images to the directory.')
    elif num == '0':
        try:
            ctx.send(file = discord.File(pet_dict[num]))
        except KeyError:
            await ctx.send('The image number currently ranges from 1 to ' + str(p))
    else:
        if int(num) > p:
            await ctx.send('The image can not be called. The range is currently 1 to ' + str(p))
        else:
            num = int(num)
            await ctx.send(file = discord.File(pet_dict[num]))

@bot.command()
async def memes(ctx, num):
    if len(meme_dict) == 0:
        await ctx.send('There are no images saved yet. Use the !s_memes command to save images to the directory.')
    elif num == '0':
        try:
            ctx.send(file = discord.File(meme_dict[num]))
        except KeyError:
            await ctx.send('The image number currently ranges from 1 to ' + str(me))
    else:
        if int(num) > me:
            await ctx.send('The image can not be called. The range is currently 1 to ' + str(me))
        else:
            num = int(num)
            await ctx.send(file = discord.File(meme_dict[num]))

#Source: https://www.youtube.com/watch?v=pgmUBOV3IIs
@bot.command()
async def s_img(ctx):
    #!update in the comment when uploading an image to save the image as a .jpg
    #exception block to check for error

    try:
        url = ctx.message.attachments[0].url            # check for an image, call exception if none found
    except IndexError:
        print("Error: No attachments")
        await ctx.send("No attachments detected!")
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
                await channel.send('Saved Image' , file = discord.File(d[c]))      #posting to bot spam channel
                inv_d = {value:key for key, value in d.items()} #https://stackoverflow.com/questions/8023306/get-key-by-value-in-dictionary?page=2&tab=votes#tab-top
                imgNum = str(inv_d[imgName])
                await ctx.send('This is image ' + imgNum + 'of the uncategorized directory')
                await channel.send('This is image ' + imgNum + 'of the uncategorized directory')
                with open('imgURLs.txt', 'a') as a_file:    #https://www.kite.com/python/answers/how-to-append-a-newline-to-a-file-in-python
                    a_file.write('\n' + str(imgName))   # writes the image name into a txt document, which can be used to recall images loaded into the dictionary
                return c

@bot.command()
async def s_pet(ctx):
    try:
        url = ctx.message.attachments[0].url           
    except IndexError:
        print("Error: No attachments")
        await ctx.send("No attachments detected!")
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
                await channel.send('Saved Image' , file = discord.File(d[c]))
                inv_d = {value:key for key, value in d.items()} 
                imgNum = str(inv_d[imgName])
                inv_pet = {value:key for key, value in pet_dict.items()} 
                petNum = str(inv_pet[imgName])
                await ctx.send('Image is saved as image ' + imgNum + ' of the unsorted directory and is image ' + petNum + ' of the pets directory.')
                await channel.send('Image is saved as image ' + imgNum + ' of the unsorted directory and is image ' + petNum + ' of the pets directory.')
                with open('petsURLs.txt', 'a') as a_file:  
                    a_file.write('\n' + str(imgName))
                with open('imgURLs.txt', 'a') as a_file:  
                    a_file.write('\n' + str(imgName))    
                return c and p

@bot.command()
async def s_memes(ctx):
    try:
        url = ctx.message.attachments[0].url           
    except IndexError:
        print("Error: No attachments")
        await ctx.send("No attachments detected!")
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
                await channel.send('Saved Image' , file = discord.File(d[c]))
                inv_d = {value:key for key, value in d.items()} 
                imgNum = str(inv_d[imgName])
                inv_meme = {value:key for key, value in meme_dict.items()} 
                memeNum = str(inv_meme[imgName])
                await ctx.send('Image is saved as image ' + imgNum + ' of the unsorted directory and is image ' + memeNum + ' of the memes directory.')
                await channel.send('Image is saved as image ' + imgNum + ' of the unsorted directory and is image ' + memeNum + ' of the memes directory.')
                with open('memeURLs.txt', 'a') as a_file:  
                    a_file.write('\n' + str(imgName))
                with open('imgURLs.txt', 'a') as a_file:  
                    a_file.write('\n' + str(imgName))    
                return c and me

@bot.event
async def on_ready():
    print('Bot is logged in as {0.user}'.format(bot))

bot.run(token)
