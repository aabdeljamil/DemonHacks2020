import discord
import time

TOKEN = 'NzY5Mzg3ODIyMjY3NDk4NTA2.X5OSPw.atVBzBlXNmLMAOtYeKY_a7CpeYg' #deleted for security purposes
GUILD = "OreoShunment's Demonhack Server"

client = discord.Client(intents=discord.Intents.all())
default_points = 10.0;

@client.event
async def on_ready():
    print('Running')

@client.event
async def on_message(message):
    
    '''
    if any(role.name.lower() == 'staff' for role in message.author.roles):
        if message.content.lower().startswith('a'):
            channel = message.channel
            await channel.send ("Send us your First and Last name for attendance!")
            
            def check(m):
                return m.content == 'hello' and m.channel == channel
            
            msg = await client.wait_for('message', check=check)
            await channel.send('Hello{.author}!'.format(msg))
    '''
    if message.content.lower() == 'test':
        #First find length of students in list
        #assume that this list of students is called students_list
        student_list = ['Mutasim', 'Abdallah', 'Ibrahim', 'Bob', 'Steve', 'Rodgers']
        numof_students = len(student_list)
            
        
        #Create dictionary by combining list of students(their name) and list of 
        #default_points (Participation points students start off with)
        
        student_dict = {}
        for student in student_list:
            student_dict[student] = default_points
            
        
        class_list = ''
        i = 1

        for student in student_dict:
            class_list += str(i) + ': ' + student + ', ' + str(student_dict[student]) + '/10.0' + '\n'
            int(i)
            i = i + 1
            
        
        #Send on channel the amount of points each student has
        
        await message.channel.send('Present students and their grades:\n' + class_list)
    
    
client.run(TOKEN)