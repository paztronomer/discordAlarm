import os
import discord
import json

# ToDo
# 1. Add a command to set the alarm
# 2. Add a command to toggle the alarm on and off
# 3. Add a command to display the time left until the alarm goes off
# 4. Add a command to display the time the alarm is set to go off
# 5. Add a command to display the current time
# 6. Add a command to display the current time in a different timezone
# 7. add command to display any time in different timezones
# 
# Put this in a class for client

# Load the token from the json file
with open("../credentials.json") as f:
    data = json.load(f)
    token = data["token"]

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
    """
    This function is called whenever the bot sees a message in a channel it has access to.
    Depending on the message, the bot will respond with either a message or triggering an action.
    """
    if message.author == client.user:
        return

    # Listing available commands
    help_text = "Available commands:\n" \
                "\t/help - Display this message\n" \
                "\t/alarm - Immediatly triggers the alarm\n" \
                "\t/alarm set [local time in 00:00 format]- Set an alarm\n" \
                "\t/toggle - Turn the alarm on and off while not resetting the previously set time\n" \
                "\t/countdown - provide the amount of time left until the alarm goes off"

    if message.content.startswith("/help"):
        await message.channel.send(help_text)

    # Trigger the alarm, mentioning who did it
    if message.content.startswith("/alarm"):
        await message.channel.send(f'@everyone {message.author} has triggered the alarm!')


# Read the token from json file
client.run(token)

"""
Idea for the alarm
import discord
import asyncio
from datetime import datetime, timedelta

# Initialize the Discord client
client = discord.Client()

# Event to run when the bot is ready
@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

# Command to schedule a message
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!schedule'):
        # Extract the time and message from the command
        command_parts = message.content[len('!schedule'):].strip().split(' ', 1)
        
        # Check if the command format is correct
        if len(command_parts) != 2:
            await message.channel.send('Invalid command format. Usage: !schedule <time> <message>')
            return
        
        # Parse the time
        try:
            scheduled_time = datetime.strptime(command_parts[0], '%Y-%m-%d %H:%M')
        except ValueError:
            await message.channel.send('Invalid time format. Please use YYYY-MM-DD HH:MM.')
            return

        # Calculate the delay until the scheduled time
        current_time = datetime.utcnow()
        delay = (scheduled_time - current_time).total_seconds()

        # Schedule the message
        if delay <= 0:
            await message.channel.send('Scheduled time must be in the future.')
        else:
            await schedule_message(delay, command_parts[1], message.channel)

# Function to schedule the message
async def schedule_message(delay, content, channel):
    await asyncio.sleep(delay)
    await channel.send(content)

# Run the bot with the Discord token
client.run('YOUR_DISCORD_BOT_TOKEN')

"""
