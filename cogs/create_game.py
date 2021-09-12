import discord
import time
from discord.ext import commands, tasks
import discord.utils
from db import db
from typing import Tuple


class NewGame(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # self.gc.start()


    @commands.command(name="new_game",
                      usage='{prefix}new_game [game_id] [captain_1], [captain_2] [player1] [player2]....[playerN]',
                      description="create a new game handle with \
                      all the players in the specified gathering voice \
                      channel + all the mentioned players.")
    @commands.guild_only()
    @commands.has_permissions()
    async def new_game(self, ctx, game_id, captain_1: discord.Member, captain_2: discord.Member, *args: discord.Member):
        try:
            server = db.get_server(ctx.message.guild.id)
            # if len(server) == 9:
            gathering_channel = self.bot.get_channel(server['gathering_spot'])
            # members = [int(i[3:-1]) for i in args]
            members = [i for i in args]
            members.extend(gathering_channel.members)
            members = list(set(members))
            st_members = [i.id for i in members.copy()]
            # captain_1 = await self.bot.fetch_user(captain_1[3:-1])
            # captain_2 = await self.bot.fetch_user(captain_2[3:-1])
            db.new_game(game_id, ctx.message.guild.id, ctx.message.author.id, captain_1.id, captain_2.id, st_members)
            game = db.get_game(game_id)
            # gm = ctx.message.guild.get_role(server['gamemaster_role'])
            # await ctx.message.author.add_roles(gm)
            # await captain_1.add_roles(ctx.message.guild.get_role(server['team_1_role']))
            # await captain_2.add_roles(ctx.message.guild.get_role(server['team_2_role']))


            embed = discord.Embed(title=f'{game["_id"]}')
            j = db.get_team(game_id, 'team_1')
            k = db.get_team(game_id, 'team_2')
            l = db.get_team(game_id, 'neutral')

            embed.add_field(name='free players:', value=' '.join(f' <@{i}>' for i in st_members), inline=False)
            print(' '.join([f' <@{i}>' if len(j) > 0 else "." for i in j]))
            print(' '.join([f' <@{i}>' if len(k) > 0 else "." for i in k]))
            print(' '.join([f' <@{i}>' if len(l) > 0 else "." for i in l]))
            print(len(db.get_team(game_id, 'neutral')))
            embed.add_field(name="Red team:",  value=' '.join([f' <@{i}>' if len(j) > 0 else "." for i in j]), inline=False)
            embed.add_field(name="Blue team:", value=' '.join([f' <@{i}>' if len(k) > 0 else "." for i in k]), inline=False)
            embed.add_field(name="Neutral:",   value='None ', inline=True)
            await ctx.send(embed=embed)
        except Exception as e:
            ctx.send(e)


    @commands.command(name="me",
                      usage='[player] [game]',
                      description="as a captain, choose a player for my team")
    @commands.guild_only()
    @commands.has_permissions()
    async def me(self, ctx, player: discord.Member, game):
        try:
            db_game = db.get_game(game)
            team = db.get_captain_team(game, ctx.message.author.id)
            pl_t = db.get_player_team(game, player.id)
            print(pl_t)
            if pl_t in ['team_1', 'team_2', 'neutral']:
                await ctx.send(f'player <@{player.id}> has already been picked ')
            else:
            # if team in ['team_1', 'team_2']:
            #     db.add_player(game, team, player.id)
            #     guild = db.get_server(ctx.message.guild.id)
            #     channel = self.bot.get_channel(guild[team])
            #     await player.add_roles(ctx.message.guild.get_role(guild[f'{team}_role']))
            #     await ctx.send(
            #         f"accepted <@{player.id}> on {'team red' if team == 'team_1' else 'team blue' if team == 'team_2' else 'neutral'}, \
            #         moving <@{player.id}> to <#{channel.id}>")
            #     db.add_player(game, team, player.id)
            #
            #     players = db.get_initial_players(game)
            #     teamed_players = [j for i in db.get_all_teamed_players(game) for j in i]
            #     [players.remove(i) if i in players else None for i in teamed_players]

                if team in ['team_1', 'team_2']:
                    db.add_player(game, team, player.id)
                    db.remove_start_player(game, player.id)
                    await ctx.send(f"accepted <@{player.id}> on {'team red' if team == 'team_1' else 'team blue' if team == 'team_2' else 'neutral'}")

                else:
                    await ctx.send(f'you are not a captain in the game you mentioned.')
                db_game = db.get_game(game)
                time.sleep(2)
                embed = discord.Embed(title=f'{db_game["_id"]}')
                j = db.get_team(db_game['_id'], 'team_1')
                k = db.get_team(db_game['_id'], 'team_2')
                l = db.get_team(db_game['_id'], 'neutral')

                embed.add_field(name='free players:', value=' '.join(f' <@{i}>' for i in db_game['initial_players']), inline=False)
                embed.add_field(name="Red team:",
                                value=' '.join([f' <@{i}>' if len(j) > 0 else "." for i in j]), inline=False)
                embed.add_field(name="Blue team:",
                                value=' '.join([f' <@{i}>' if len(k) > 0 else "." for i in k]), inline=False)
                # embed.add_field(name="Neutral:",
                #                 value=' '.join([f' <@{i}>' if len(l) > 0 else "." for i in l]), inline=True)
                await ctx.send(embed=embed)
        except Exception as e:
            print(e)


    @commands.command(name="remove",
                      usage='[player] [game]',
                      description="remove player from a game")
    @commands.guild_only()
    @commands.has_permissions()
    async def remove(self, ctx, player: discord.Member, game):
        print(player.id)
        async def embedstuff():
            db_game = db.get_game(game)
            embed = discord.Embed(title=f'{db_game["_id"]}')
            j = db.get_team(db_game['_id'], 'team_1')
            k = db.get_team(db_game['_id'], 'team_2')
            l = db.get_team(db_game['_id'], 'neutral')

            embed.add_field(name='free players:', value=' '.join(f' <@{i}>' for i in db_game['initial_players']),
                            inline=False)
            embed.add_field(name="Red team:",
                            value=' '.join([f' <@{i}>' if len(j) > 0 else "." for i in j]), inline=False)
            embed.add_field(name="Blue team:",
                            value=' '.join([f' <@{i}>' if len(k) > 0 else "." for i in k]), inline=False)
            embed.add_field(name="Neutral:",
                        value=' '.join([f' <@{i}>' if len(l) > 0 else "." for i in l]), inline=True)
            await ctx.send(embed=embed)
        if ctx.message.author.id == db.get_host(game):
            print(db.get_player_team(game, player.id))
            a = db.get_player_team(game, player.id)
            if a is None:
                db.remove_start_player(game, player.id)
                await embedstuff()
                await ctx.send(f"removed: <@{player.id}")
            else:
                db.remove_player(game, a, player.id)
                try:
                    db.remove_start_player(game, player.id)
                except Exception as e:
                    print(e)
                await embedstuff()
                await ctx.send(f"removed: <@{player.id}>")
        else:
            await ctx.send(f'you arent the host of this game')


    @commands.command(name="status",
                      usage='[player] [game]',
                      description="remove player from a game")
    @commands.guild_only()
    @commands.has_permissions()
    async def status(self, ctx, game):
        db_game = db.get_game(game)
        embed = discord.Embed(title=f'{db_game["_id"]}')
        j = db.get_team(db_game['_id'], 'team_1')
        k = db.get_team(db_game['_id'], 'team_2')
        l = db.get_team(db_game['_id'], 'neutral')

        embed.add_field(name='free players:', value=' '.join(f' <@{i}>' for i in db_game['initial_players']),
                        inline=False)
        embed.add_field(name="Red team:",
                        value=' '.join([f' <@{i}>' if len(j) > 0 else "." for i in j]), inline=False)
        embed.add_field(name="Blue team:",
                        value=' '.join([f' <@{i}>' if len(k) > 0 else "." for i in k]), inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="join",
                      usage='[game]',
                      description="join the 'waiting to be picked' list for a game")
    @commands.guild_only()
    @commands.has_permissions()
    async def join(self, ctx, game):
        db.add_start_player(game, ctx.message.author.id)
        game = db.get_game(game)

        embed = discord.Embed(title=f'{game["_id"]}')
        j = db.get_team(game["_id"], 'team_1')
        k = db.get_team(game["_id"], 'team_2')
        l = db.get_team(game["_id"], 'neutral')

        embed.add_field(name='free players:', value=' '.join(f' <@{i}>' for i in game['initial_players']), inline=False)
        embed.add_field(name="Red team:", value=' '.join([f' <@{i}>' if len(j) > 0 else "." for i in j]),
                        inline=False)
        embed.add_field(name="Blue team:", value=' '.join([f' <@{i}>' if len(k) > 0 else "." for i in k]),
                        inline=False)
        # embed.add_field(name="Neutral:", value=' '.join([f' <@{i}>' if len(l) > 0 else "." for i in l]),
        #                 inline=True)
        await ctx.send(embed=embed)

    @commands.command(name="neutral",
                      usage='{prefix}neutral [player] [game]',
                      description="as a host, choose a player for the neutral team")
    @commands.guild_only()
    @commands.has_permissions()
    async def neutral(self, ctx, player, game):
        try:
            team = db.get_captain_team(game, ctx.message.author.id)
            if team in ['team_1', 'team_2']:
                db.add_player(game, team, player.id)
                # guild = db.get_server(ctx.message.guild.id)
                # channel = self.bot.get_channel(guild[team])
                # await player.add_roles(ctx.message.guild.get_role(guild[f'{team}_role']))
                # await ctx.send(f"accepted <@{player.id}> on neutral, \
                #     moving <@{player.id}> to <#{channel.id}>")
                await ctx.send(f"accepted <@{player.id}> on neutral")

                db.add_player(game, team, player.id)

                players = db.get_initial_players(game)
                teamed_players = [j for i in db.get_all_teamed_players(game) for j in i]
                [players.remove(i) if i in players else None for i in teamed_players]

                embed = discord.Embed(title=f'{game}')
                j = db.get_team(game["_id"], 'team_1')
                k = db.get_team(game["_id"], 'team_2')
                l = db.get_team(game["_id"], 'neutral')

                embed.add_field(name='free players:', value=' '.join(f' <@{i}>' for i in game['initial_players']),
                                inline=False)
                embed.add_field(name="Red team:", value=' '.join([f' <@{i}>' if len(j) > 0 else "." for i in j]),
                                inline=False)
                embed.add_field(name="Blue team:", value=' '.join([f' <@{i}>' if len(k) > 0 else "." for i in k]),
                                inline=False)
                # embed.add_field(name="Neutral:", value=' '.join([f' <@{i}>' if len(l) > 0 else "." for i in l]),
                #                 inline=True)
                await ctx.send(embed=embed)
                # await player.move_to(channel)
            else:
                await ctx.send(f'you are not a captain in the game you mentioned.')
        except Exception as e:
            await ctx.send(e)

    # @tasks.loop(minutes=1)
    # async def gc(self):
    #     try:
    #         now = time.time()
    #         games = db.get_all_games()
    #         for game in games:
    #             if now - game['current_time'] > 28_000:
    #                 guild = self.bot.get_guild(game['guild'])
    #                 await guild.get_member(game['host']).remove_roles(guild.get_role([f'gamemaster_role']))
    #                 for player in db.get_all_teamed_players(game['_id']):
    #                     team = db.get_player_team(game['_id'], player)
    #                     await guild.get_member(player).remove_roles(guild.get_role([f'{team}_role']))
    #                 # db.delete_game(game['_id'])
    #     except Exception as e:
    #         print(e)


def setup(bot: commands.Bot):
    bot.add_cog(NewGame(bot))
