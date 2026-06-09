import discord
import os
from threading import Thread
from flask import Flask

# --- The Fake Web Server to keep Render awake ---
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is awake and watching for boosts!"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- The Actual Discord Bot ---
intents = discord.Intents.default()
intents.message_content = True # Required so the bot can read system messages
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Successfully logged in as {client.user}')

@client.event
async def on_message(message):
    # Ignore normal text messages or other bots
    if message.author.bot:
        return

    # Check if the message is a native Discord system message for a server boost
    boost_types = [
        discord.MessageType.premium_guild_subscription,
        discord.MessageType.premium_guild_tier_1,
        discord.MessageType.premium_guild_tier_2,
        discord.MessageType.premium_guild_tier_3
    ]
    
    if message.type in boost_types:
        embed = discord.Embed(
            title="🚀 Server Boosted!",
            description=f"Massive thanks to {message.author.mention} for boosting the server! 🎉\n\nEnjoy the shiny pink badge and new perks.",
            color=0xf47fff # Discord Nitro Pink
        )
        embed.set_thumbnail(url=message.author.display_avatar.url)
        
        # Try to delete Discord's boring default system message
        try:
            await message.delete()
        except discord.Forbidden:
            print("Bot doesn't have permission to delete the default message.")
            
        # Send the shiny new embed
        await message.channel.send(embed=embed)

if __name__ == "__main__":
    keep_alive() # Start the fake web server
    client.run(os.environ.get('DISCORD_TOKEN')) # Start the bot using your hidden token
