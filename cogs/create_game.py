import discord
from discord.ext import commands
from db import db


class NewGame(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    
    @commands.command(name="new_game",
                      usage='{prefix}new_game [game_id] [captain_1], [captain_2] [player1] [player2]....[playerN]',
                      description="create a new game handle with \
                      all the players in the specified gathering voice \
                      channel + all the mentioned players.")
    @commands.guild_only()
    @commands.has_permissions()
    async def new_game(self, ctx, game_id, captain_1, captain_2, *args):
        server = db.get_server(ctx.message.guild.id)
        if len(server == 3):
            
            gathering_channel = await self.bot.get_channel(server.gathering_spot)
            members = set(gathering_channel.members + [member for member in args].append(ctx.message.author.id))
            members.append(captain_1)
            members.append(captain_2)
            db.new_game(game_id, ctx.message.author.id, captain_1, captain_2, members)
    
    
    @commands.command(name="me",
                      usage='{prefix}me [player] [game]',
                      description="as a captain, choose a player for my team")
    @commands.guild_only()
    @commands.has_permissions()
    async def me(self, ctx, player, game):
        try:
            team = db.get_captain_team(game, ctx.message.author.id)
            if team in ['team_1', 'team_2']:
                db.add_player(game, team, player.id)
                await ctx.send(f"accepted <@{player.id}> on {'team red' if team == 'team_1' else 'team blue'}")
            else:
                await ctx.send(f'you are not a captain in the game you mentioned.')
        except Exception as e:
            await ctx.send(e)


def setup(bot: commands.Bot):
    bot.add_cog(NewGame(bot))
