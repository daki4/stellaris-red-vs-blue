import pymongo


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['stellaris-red-vs-blue']
server_col = db['servers']
game_col = db['games']


def setup_server(serverid, gather_spot, team_1, team_2, neutral):
    server_col.insert_one(
        {
            '_id': serverid,
            'gathering_spot': gather_spot,
            'team_1': team_1,
            'team_2': team_2,
            'neutral': neutral
        })


def get_server(serverid):
    return server_col.find_one({'_id': serverid})


def new_game(msgid, host, captain_1, captain_2, starting_players):
    game_col.insert_one({'_id': msgid,
                        'host': host,
                        'initial_players': starting_players,
                        'teams': [
                            {
                                'name': 'team_1',
                                'captain': captain_1,
                                'players': []
                            }, {
                                'name': 'team_2',
                                'captain': captain_2,
                                'players': []
                            },
                            {
                                'name': 'neutral',
                                'players': []
                            }],
                        })


def add_player(msgid, team, player):
    
    if team is None:
        game_col.update_one({'_id': msgid
                            },
                            {
                                'initial_players': {
                                    '$push': player
                                }
                            })
    else:
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
                                '$push': {
                                    'teams.$.players': player
                                }
                            })


def get_initial_players(msgid):
    a = game_col.find_one({'_id': msgid})
    return a['initial_players']


def get_player_team(msgid, player):
    try:
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
                                '$in': [
                                    player,
                                    '$$team.players'
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
    except Exception as e:
        print(e)

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
