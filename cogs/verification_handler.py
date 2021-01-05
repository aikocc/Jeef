import discord
import voxelbotutils as utils
import string
import random


class VerificationHandler(utils.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.random_code = dict()

    @utils.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """
        Member Join Handler
        """
        if member.guild.id != 795795423838470186:
        	return

        code = "".join([random.choice(list(string.ascii_letters + string.digits + ' ')) for _ in range(10)])

        self.random_code[member.id] = code

        welcome_message = textwrap.dedent(f"""
        	Welcome to `{member.guild.name}`.

        	To help fight against bots and automated raids we have implemented a verification system.
        	To verify you'll need to `.verify <code>` without the <>.

        	Your Code is: `{self.random_code[member.id]}`
        """)

        await member.send(welcome_message)

    @utils.command()
    async def verify(self, ctx: utils.Context, code: str):
    	"""
    	Verify Command
    	"""

    	if self.random_code[ctx.author.id] == code:
    		guild = self.bot.get_guild(795795423838470186)
    		member = guild.get_member(ctx.author.id)
    		try:
    			await member.add_roles(guild.get_role(795796913508974622))
    		except Exception as e:
    			raise e

def setup(bot:utils.Bot):
    x = VerificationHandler(bot)
    bot.add_cog(x)
