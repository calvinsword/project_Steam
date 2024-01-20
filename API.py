import requests

# Steam API
"""KEY IS: 7D0FF89CE8B73A585A3265963AE39708 -- 76561199005826631"""
"""Breid het dashboard uit met functionaliteit die de data live uit de Steam API haalt
in plaats van uit het bronbestand
(bij voorkeur zo gestructureerd dat er géén code tussen functies is gekopieerd)."""

APIKEY = '7D0FF89CE8B73A585A3265963AE39708'
STEAMID = '76561199040506358'
LINK = 'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=' + APIKEY + '&steamid=' + STEAMID + '&relationship=friend'

friendlist = requests.get(LINK).json()['friendslist']['friends']

steamidlist = []
for i in range(len(friendlist)):
    steamidlist.append(friendlist[i]['steamid'])

joinedsids = ','.join(steamidlist)


def printFriendInfo(ids):
    players_info = []
    useruri = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=' + APIKEY + '&steamids=' + ids
    userget = requests.get(useruri).json()['response']
    for i in range(10):
        players_info.append(userget['players'][i])
    return players_info


def printOnlineFriends(ids):
    useruri = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=' + APIKEY + '&steamids=' + ids
    userget = requests.get(useruri).json()['response']

    online_friends = []
    onlineDict = {}
    maxnamelen = 0

    players = userget.get('players', [])

    for player in players:
        tonli = player.get('personastate', 0)

        if tonli == 1:
            if 'gameextrainfo' in player:
                sname = player['personaname']
                sgame = player['gameextrainfo']
                onlineDict.update({sname: sgame})
                friend_name_game = (sname + " " + sgame)
                if len(sname) > maxnamelen:
                    maxnamelen = len(sname)
                online_friends.append(friend_name_game)

    if not onlineDict:
        return ["None of your friends are currently playing a game."]
    else:
        result_list = []
        sortDict = sorted(onlineDict.items(), key=lambda z: z[1])
        for i in sorted(onlineDict.keys()):
            tspaces = " " * (maxnamelen - len(i) + 2)
            result_list.append(f"{i}{tspaces}[{onlineDict[i]}]")
        return result_list

printOnlineFriends(joinedsids)

# Sorteren


# zoeken


# sorteren geavanceerd


#  zoeken Geavanceerd


# grafieken/diagrammen


# normaalverdeling
