import voxelbotutils as utils
import discord
from discord.ext import commands
import string


class MessageBlacklist(utils.Cog):

    @utils.group()
    @commands.has_permissions(manage_guild=True)
    async def blacklist(self, ctx: utils.Context):
        return

    @blacklist.command()
    @commands.has_permissions(manage_guild=True)
    async def add(self, ctx: utils.Context, word: str):
        """Add words to blacklist"""

        word = ''.join( [c for c in word.lower() if c not in set(string.punctuation + string.digits + string.whitespace)] )
        
        # Create a database connection and insert the word into the database        
        async with self.bot.database() as db:
            data = await db("INSERT INTO blacklist_words (guild_id, word) VALUES ($1, $2)", ctx.guild.id, word.lower())

        await ctx.send(f"Added `{word.lower()}` to the blacklist.")

    @blacklist.command()
    @commands.has_permissions(manage_guild=True)
    async def remove(self, ctx: utils.Context, word: str):
        """removes words to blacklist"""

        word = ''.join( [c for c in word.lower() if c not in set(string.punctuation + string.digits + string.whitespace)] )
        
        # Create a database connection and insert the word into the database        
        async with self.bot.database() as db:
            data = await db("DELETE FROM blacklist_words WHERE guild_id = $1 AND word = $2", ctx.guild.id, word)

        await ctx.send(f"Removed `{word}` to the blacklist.")

    @blacklist.command()
    @commands.has_permissions(manage_guild=True)
    async def list(self, ctx: utils.Context):
        """lists blacklisted words"""
        
        # Create a database connection and insert the word into the database        
        async with self.bot.database() as db:
            data = await db("SELECT word FROM blacklist_words WHERE guild_id = $1", ctx.guild.id)

        # Check if there are any blacklisted works
        if len(data) == 0:
            return

        blacklisted_words = ""

        # Turn database result to a list
        for x in data:
            blacklisted_words += "`"+x["word"]+"` "

        await ctx.send(f"Blacklist: " + blacklisted_words)

    @utils.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Check all messages and check if message contains a blacklisted word"""
        if message.author == message.guild.me:
            return

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

        msg = ''.join( [c for c in message.content.lower() if c not in set(string.punctuation + string.digits + string.whitespace)] )

        
        # Check if blacklisted word is in message
        for word in blacklisted_words:
            if word in msg:
                await message.delete()
                await message.channel.send(f"{message.author.mention} you can't say that word! >:(")
                self.bot.dispatch('blacklisted_word', message.author, word)


def setup(bot:utils.Bot):
    x = MessageBlacklist(bot)
    bot.add_cog(x)
