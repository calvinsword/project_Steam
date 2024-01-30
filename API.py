# Steam API
"""KEY IS: 7D0FF89CE8B73A585A3265963AE39708 -- 76561199005826631"""
"""Breid het dashboard uit met functionaliteit die de data live uit de Steam API haalt
in plaats van uit het bronbestand
(bij voorkeur zo gestructureerd dat er géén code tussen functies is gekopieerd)."""

import requests

APIKEY = '7D0FF89CE8B73A585A3265963AE39708'
STEAMID = '76561199040506358'


def printOnlineFriends(APIKEY, STEAMID):
    LINK = 'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=' + APIKEY + '&steamid=' + str(
        STEAMID) + '&relationship=friend'
    if requests.get(LINK).json() == {}:
        return False
    friendlist = requests.get(LINK).json()['friendslist']['friends']

    steamidlist = []
    for i in range(len(friendlist)):
        steamidlist.append(friendlist[i]['steamid'])

    joinedsids = ','.join(steamidlist)

    useruri = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=' + APIKEY + '&steamids=' + joinedsids
    userget = requests.get(useruri).json()['response']

    online_friends = []
    onlineDict = {}
    maxnamelen = 0

    players = userget.get('players', [])
    for player in players:
        if 'gameextrainfo' in player:
            sname = player['personaname']
            sgame = player['gameextrainfo']
            onlineDict.update({sname: sgame})
            friend_name_game = (sname + " " + sgame)
            if len(sname) > maxnamelen:
                maxnamelen = len(sname)
            online_friends.append(friend_name_game)

    if not onlineDict:
        return []
    else:
        result_list = []
        sortDict = sorted(onlineDict.items(), key=lambda z: z[1])
        for i in sorted(onlineDict.keys()):
            array = [i, onlineDict[i]]
            result_list.append(array)

        return result_list

printOnlineFriends(APIKEY, 76561199143747374)
