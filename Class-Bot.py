import discord
from discord.ext import commands
import asyncio
import time
import re

TOKEN = "NzY5Mzg3MTk3NDEyODAyNjAw.X5ORqg.o9o_TZ4Cs8TsRkurYJ7PeRBvkYE" #delete when pushing
GUILD = "OreoShunment's Demonhack Server"


client = discord.Client(intents = discord.Intents.all())
currentGuild = None

kickList = {}
lastMsg = {}
cussVariants = ['fuck', 'shit', 'bitch', 'ass', 'cunt', 'cock', 'dick', 'damn', 'retard']#can add other cuss words

isLecture = False
prefix = "!"

mutelist = {}
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
	

async def MuteAll(flag): # flag is True to mute, False to unmute
	global currentGuild
	if currentGuild == None:
		print("Not part of a guild")
		return
	for memb in currentGuild.members:
		if any(role.name.lower() == "student" for role in memb.roles) or len(memb.roles) == 1:
			if flag:
				mutelist[memb] = 0
				await memb.edit(mute = True)
			else:
				mutelist.pop(memb)
				await memb.edit(mute = False)
				
async def HandleMute(member, flag, channel): # flag is True to mute, False to unmute
	global currentGuild
	if currentGuild == None:
		print("Not part of a guild")
		return
	if member in mutelist.keys():
		if flag:
			if mutelist[member] == 0:
				mutelist[member] = 1
				await member.edit(mute = False)
				await channel.send("User **" + member.nick + " **has raised their hand")
			else:
				await channel.send("You already have your hand raised", delete_after = 10.0)
		else:
			if mutelist[member] == 1:
				mutelist[member] = 0
				await member.edit(mute = True)
				await channel.send("User **" + member.nick + " **has lowered their hand")
			else:
				await channel.send("You already have your hand lowered", delete_after = 10.0)
	else:
		await channel.send("You are not a part of a class session", delete_after = 10.0)
		
async def TextMute(member):
	global currentGuild
	if currentGuild == None:
		print("Not part of a guild")
		return
	if any(role.name.lower() == "muted" for role in currentGuild.roles):
		await member.add_roles(discord.utils.get(currentGuild.roles, name = "muted"))
	else: # role "muted" does not exist in the server
		pos = discord.utils.get(currentGuild.roles, name = "student").position + 1
		perm = discord.Permissions(send_messages = False, read_messages = True, connect = True, speak = True, use_voice_activation = True, read_message_history = True)
		Nrole = await currentGuild.create_role(name = "muted", permissions = perm)
		await Nrole.edit(position = pos)
		for channel in currentGuild.channels:
			if channel.type == discord.ChannelType.text:
				await channel.set_permissions(Nrole, send_messages = False)
		await member.add_roles(Nrole)
		


@client.event
async def on_ready():
	for guild in client.guilds:
		if guild.name == GUILD:
			global currentGuild
			currentGuild = guild
			break

	print(client.user, 'connected to guild ', guild.name, '#', guild.id)
	isLecture = False


@client.event
async def on_message(message):
	if message.author == client.user: #don't want bot replying to itself
		return
		
	possCommand = (message.content.lower()).split(None, 1)
	
	if possCommand[0] == (prefix + "lecture"): # command is !lecture
		if not (any(role.name.lower() == "staff" for role in message.author.roles)) or len(message.author.roles) == 1:
			await message.channel.send("You do not have permission to use the command '!lecture'", delete_after = 10.0)
			return
		if len(possCommand) <= 1:
			await message.channel.send("Incorrect usage of '!lecture'\nproper usage is '!lecture (on/off)'", delete_after = 20.0)
			return
		global isLecture
		if possCommand[1] == "on":
			if not isLecture:
				classlist = []
				mutelist = {}
				isLecture = True
				await MuteAll(True)
				await message.channel.send("Lecture is now in session", delete_after = 10.0)
			else:
				await message.channel.send("Lecture is already active", delete_after = 10.0)
		elif possCommand[1] == "off":
			if isLecture:
				isLecture = False
				await MuteAll(False)
				await message.channel.send("Lecture has concluded", delete_after = 10.0)
			else:
				await message.channel.send("Lecture is already inactive", delete_after = 10.0)
		else:
			await message.channel.send("Incorrect usage of '!lecture'\n\tproper usage is '!lecture (on/off)'", delete_after = 20.0)
		return
	
	if possCommand[0] == (prefix + "assign"): # command is !assign
		if not (any(role.name.lower() == "staff" for role in message.author.roles)) or len(message.author.roles) == 1:
			await message.channel.send("You do not have permission to use the command '!assign'", delete_after = 10.0)
			return
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
		
	if possCommand[0] == (prefix + "hand"): # command is !hand
		if any(role.name.lower() == "student" for role in message.author.roles) or len(message.author.roles) == 1:
			if len(possCommand) <= 1:
				await message.channel.send("Incorrect usage of '!hand'\nproper usage is '!hand (raise/lower)'", delete_after = 20.0)
				return
			if possCommand[1] == "raise":
				await HandleMute(message.author, True, message.channel)
			elif possCommand[1] == "lower":
				await HandleMute(message.author, False, message.channel)
			else:
				await message.channel.send("Incorrect usage of '!hand'\nproper usage is '!hand (raise/lower)'", delete_after = 20.0)
		else:
			await message.channel.send("'!hand' is meant for students only", delete_after = 10.0)
		return
		
	if possCommand[0] == (prefix + "checkin"):
		if any(role.name.lower() == 'student' for role in message.author.roles):
			if isLecture:
				if message.author.nick not in classlist:
					classlist.append(message.author.nick)
					await message.channel.send("Checked in.", delete_after=10.0)
				else:
					await message.channel.send("Already checked in", delete_after=10.0)
			else:
				await message.channel.send("Lecture has not started.")
		else:
			await message.channel.send("!checkin is for students only.")
		return

	if possCommand[0] == (prefix + "attendance"):
		if any(role.name.lower() == 'staff' for role in message.author.roles):
			if not isLecture:
				attendancelist = ""
				for student in classlist:
					print(student)
					attendancelist = attendancelist + student + "\n"
				await message.channel.send(attendancelist + "End of list.")
			else:
				await message.channel.send("Lecture has not ended.")
		else:
			await message.channel.send("!attendance is for instructors only.")
		return
	
	if any(role.name.lower() == "student" for role in message.author.roles) or len(message.author.roles) == 1:
		if message.author in lastMsg and message.content.lower() == lastMsg[message.author]: # Spam filter
			msg = str(message.author) + ", don't spam!"
			await message.channel.send(msg, delete_after = 10.0)
			await message.delete()
			return
		else:
			lastMsg[message.author] = message.content.lower()

		if any(re.search(r"\b" + re.escape(variant) + r"\b", message.content.lower()) for variant in cussVariants): # Test for swearing
			if message.author in kickList:
				if kickList[message.author] >= 2:
					msg = str(message.author) + ' has been muted for cussing too many times.'
					await message.channel.send(msg)
					await TextMute(message.author)
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
