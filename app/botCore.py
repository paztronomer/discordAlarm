import os
import json
import asyncio
from datetime import datetime, timedelta

import discord


__author__ = "Francisco Paz"
__version__ = "0.1.0"
__status__ = "Development"


class AlarmClient(discord.Client):

    def __init__(self, *args, **kwargs):
        # Makes sur to call parent init
        super().__init__(*args, **kwargs)
        self.alarm_on = False
        self.alarm_hh = -1
        self.alarm_mm = -1
        self.aalrm_was_set_by_user = None
        self.alarm_datestamp = None

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
                    "\t/alarm set [local time in HH:MM in 24h format, UTC]- Set an alarm in UTC time\n" \
                    "\t/toggle - Turn the alarm on and off while not resetting the previously set time\n" \
                    "\t/countdown - Displays the amount of time left until the alarm goes off\n" \
                    "\t/alarm time - Display the time the alarm is set to go off\n" \
                    "\t/utc now - Display the current time in UTC\n" \
                    "\t/alarm set by - Display the user who set the alarm\n" \
                    "\t/alamr was set when - Display the time the alarm was set\n" \
                    "\t/utc to local - Display the current UTC time in different timezones\n"
       

        if message.content.startswith("/help"):
            await message.channel.send(help_text)

        # Trigger the alarm, mentioning who did it
        if message.content.startswith("/alarm"):
            await message.channel.send(f'@everyone {message.author} has triggered the alarm!')

        # Toggle the alarm on and off
        if message.content.startswith("/toggle"):
            self.alarm_on = not self.alarm_on
            await message.channel.send(f'Alarm is now {"on" if self.alarm_on else "off"}')

        # Set the alarm
        if message.content.startswith("/alarm set"):
            # Extract the time from the message
            command_parts = message.content[len('/alarm set'):].strip()
            # Check if the command format is correct
            if len(command_parts) != 5:
                await message.channel.send('Invalid command format. Usage: /alarm set <time in 00:00 format>')
                return
            # Validate the alarm time values
            try:
                hour = int(command_parts[:2])
                minute = int(command_parts[3:])
            except ValueError:
                await message.channel.send('Invalid time format. Please use HH:MM in 24h format, UTC time.')
                return
            if hour < 0 or hour > 23 or minute < 0 or minute > 59:
                await message.channel.send('Invalid time format. Please use 00-23:00-59 format.')
                return
            self.alarm_hh = hour
            self.alarm_mm = minute
            self.alarm_datestamp = datetime.now(datetime.timezone.utc)
            # Set the alarm time in UTC
            # Calculate the delay until the scheduled time
            current_time = datetime.now(datetime.timezone.utc)
            # Calculate scheduled time in UTC, then calculate delay
            scheduled_time = current_time.replace(hour=self.alarm_hh, minute=self.alarm_mm, second=0, microsecond=0)
            delay = (scheduled_time - current_time).total_seconds()
            # If delay < 0, the alarm is set for the next day
            if delay < 0:
                delay += 86400
            # Call the waiting function
            await self.schedule_alarm(delay, message)
            self.alarm_was_set_by_user = message.author
            # Send a message to the channel to confirm the alarm is set
            await message.channel.send(f'Alarm is set to go off at {command_parts}, UTC time.')

        # Provide the amount of time left until the alarm goes off
        if message.content.startswith("/countdown"):
            # Calculate the delay until the scheduled time
            current_time = datetime.now(datetime.timezone.utc)
            scheduled_time = current_time.replace(hour=self.alarm_hh, minute=self.alarm_mm, second=0, microsecond=0)
            delay = (scheduled_time - current_time).total_seconds()
            # If delay < 0, the alarm is set for the next day
            if delay < 0:
                delay += 86400
            # Send a message to the channel to confirm the alarm is set
            await message.channel.send(f'Time left until the alarm goes off: {str(timedelta(seconds=delay))} sec, {str(timedelta(minutes=delaya/60))} min, {str(timedelta(hours=delay/3600))} hours.')

        # Provide the time the alarm is set to go off
        if message.content.startswith("/alarm time"):
            await message.channel.send(f'Alarm is set to go off at {self.alarm_hh}:{self.alarm_mm}, UTC time.')

        # Provide the current time in UTC
        if message.content.startswith("/utc now"):
            await message.channel.send(f'Current time in UTC: {datetime.now(datetime.timezone.utc).strftime("%H:%M:%S")}')

        # Provide the user who set the alarm
        if message.content.startswith("/alarm set by"):
            await message.channel.send(f'Alarm was set by {self.alarm_was_set_by_user}')
        
        # Provide the time the alarm was set
        if message.content.startswith("/alarm was set when"):
            await message.channel.send(f'Alarm was set at {self.alarm_datestamp}, UTC time.')
        
        # Provide the current UTC time in different timezones
        if message.content.startswith("/utc to local"):
            await message.channel.send(f'Current time in UTC: {datetime.now(datetime.timezone.utc).strftime("%H:%M:%S")}')
            # Add more timezones here
            await message.channel.send(f'Current time in EST: {datetime.now(datetime.timezone.utc).astimezone(timezone("US/Eastern")).strftime("%H:%M:%S")}')
            await message.channel.send(f'Current time in PST: {datetime.now(datetime.timezone.utc).astimezone(timezone("US/Pacific")).strftime("%H:%M:%S")}')
            await message.channel.send(f'Current time in CET: {datetime.now(datetime.timezone.utc).astimezone(timezone("CET")).strftime("%H:%M:%S")}')
            await message.channel.send(f'Current time in JST: {datetime.now(datetime.timezone.utc).astimezone(timezone("JST")).strftime("%H:%M:%S")}')
            await message.channel.send(f'Current time in AEST: {datetime.now(datetime.timezone.utc).astimezone(timezone("Australia/Sydney")).strftime("%H:%M:%S")}')
            await message.channel.send(f'Current time in IST: {datetime.now(datetime.timezone.utc).astimezone(timezone("Asia/Kolkata")).strftime("%H:%M:%S")}')
            await message.channel.send(f'Current time in SGT: {datetime.now(datetime.timezone.utc).astimezone(timezone("Asia/Singapore")).strftime("%H:%M:%S")}')
            await message.channel.send(f'Current time in NZST: {datetime.now(datetime.timezone.utc).astimezone(timezone("NZ")).strftime("%H:%M:%S")}')
            await message.channel.send(f'Current time in BRT: {datetime.now(datetime.timezone.utc).astimezone(timezone("America/Sao_Paulo")).strftime("%H:%M:%S")}')
            await message.channel.send(f'Current time in ART: {datetime.now(datetime.timezone.utc).astimezone(timezone("America/Argentina/Buenos_Aires")).strftime("%H:%M:%S")}')
            await message.channel.send(f'Current time in CLT: {datetime.now(datetime.timezone.utc).astimezone(timezone("Chile/Continental")).strftime("%H:%M:%S")}')
            await message.channel.send(f'Current time in EAT: {datetime.now(datetime.timezone.utc).astimezone(timezone("Africa/Nairobi")).strftime("%H:%M:%S")}')
            await message.channel.send(f'Current time in WAT: {datetime.now(datetime.timezone.utc).astimezone(timezone("Africa/Lagos")).strftime("%H:%M:%S")}')
            await message.channel.send(f'Current time in EET: {datetime.now(datetime.timezone.utc).astimezone(timezone("Europe/Bucharest")).strftime("%H:%M:%S")}')
            await message.channel.send(f'Current time in GST: {datetime.now(datetime.timezone.utc).astimezone(timezone("Asia/Dubai")).strftime("%H:%M:%S")}')

        
    # Function to schedule the alarm
    async def schedule_alarm(self, delay, message):
        await asyncio.sleep(delay)
        if self.alarm_on:
            await message.channel.send(f'@everyone Alarm is ringing!')
        else:
            await message.channel.send(f'@everyone Alarm was set for {self.alarm_hh}:{self.alarm_mm} but it was turned off')

if __name__ == "__main__":
        
    # Load the token from the json file
    with open("../credentials.json") as f:
        data = json.load(f)
        token = data["token"]

    intents = discord.Intents.default()
    intents.message_content = True

    client = AlarmClient(intents=intents)

    # Read the token from json file
    client.run(token)