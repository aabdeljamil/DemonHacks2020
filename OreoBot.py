import discord
from discord.ext import commands
import asyncio
import time

TOKEN = "" #delete when pushing
GUILD = "OreoShunment's Demonhack Server"

client = discord.Client()

kickList = {}
lastMsg = {}
cussVariants = ['fuck', 'shit', 'bitch', 'ass']#can add other cuss words

@client.event
async def on_message(message):
	if message.author == client.user: #don't want bot replying to itself
		return
	
	if message.author in lastMsg and message.content.lower() == lastMsg[message.author]: # Spam filter
		if message.author in kickList:
			if kickList[message.author] >= 2:
				msg = str(message.author) + " has been kicked from this server for spamming."
				await message.channel.send(msg, delete_after = 10.0)
				#await message.author.kick()
				kickList.pop(message.author)
			else:
				kickList[message.author] = kickList[message.author] + 1
				msg = str(message.author) + ", don't spam! This is your " + ("first" if kickList[message.author] == 1 else "second") + " warning."
				await message.channel.send(msg, delete_after = 10.0)
		else:
			kickList[message.author] = 1
			msg = str(message.author) + ", don't spam! This is your first warning."
			await message.channel.send(msg, delete_after = 10.0)
		await message.delete()
	else:
		lastMsg[message.author] = message.content.lower()
        
	if any(variant in message.content.lower() for variant in cussVariants): # Test for swearing
		if len(message.author.roles) == 1: #change to check
			if message.author in kickList:
				if kickList[message.author] >= 2:
					msg = str(message.author) + ' has been kicked from this server for cussing too many times.'
					await message.channel.send(msg, delete_after = 10.0)
					#await message.author.kick()
					kickList.pop(message.author) #if user is added back, their chance gets reset
				else:
					kickList[message.author] = kickList[message.author] + 1
					msg = str(message.author) + ", don't cuss! This is your " + ("first" if kickList[message.author] == 1 else "second") + " warning."
					await message.channel.send(msg, delete_after = 10.0)
			else:
				kickList[message.author] = 1
				msg = str(message.author) + ", don't cuss! This is your first warning."
				await message.channel.send(msg, delete_after = 10.0)
		await message.delete()

@client.event
async def on_ready():
	for guild in client.guilds:
		if guild.name == GUILD:
			break

	print(client.user, 'connected to guild ', guild.name, '#', guild.id)

client.run(TOKEN)
