import discord
import time
from discord.ext import commands, tasks
from db import db


class NewGame(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.command(name="new_game")
    @commands.guild_only()
    @commands.has_permissions()
    async def new_game(self, ctx, captain_1: discord.Member, captain_2: discord.Member, *args: discord.Member):
        server = db.get_server(ctx.message.guild.id)
        gathering_channel = self.bot.get_channel(server['gathering_spot'])
        print([*args])
        members = list(set([*[i.id for i in args], *[i.id for i in gathering_channel.members if i not in [captain_1, captain_2]]]))
        print(members)
        new_game_id = self.generate_game_id(ctx)
        db.new_game(new_game_id, ctx.message.guild.id, ctx.message.author.id, captain_1.id, captain_2.id, members)
        await self.send_embed(ctx, new_game_id)


    def generate_game_id(self, ctx):
        return ctx.message.id


    async def get_game_id(self, guild):
        messages = await self.bot.get_channel(db.get_server(guild)['bot_channel']).history(limit=200).flatten()
        gid = [i for i in messages  if '?/new_game' in i.content]
        return gid[0].id


    @commands.command(name="me")
    @commands.guild_only()
    @commands.has_permissions()
    async def me(self, ctx, player: discord.Member):
        try:
            team = db.get_captain_team(await self.get_game_id(ctx.message.guild.id), ctx.message.author.id)
            pl_t = db.get_player_team(await self.get_game_id(ctx.message.guild.id), player.id)
            print(pl_t)
            if pl_t in ['team_1', 'team_2', 'neutral']:
                await ctx.send(f'player <@{player.id}> has already been picked ')
            else:
                if team in ['team_1', 'team_2']:
                    db.add_player(await self.get_game_id(ctx.message.guild.id), team, player.id)
                    db.remove_start_player(await self.get_game_id(ctx.message.guild.id), player.id)
                    await ctx.send(f"accepted <@{player.id}> on {'team red' if team == 'team_1' else 'team blue' if team == 'team_2' else 'neutral'}")
                else:
                    await ctx.send(f'you are not a captain in the game you mentioned.')
                time.sleep(2)
                await self.send_embed(ctx, db.get_game(await self.get_game_id(ctx.message.guild.id)))
        except Exception as e:
            print(e)


    # @commands.command(name="remove",
    #                   usage='[player] [game]',
    #                   description="remove player from a game")
    # @commands.guild_only()
    # @commands.has_permissions()
    # async def remove(self, ctx, player: discord.Member, ):
    #     if ctx.message.author.id == db.get_host(await self.get_game_id(ctx.message.guild.id)):
    #         a = db.get_player_team(await self.get_game_id(ctx.message.guild.id), player.id)
    #         if a is None:
    #             db.remove_start_player(await self.get_game_id(ctx.message.guild.id), player.id)
    #         else:
    #             try:
    #                 db.remove_player(await self.get_game_id(ctx.message.guild.id), a, player.id)
    #                 db.remove_start_player(await self.get_game_id(ctx.message.guild.id), player.id)
    #             except Exception as e:
    #                 print(e)
    #         await self.send_embed(await self.get_game_id(ctx.message.guild.id)['_id'])
    #     else:
    #         await ctx.send(f'you arent the host of this game')


    @commands.command(name="status")
    @commands.guild_only()
    @commands.has_permissions()
    async def status(self, ctx):
        print(await self.get_game_id(ctx.message.guild.id))
        await self.send_embed(ctx, await self.get_game_id(ctx.message.guild.id))


    @commands.command(name="join")
    @commands.guild_only()
    @commands.has_permissions()
    async def join(self, ctx):
        db.add_start_player(await self.get_game_id(ctx.message.guild.id), ctx.message.author.id)
        game = db.get_game(await self.get_game_id(ctx.message.guild.id))

        await self.send_embed(game['_id'])


    async def get_history(channel: discord.TextChannel):
        messages = await channel.history(limit=200).flatten()
        return messages


    async def send_embed(self, ctx, game):
        db_game = db.get_game(game)
        embed = discord.Embed(title=f'{db_game["_id"]}')
        j = db.get_team(db_game['_id'], 'team_1')
        k = db.get_team(db_game['_id'], 'team_2')

        embed.add_field(name='free players:', value=' '.join(f' <@{i}>' for i in db_game['initial_players']),
                        inline=False)
        embed.add_field(name="Red team:",
                        value=' '.join([f' <@{i}>' if len(j) > 0 else "." for i in j]), inline=False)
        embed.add_field(name="Blue team:",
                        value=' '.join([f' <@{i}>' if len(k) > 0 else "." for i in k]), inline=False)
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(NewGame(bot))
