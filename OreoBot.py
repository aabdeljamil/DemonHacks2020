import discord
import asyncio
import time

TOKEN = "NzY5Mzg3MjE5MTUyMjczNDE5.X5ORrw.1wrv7kv6bMSdhinwOb7BA_B949w"
GUILD = "OreoShunment's Demonhack Server"

client = discord.Client()

@client.event
async def on_message(message):
    pass

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(client.user, 'connected to guild ', guild.name, '#', guild.id)

client.run(TOKEN)
