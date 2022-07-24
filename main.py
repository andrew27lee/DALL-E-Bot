import os, re, base64, discord
from dotenv import load_dotenv
from discord.ext import commands
from requests import post

load_dotenv('.env')
bot = commands.Bot(command_prefix='!')


@bot.command()
async def generate(ctx, prompt):
    if not os.path.isdir('img'):
        os.makedirs('img')
    
    req = post(url = "https://bf.dallemini.ai/generate", json = {'prompt': prompt})
    images = re.search('\[(.*)\]', req.content.decode("utf-8") ).group(0)
    encodings = [e.replace("\\n", "") for e in re.findall('"([^"]*)"', images)]
    
    myfiles = []
    for i, encoded in enumerate(encodings):
        with open("img/image{}.png".format(i), "wb") as fh:
            fh.write(base64.b64decode(encoded))
        myfiles.append(discord.File("img/image{}.png".format(i)))
    
    await ctx.send(files = myfiles)


bot.run(os.getenv('TOKEN'))
