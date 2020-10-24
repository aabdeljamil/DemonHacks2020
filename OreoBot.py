import discord
from discord.ext import commands
import asyncio
import time

TOKEN = "NzY5Mzg3MjE5MTUyMjczNDE5.X5ORrw.-qJUdsx3CconFNSxK5qLcob9a0o" #delete when pushing
GUILD = "OreoShunment's Demonhack Server"

client = discord.Client()

kickList = {}
lastMsg = {}
cussVariants = ['fuck', 'shit', 'bitch', 'ass', 'cunt', 'cock', 'dick', 'damn', 'retard']#can add other cuss words

isLecture = False
prefix = "!"

classlist = []

DAYINSECONDS = 86400.0
WAITTIME = 5.0 # SET TO DAYINSECONDS FOR PROPER BEHAVIOR OF REMINDING EVERY DAY

async def assignment(numDays, channel, assignmentText):
	if numDays <= 0.0:
		return
	n = numDays 
	while n > 0.0:
		await channel.send("assignment **" + assignmentText + " **will be due in " + str(round(n,1)) + " days")
		waittime = (WAITTIME if WAITTIME <= WAITTIME * n else WAITTIME * n)
		await asyncio.sleep(waittime)
		n = n - 1
	await channel.send("assignment **" + assignmentText + " **is now ***DUE***")


@client.event
async def on_ready():
	for guild in client.guilds:
		if guild.name == GUILD:
			break

	print(client.user, 'connected to guild ', guild.name, '#', guild.id)
	isLecture = False


@client.event
async def on_message(message):
	if message.author == client.user: #don't want bot replying to itself
		return
		
	possCommand = (message.content.lower()).split(None, 1)
	if possCommand[0] == (prefix + "lecture"): # command is !lecture
		if len(possCommand) <= 1:
			await message.channel.send("Incorrect usage of '!lecture'\nproper usage is '!lecture (on/off)'", delete_after = 20.0)
			return
		
		global isLecture
		if possCommand[1] == "on":
			if not isLecture:
				isLecture = True
				await message.channel.send("Lecture is now in session", delete_after = 10.0)
			else:
				await message.channel.send("Lecture is already active", delete_after = 10.0)
		elif possCommand[1] == "off":
			if isLecture:
				isLecture = False
				await message.channel.send("Lecture has concluded", delete_after = 10.0)
			else:
				await message.channel.send("Lecture is already inactive", delete_after = 10.0)
		else:
			await message.channel.send("Incorrect usage of '!lecture'\n\tproper usage is '!lecture (on/off)'", delete_after = 20.0)
		return
	if possCommand[0] == (prefix + "assign"): # command is !assign
		if len(possCommand) <= 1:
			await message.channel.send("Incorrect usage of '!assign'\nproper usage is '!assign <number of days> <assignment name>'", delete_after = 20.0)
			return
		cmdSplit = possCommand[1].split(None,1)
		if len(cmdSplit) <= 1:
			await message.channel.send("Incorrect usage of '!assign'\nproper usage is '!assign <number of days> <assignment name>'", delete_after = 20.0)
			return
		x = 0.0
		try:
			x = float(cmdSplit[0])
		except:
			await message.channel.send("Incorrect usage of '!assign'\nproper usage is '!assign <number of days> <assignment name>'", delete_after = 20.0)
			return
		await message.channel.send("Set assignment **" + cmdSplit[1] + " **to be due in " + str(x) + " days", delete_after = 20.0)
		loop = asyncio.get_event_loop()
		loop.create_task(assignment(x, message.channel, cmdSplit[1]))
		return
	
	if any(role.name.lower() == "student" for role in message.author.roles) or len(message.author.roles) == 1:
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
			return
		else:
			lastMsg[message.author] = message.content.lower()
			
		if any(variant in message.content.lower() for variant in cussVariants): # Test for swearing
			if message.author in kickList:
				if kickList[message.author] >= 2:
					msg = str(message.author) + ' has been kicked from this server for cussing too many times.'
					await message.channel.send(msg, delete_after = 10.0)
					#await message.author.kick()
					kickList.pop(message.author) # if user is added back, their chance gets reset
				else:
					kickList[message.author] = kickList[message.author] + 1
					msg = str(message.author) + ", don't cuss! This is your " + ("first" if kickList[message.author] == 1 else "second") + " warning."
					await message.channel.send(msg, delete_after = 10.0)
			else:
				kickList[message.author] = 1
				msg = str(message.author) + ", don't cuss! This is your first warning."
				await message.channel.send(msg, delete_after = 10.0)
		await message.delete()
		return
			
			

client.run(TOKEN)
