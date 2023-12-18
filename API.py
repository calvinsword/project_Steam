# Steam API
"""KEY IS: 7D0FF89CE8B73A585A3265963AE39708 -- 76561199005826631"""
"""Breid het dashboard uit met functionaliteit die de data live uit de Steam API haalt
in plaats van uit het bronbestand
(bij voorkeur zo gestructureerd dat er géén code tussen functies is gekopieerd)."""

import requests

APIKEY = '7D0FF89CE8B73A585A3265963AE39708'
STEAMID = '76561199040506358'
LINK = 'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=' + APIKEY + '&steamid=' + STEAMID + '&relationship=friend'


friendlist = requests.get(LINK).json()['friendslist']['friends']

steamidlist = []
for i in range(len(friendlist)):
    steamidlist.append(friendlist[i]['steamid'])


joinedsids = ','.join(steamidlist)



def printFriendInfo(ids):
    useruri = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=' + APIKEY + '&steamids=' + ids
    userget = requests.get(useruri).json()['response']
    for i in range(len(userget['players'])):
        print(userget['players'][i])



def printOnlineFriends(ids):
    useruri = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=' + APIKEY + '&steamids=' + ids
    userget = requests.get(useruri).json()['response']

    onlineDict = {}
    global maxnamelen
    maxnamelen = 0
    for i in range(len(userget['players'])):
        tonli = userget['players'][i]['personastate']
        if tonli == 1:

            if 'gameextrainfo' in userget['players'][i]:
                sname = userget['players'][i]['personaname']
                sgame = userget['players'][i]['gameextrainfo']
                onlineDict.update({sname: sgame})
                if len(sname) > maxnamelen:
                    maxnamelen = int(len(sname))

        else:

            continue
    if not onlineDict:
        print("None of your friends are currently playing a game.")
    else:
        sortDict = sorted(onlineDict.items(), key=lambda z: z[1])
        for i in sorted(onlineDict.keys()):

            tspaces = ""
            lennamediff = (maxnamelen - len(i)) + 2
            for x in range(lennamediff):
                tspaces += ' '
            print(i + tspaces, "[" + onlineDict[i] + "]")



printOnlineFriends(joinedsids)


# Sorteren


# zoeken


# sorteren geavanceerd


#  zoeken Geavanceerd


# grafieken/diagrammen


# normaalverdeling