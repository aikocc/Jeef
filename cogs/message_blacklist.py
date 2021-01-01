import voxelbotutils as utils
import discord
import string


class MessageBlacklist(utils.Cog):

    @utils.group()
    async def blacklist(self, ctx: utils.Context):
        await ctx.send("Pong!")

    @blacklist.command()
    async def add(self, ctx: utils.Context, word: str):
        """Add words to blacklist"""
        
        # Create a database connection and insert the word into the database        
        async with self.bot.database() as db:
            data = await db("INSERT INTO blacklist_words (guild_id, word) VALUES ($1, $2)", ctx.guild.id, word)

        await ctx.send(f"Added `{word}` to the blacklist.")

    @blacklist.command()
    async def remove(self, ctx: utils.Context, word: str):
        """removes words to blacklist"""
        
        # Create a database connection and insert the word into the database        
        async with self.bot.database() as db:
            data = await db("DELETE FROM blacklist_words WHERE guild_id = $1, word = $2", ctx.guild.id, word)

        await ctx.send(f"Removed `{word}` to the blacklist.")

    @utils.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Check all messages and check if message contains a blacklisted word"""

        # Start a database connection and grab all blacklisted words
        async with self.bot.database() as db:
            data = await db("SELECT word FROM blacklist_words WHERE guild_id = $1", message.guild.id)

        # Check if there are any blacklisted works
        if len(data) == 0:
            return

        blacklisted_words = []

        # Turn database result to a list
        for x in data:
            blacklisted_words.append(x["word"])

        msg = message.content.strip(list(string.punctuation + string.digits + " "))

        # Check if blacklisted word is in message
        for word in blacklisted_words:
            if word in msg:
                await message.delete()
                await message.channel.send(f"{message.author} you can't say that word! >:(")


def setup(bot:utils.Bot):
    x = MessageBlacklist(bot)
    bot.add_cog(x)
