import discord
from discord.ext import commands
from db import db


class Setup(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    
    # @commands.command(name="set_up",
    #                 usage='{prefix}set_up [gathering_channel] \
    #                 [team1_channel] [team2_channel]',
    #                 description="setup the gathering spot and the target \
    #                 team locations (red & blue teams)")
    # @commands.guild_only()
    # @commands.has_permissions(administrator=True)
    # async def set_up(self, ctx, gathering_channel: discord.VoiceChannel,
    #         team_1: discord.VoiceChannel, team_1_role: discord.Role,
    #         team_2: discord.VoiceChannel, team_2_role: discord.Role,
    #         neutral: discord.VoiceChannel, neutral_role: discord.Role,
    #         gm_role: discord.Role):
    #     try:
    #         db.setup_server(ctx.message.guild.id, gathering_channel.id, team_1.id,
    #                         team_1_role.id, team_2.id, team_2_role.id, neutral.id, neutral_role.id, gm_role.id )
    #         await ctx.send(f'setup complete! you can use the {await self.bot.get_prefix(ctx.message)}help to see how to proceed')
    #     except Exception as e:
    #         await ctx.send(f'setup failed. Message DAKI4#1002 if setup fails again.')
    #         await ctx.send(e)


    @commands.command(name="set_up",
                    usage='{prefix}set_up [gathering_channel] \
                    [team1_channel] [team2_channel]',
                    description="setup the gathering spot and the target \
                    team locations (red & blue teams)")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def set_up(self, ctx, bot_channel: discord.TextChannel, gathering_channel: discord.VoiceChannel):
        try:
            db.setup_server(ctx.message.guild.id, bot_channel.id, gathering_channel.id)
            await ctx.send(f'setup complete! you can use the {await self.bot.get_prefix(ctx.message)}help to see how to proceed')
        except Exception as e:
            await ctx.send(f'setup failed. Message DAKI4#1002 if setup fails again.')
            await ctx.send(e)


    # @commands.command(name="setup",
    #                 usage='{prefix}setup [gathering_channel] \
    #                 [team1_channel] [team2_channel]',
    #                 description="setup the gathering spot and the target \
    #                 team locations (red & blue teams)")
    # @commands.guild_only()
    # @commands.has_permissions(administrator=True)
    # async def help_setup(self, ctx):
    #     await ctx.send(f'run the {self.bot.prefix}setup command. \
    #                      when you run the {self.bot.prefix}setup \
    #                      <#gatherging_area vcid> <#team_1 vcid> <#team_ 2vcid>. \
    #                      the command must look at the end like this: \n\
    #                      {self.bot.prefix}setup <#1123214124> <#545435123> <#2135663546> \n\
    #                      also: to get the IDs that the bot requires, right click on a voice \
    #                      channel and at the bottom > copy ID.')

def setup(bot: commands.Bot):
    bot.add_cog(Setup(bot))
