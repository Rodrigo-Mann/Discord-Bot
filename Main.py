import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging
import os
import random
import asyncio
import utils.text_to_audio_handling as bot_voice

VOICE="Miguel"

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
    response_voice_instance = bot_voice.text_to_audio(file_id=chosen.id, audio_lang=VOICE)
    print("Voice object created.")
    if ctx.author.voice:

        channel = ctx.author.voice.channel
        response_voice_instance.text_to_speech_request(f"La peripecia de ahora es....' {final_format} '....palabras muy sabias")
        await channel.connect()
        voice_client = ctx.voice_client
        if voice_client and voice_client.is_connected():
            # FFmpegPCMAudio uses ffmpeg to process the file
            source = discord.FFmpegPCMAudio(response_voice_instance.path)
            voice_client.play(source)
            while voice_client.is_playing():
                await asyncio.sleep(1)
        await ctx.voice_client.disconnect()

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
