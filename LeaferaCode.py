import discord
from discord import app_commands
import random

class LeaferaCode:
    
    def __init__(self):
        pass
    def random_emoji():       
        # List of emojis to choose from
        emojis = [
            '💌',
            '🕳️',
            '🛀',
            '🛌',
            '🔪',
            '🗺️',
            '🧭'
        ]
        # Return a random emoji from the list
        return random.choice(emojis)

    def random_room_name():
        # List of room names to choose from
        room_names = [
            "Office",
            "Meeting Room",
            "Conference Room",
            "Break Room",
            "Lounge",
            "Reception",
            "Training Room",
            "Auditorium",
            "Boardroom",
            "Collaboration Space",
            "Classroom",
            "Workshop",
            "Seminar Room",
            "Meditation Room"
        ]
        return random.choice(room_names)
    async def OpenOffice(member, before, after):
    
        new_room = None
        # Check if the user entered the specific voice channel
        if after.channel is not None and after.channel.name == "🏦השכרת משרדים":
            category = discord.utils.get(after.channel.guild.categories, id = 843477859020308513)
                  
            # Create a new room with their name
            emoji = LeaferaCode.random_emoji()
            room = LeaferaCode.random_room_name()
            new_room = await after.channel.guild.create_voice_channel(f"{member.name} {room} {emoji}", category=category)
            # Move the member to the new room     
            await member.move_to(new_room)

        if new_room != None:
            return new_room.id
        else:
            return None

   