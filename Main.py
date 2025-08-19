import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging
import os
import random
import requests
import json
import asyncio

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

#when a message is sent outside of bot
async def channel_warner(ctx):
    if ctx.channel.name != "bot":
        file = discord.File(fp="C:\\Users\\Main\\Desktop\\Serious\\Automation\\Discord\\Images\\Burro.png", filename="Burro.png")
        await ctx.send(f"Utilice el canal bot para comandos {ctx.author.name}", file=file)
        return True
#when you need a little spice in the voice chat
async def text_to_speech(text):
    url="https://ttsmp3.com/makemp3_new.php"
    request = requests.post(url=url, data={"msg":text,"lang":"Miguel","source":"testing"})
    if request.status_code==200:
        link=json.loads(request.text)["URL"]
        dowload_response = requests.get(link, stream=True)
        output_file = json.loads(request.text)["MP3"]
        if dowload_response.status_code == 200:
            with open(output_file, 'wb') as f:
                for chunk in dowload_response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print("Download complete!")
        return os.path.abspath(output_file)


# When we login in
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

#when we receive a message
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    print(f"Message received: {message.content}")
    await bot.process_commands(message)

#Hello User
@bot.command()
async def hola(ctx):
    if(await channel_warner(ctx)): return
    print(f"Sending Hello to {ctx.author.name}")
    await ctx.send(f'Hola @{ctx.author.name}!')

#Random peripecia
@bot.command()
async def lorenzo(ctx):
    if(await channel_warner(ctx)): return

    channel = discord.utils.get(ctx.guild.text_channels, name="peripecias-do-lorenzo")
    messages = [msg async for msg in channel.history(limit=200)]
    chosen = random.choice(messages)
    print(f"Message chosen: {chosen.content}")
    final_format = chosen.content.replace('\r', '....\r').replace('\n', '.....\n')
    audio_file= await text_to_speech(f"La peripecia de ahora es....' {final_format} '....palabras muy sabias")

    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        voice_client = ctx.voice_client
        if voice_client and voice_client.is_connected():
            # FFmpegPCMAudio uses ffmpeg to process the file
            source = discord.FFmpegPCMAudio(audio_file)
            voice_client.play(source)
            while voice_client.is_playing():
                await asyncio.sleep(1)
        await ctx.voice_client.disconnect()
    os.remove(audio_file)
    await ctx.send(f"La peripecia de ahora es....' {chosen.content} '....palabras muy sabias")

'''
@bot.command()
async def createchannel(ctx, name: str):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=name)

    print(f"Command received: {ctx.message.content}")  # debug
    print(f"Channel name to create: {name}")

    if not existing_channel:
        await guild.create_text_channel(name)
        await ctx.send(f'✅ Canal creado: {name}')
    else:
        await ctx.send(f'⚠️ Um canal con este nombre ya existe: "{name}"!')
'''



bot.run(token=token, log_handler=handler, log_level=logging.DEBUG)
