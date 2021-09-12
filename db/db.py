from discord import player
import pymongo
import time

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['stellaris-red-vs-blue']
server_col = db['servers']
game_col = db['games']


# def setup_server(serverid, gather_spot, team_1, team_1_role, team_2, team_2_role, neutral, neutral_role, gm_role):
#     server_col.insert_one(
#         {
#             '_id': serverid,
#             'gathering_spot': gather_spot,
#             'team_1': team_1,
#             'team_1_role': team_1_role,
#             'team_2': team_2,
#             'team_2_role': team_2_role,
#             'neutral': neutral,
#             'neutral_role': neutral_role,
#             'gamemaster_role': gm_role
#         })

def setup_server(serverid, gather_spot):
    server_col.insert_one(
        {
            '_id': serverid,
            'gathering_spot': gather_spot
        })


def get_server(serverid):
    return server_col.find_one({'_id': serverid})


def delete_game(msgid):
    game_col.delete_one({'_id': msgid})


def new_game(msgid, guild, host, captain_1, captain_2, starting_players):
    game_col.insert_one({'_id': msgid,
                         'guild': guild,
                         'host': host,
                         'current_time': time.time(),
                         'initial_players': starting_players,
                         'teams': [
                             {
                                 'name': 'team_1',
                                 'captain': captain_1,
                                 'players': [captain_1]
                             }, {
                                 'name': 'team_2',
                                 'captain': captain_2,
                                 'players': [captain_2]
                             },
                             {
                                 'name': 'neutral',
                                 'players': []
                             }],
                         })
    # add_player(msgid, 'team_1', captain_1)
    # add_player(msgid, 'team_2', captain_2)


def add_player(msgid, team, player):
    game_col.update_one({'_id': msgid, 'teams.name': team
                         },
                        {
                            '$push': {
                                'teams.$.players': player
                            }
                        })


def remove_player(msgid, team, player):
    game_col.update_one({'_id': msgid, 'teams.name': team
                         },
                        {
                            '$pull': {
                                'teams.$.players': player
                            }
                        })


def remove_start_player(msgid, player):
    game_col.update_one({'_id': msgid
                         },
                        {
                            '$pull': {
                                'initial_players': player
                            }
                        })


def add_start_player(msgid, player):
    game_col.update_one({'_id': msgid
                         },
                        {
                            '$push': {
                                'initial_players': player
                            }
                        })


def get_host(msgid):
    a = game_col.find_one({'_id': msgid})
    return a['host']


def get_initial_players(msgid):
    a = game_col.find_one({'_id': msgid})
    return a['initial_players']


def get_all_teamed_players(msgid):
    a = game_col.find_one({'_id': msgid}, {'teams.players': 1})
    return [i['players'] for i in a['teams']]


def get_game(msgid):
    a = game_col.find({'_id': msgid})
    for i in a:
        return i


# def get_player_team(msgid, player):
#

def get_player_team(msgid, player):
    b = game_col.find_one({'_id': msgid})
    
    for team in b['teams']:
        if player in team['players']:
            return team['name']
    
    # b = game_col.aggregate([
    #     {
    #         '$match': {
    #             '_id': msgid
    #         }
    #     },
    #     {
    #         '$replaceRoot': {
    #             'newRoot': {
    #                 '$first': {
    #                     '$filter': {
    #                         'input': '$teams',
    #                         'as': 'team',
    #                         'cond': {
    #                             '$in': [
    #                                 player,
    #                                 '$$team.players'
    #                             ]
    #                         }
    #                     }
    #                 }
    #             }
    #         }
    #     }
    # ])
    # for i in b:
    #     return i['name']


def get_team(msgid, team):
    a = game_col.find_one({'_id': msgid})
    return ([t['players'] for t in a['teams'] if t['name'] == team] or [None])[0]


def get_captain_team(msgid, captain):
    b = game_col.aggregate([
        {
            '$match': {
                '_id': msgid
            }
        },
        {
            '$replaceRoot': {
                'newRoot': {
                    '$first': {
                        '$filter': {
                            'input': '$teams',
                            'as': 'team',
                            'cond': {
                                '$eq': [
                                    '$$team.captain',
                                    captain
                                ]
                            }
                        }
                    }
                }
            }
        }
    ])
    for i in b:
        return i['name']


def get_all_games():
    return [i for i in game_col.find({})]

def test():
    game = "222"
    print(get_player_team(game, 703199010315305000))

test()
