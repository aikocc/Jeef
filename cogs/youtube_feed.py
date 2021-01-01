import discord
from discord.ext import tasks
import voxelbotutils as utils


class YoutubeFeed(utils.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.youtuber_ids = ["UCElglHNtOwvSwq0UC1ygxSA",] #TODO get from Config
        self.YOUTUBE_API_KEY = bot.config["youtube"]["api_token"]

        self.get_youtube_feed.start()

    def cog_unload(self):
        self.get_youtube_feed.stop()

    @tasks.loop(seconds=5)
    async def get_youtube_feed(self):

        for youtube_id in self.youtuber_ids:

            video_links = []

            headers = {
                "Authorization": f"Bearer {self.YOUTUBE_API_KEY}",
                "Accept": "application/json",
            }

            async with self.bot.session.get(f"https://youtube.googleapis.com/youtube/v3/search?part=snippet&channelId={youtube_id}&type=video&key={self.YOUTUBE_API_KEY}", headers=headers) as r:
                data = await r.json()

                number_of_new_videos = data["pageInfo"]["resultsPerPage"]

                if number_of_new_videos == 0:
                    return

                new_videos = data["items"]
                for x in new_videos:
                	video_links.append(x)

            message = f"Woah {new_videos[0]['snippet']['channelTitle']} has just uploaded a new video, you should go check it out!\n\n{'\n'.join(video_links)}"
                
            await self.bot.get_guild(793352612568760320).get_channel(794347469483671564).send(message)



def setup(bot:utils.Bot):
    x = YoutubeFeed(bot)
    bot.add_cog(x)