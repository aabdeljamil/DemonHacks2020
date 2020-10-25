import discord
import asyncio
import time
import random

TOKEN = 'NzY5Mzg0MDg1MTM4ODMzNDM5.X5OOxA.LLmbm4wQQ88JO-6eZmAejyZM2lM' #delete before pushing
GUILD = "OreoShunment's Demonhack Server"

client = discord.Client()
for guild1 in client.guilds:
    if guild1.name == GUILD:
        guild = guild1
        break

prefix = '!'
groupCreated = False
answerOptions = ['A', 'B', 'C', 'D']


@client.event
async def on_message(message):
    def check(reaction, user):
        emoji1 = discord.utils.get(message.author.guild.emojis, name='one')
        emoji2 = discord.utils.get(message.author.guild.emojis, name='two')
        emoji3 = discord.utils.get(message.author.guild.emojis, name='three')
        emoji4 = discord.utils.get(message.author.guild.emojis, name='four')
        return user == message.author and str(reaction.emoji) == emoji1 or emoji2 or emoji3 or emoji4

    global groupCreated
    guild = client.guilds[0]
    if message.author == client.user: #don't want bot replying to itself
        return
    
    if message.content.lower().startswith(prefix + 'group create'):
        if any(role.name.lower() == 'staff' for role in message.author.roles):#check for 'instructor' role (required)
            targetVoiceChnl = message.author.voice.channel
            listMbrsInVoiceChnl = targetVoiceChnl.members
            numStudentsInVoiceChnl = len(listMbrsInVoiceChnl)

            msgList = message.content.split()
            maxNumOfStudentsInGroup = int(msgList[2])
            if maxNumOfStudentsInGroup < 1:
                await message.channel.send('Must be a positive non-zero number')
                return
            numChnlsToCreate = numStudentsInVoiceChnl // maxNumOfStudentsInGroup
            remainder = numStudentsInVoiceChnl % maxNumOfStudentsInGroup
            
            category = discord.utils.get(guild.categories, name='VOICE CHANNELS')
            for i in range(numChnlsToCreate):
                group = 'Group'
                chnlName = group + str(i)
                roleName1 = group + str(i)
                ROLE = await guild.create_role(name=roleName1)
                TXTCHNL = await guild.create_text_channel(chnlName)
                VOICECHNL = await guild.create_voice_channel(chnlName)
            groupCreated = True
        else:
            await message.channel.send('Must be staff member')


    elif message.content.lower() == prefix + 'group start':
        newRoles = []
        for j in range(maxNumOfStudentsInGroup):
            rand = random.randint(0, numStudentsInVoiceChnl-1)
            chnl = discord.utils.get(guild.voice_channels, name=chnlName)
            await listMbrsInVoiceChnl[rand].move_to(chnl)
            del listMbrsInVoiceChnl[rand]
            numStudentsInVoiceChnl -= 1
            '''
            guildRoles = guild.roles
            for guildRole in guildRoles:
                newRoles.append(guildRole)  

            every1 = discord.utils.get(guild.roles, name='@everyone')      
            targetRole1 = discord.utils.get(guild.roles, name=roleName1)
            for j in range(maxNumOfStudentsInGroup):
                rand = random.randint(0, numStudentsInVoiceChnl-1)
                await listMbrsInVoiceChnl[rand].add_roles(targetRole1)
                del listMbrsInVoiceChnl[rand]
                numStudentsInVoiceChnl -= 1
            


            guildTextChnls = guild.text_channels
            for guildTextChnl in guildTextChnls:
                if guildTextChnl.name == chnlName:
                    targetTextChnl = guildTextChnl
            await targetTextChnl.set_permissions(targetRole, read_messages=True, send_messages=True)
            await targetTextChnl.set_permissions(every1, read_messages=False, send_messages=False)



            guildVoiceChnls = guild.voice_channels
            for guildVoiceChnl in guildVoiceChnls:
                if guildVoiceChnl.name == chnlName:
                    targetVoiceChnl = guildVoiceChnl
            await targetVoiceChnl.set_permissions(targetRole, read_messages=True, send_messages=True)
            await targetVoiceChnl.set_permissions(every1, read_messages=False, send_messages=False)
            '''
        '''
        k = 0
        for member in listMbrsInVoiceChnl:
            await member.add_roles(newRoles[k])
            k += 1
        '''


    elif message.content.lower() == prefix + 'group end':
        return



    elif message.content.lower() == prefix + 'poll':
        answers = []
        x = 4
        lstIndex = 0
        t_end = time.time() + 60
        await message.channel.send('Enter question')
        try:
            msg1 = await client.wait_for('message', timeout=30.0)
        except asyncio.TimeoutError:
            await message.channel.send('No response, poll cancelled')
        question = msg1.content
        while x > 0:
            msg = 'Enter option ' + answerOptions[lstIndex] + ", or enter 'end' to cancel poll"
            await message.channel.send(msg)
            try:
                msg2 = await client.wait_for('message', timeout=30.0)
                if msg2.content == 'end':
                    await message.channel.send('Poll cancelled')
                    return
                answers.append(msg2.content)
                lstIndex += 1
                x -= 1
            except asyncio.TimeoutError:
                await message.channel.send('No response, poll cancelled')
                return
        
        message1 = await message.channel.send('**Poll:**\n' + question + '\n\n:one:  ' + answers[0] + '\n:two:  ' + answers[1] + '\n:three:  ' + answers[2] + '\n:four:  ' + answers[3] + '\n\nPoll will end in 60 seconds' + '\nAnswer by reacting to this message with the corresponding emojis:') 
        await message1.add_reaction('1️⃣')
        await message1.add_reaction('2️⃣')
        await message1.add_reaction('3️⃣')
        await message1.add_reaction('4️⃣')

        while time.time() < t_end:
            try:
                reaction, user = await client.wait_for('reaction_add', timeout=35.0, check=check)
            except asyncio.TimeoutError:
                pass

        await message.channel.send('Poll ended')

@client.event
async def on_ready():
    for guild1 in client.guilds:
        if guild1.name == GUILD:
            guild = guild1
            break
    print(client.user, 'connected to guild ', guild.name, '#', guild.id)

client.run(TOKEN)