import discord
from discord.ext import tasks
import voxelbotutils as utils


class TikTokFeed(utils.Cog):

    def __init__(self, bot):
    	self.bot = bot
    	self.tiktok_updater.start()

    @task.loop(seconds=15)



def setup(bot:utils.Bot):
    x = CustomUserVCs(bot)
    bot.add_cog(x)
