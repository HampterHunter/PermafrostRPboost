# --- The Actual Discord Bot ---
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# DROP YOUR COPIED CHANNEL ID HERE (No quotes!)
TARGET_CHANNEL_ID = 1511793049192108175

@client.event
async def on_ready():
    print(f'Successfully logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author.bot:
        return

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
            color=0xf47fff 
        )
        embed.set_thumbnail(url=message.author.display_avatar.url)
        
        try:
            await message.delete()
        except discord.Forbidden:
            print("Bot doesn't have permission to delete the default message.")
            
        # --- THE FIX: ROUTE TO SPECIFIC CHANNEL ---
        target_channel = client.get_channel(TARGET_CHANNEL_ID)
        
        if target_channel:
            await target_channel.send(embed=embed)
            print(f"Successfully sent boost embed to {target_channel.name}")
        else:
            print("ERROR: Could not find the target channel. Check the ID and bot permissions.")
