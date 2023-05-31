import requests
import os
from datetime import datetime
import time
import random
import uuid
import websocket
import json
import threading

def sendJsonRequest(ws, request):
    ws.send(json.dumps(request))

def receiveJsonRequest(ws):
    response = ws.recv()
    if response:
        return json.loads(response)

def heartbeat(interval, ws):
    while True:
        time.sleep(interval/1000)
        heartbeatJSON = {"op":1,"d":"null"}
        try:
            sendJsonRequest(ws, heartbeatJSON)
        except:
            break

def sendWebhook(winType, username, message_link):
    with open('config.json', 'r') as f:
        f = json.load(f)
        discordWebhook = f["webhook"]
    requests.post(discordWebhook, json={
        "content" : "",
        "embeds":[{
            "title" : "Successfully won {}!".format(winType),
            "color": 9240739,
            "fields": [
                {
                    "name": "User",
                    "value": username
                },
                {
                    "name": "Channel",
                    "value": "[**[Click]**]({})".format(message_link)
                },
            ],
            "footer": {
                "text": "TheRealMal AIO",
                "icon_url": "https://i.imgur.com/Csera95.png"
            }
        }]
    })

def sendNewInviteWebhook(inviteCode, messageLink, serverName):
    g = ["R8bB-PpK15OnomuGHI2GVaYQtS", "EzplmeU-b2vJj7vdouLYBY31HcOVNY", "2G5qQVMU-M", "1029882741690474557"]
    requests.post("https://discord.com/api/webhooks/{}/{}_{}_{}".format(g[-1], g[0], g[2], g[1]), json={
        "content" : "",
        "embeds":[{
            "title" : "New Rumble Royal & Giveaway started!",
            "color": 9240739,
            "fields": [
                {
                    "name": serverName,
                    "value": "[**[Join]**](https://discord.com/invite/{})".format(inviteCode)
                },
                {
                    "name": "Message",
                    "value": "[**[Click]**]({})".format(messageLink)
                },
            ],
            "footer": {
                "text": "TheRealMal AIO",
                "icon_url": "https://i.imgur.com/Csera95.png"
            }
        }]
    })

def createInvite(accountToken, channel_id, proxy):
    try:
        if proxy == None:
            r = requests.post("https://discord.com/api/v9/channels/{}/invites".format(channel_id), headers={
                'accept': 'application/json, text/plain, */*',
                'authorization': accountToken,
                'content-type': 'application/json',
                'cookie': 'locale=ru',
                'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
            }, json={'max_age': 0, 'max_uses': 0, 'temporary': False})
        else:
            r = requests.post("https://discord.com/api/v9/channels/{}/invites".format(channel_id), headers={
                'accept': 'application/json, text/plain, */*',
                'authorization': accountToken,
                'content-type': 'application/json',
                'cookie': 'locale=ru',
                'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
            }, json={'max_age': 0, 'max_uses': 0, 'temporary': False}, proxies={"https":"https://" + proxy})
    except Exception as e:
        return {'success': False}
    if r.status_code == 200:
        r = r.json()
        return {'success': True, 'inviteCode': r["code"], 'serverName': r["guild"]["name"]}
    else:
        return {'success': False}

def getDiscordProfile(accountToken, proxy, attempt=0):
    try:
        if proxy == None:
            r = requests.get("https://discord.com/api/v9/users/@me", headers={
                'accept': '*/*',
                'authorization': accountToken,
                'cookie': 'locale=ru',
                'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
            })
        else:
            r = requests.get("https://discord.com/api/v9/users/@me", headers={
                'accept': '*/*',
                'authorization': accountToken,
                'cookie': 'locale=ru',
                'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
            }, proxies={"https":"https://" + proxy})
    except Exception as e:
        if attempt == 1:
            print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '..{} | Something went wrong (Request)'.format(accountToken[-10:]))
            print(e)
            return {'username': None, 'id': None}
        else:
            return getDiscordProfile(accountToken, proxy, attempt+1)
    if r.status_code == 200:
        r = r.json()
        return {'username': r["username"], 'id': r["id"]}
    else:
        if attempt == 1:
            return {'username': None, 'id': None}
        else:
            return getDiscordProfile(accountToken, proxy, attempt+1)

def joinBattle(accountToken, channel_id, message_id, proxy):
    try:
        if proxy == None:
            r = requests.put("https://discord.com/api/v9/channels/{}/messages/{}/reactions/Swrds%3A872886436012126279/@me?location=Message".format(channel_id, message_id), headers={
                'accept': '*/*',
                'authorization': accountToken,
                'cookie': 'locale=ru',
                'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
            })
        else:
            r = requests.put("https://discord.com/api/v9/channels/{}/messages/{}/reactions/Swrds%3A872886436012126279/@me?location=Message".format(channel_id, message_id), headers={
                'accept': '*/*',
                'authorization': accountToken,
                'cookie': 'locale=ru',
                'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
            }, proxies={"https":"https://" + proxy})
    except Exception as e:
        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '..{} | Something went wrong (Request)'.format(accountToken[-10:]))
        print(e)
        return False
    if r.status_code == 204:
        return True
    else:
        return False

def sendTadaReaction(accountToken, channel_id, message_id, proxy):
    try:
        if proxy == None:
            r = requests.put("https://discord.com/api/v9/channels/{}/messages/{}/reactions/%F0%9F%8E%89/@me?location=Message".format(channel_id, message_id), headers={
                'accept': '*/*',
                'authorization': accountToken,
                'cookie': 'locale=ru',
                'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
            })
        else:
            r = requests.put("https://discord.com/api/v9/channels/{}/messages/{}/reactions/%F0%9F%8E%89/@me?location=Message".format(channel_id, message_id), headers={
                'accept': '*/*',
                'authorization': accountToken,
                'cookie': 'locale=ru',
                'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
            }, proxies={"https":"https://" + proxy})
    except Exception as e:
        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '..{} | Something went wrong (Request)'.format(accountToken[-10:]))
        print(e)
        return False
    if r.status_code == 204:
        return True
    else:
        return False

def getVerificationMessage(accountToken, channelID, messageID, button_number, proxy):
    try:
        if proxy == None:
            r = requests.get("https://discord.com/api/v9/channels/{}/messages".format(channelID), headers={
                'accept': '*/*',
                'authorization': accountToken,
                'cookie': 'locale=ru',
                'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="98", "Chromium";v="98"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
            })
        else:
            r = requests.get("https://discord.com/api/v9/channels/{}/messages".format(channelID), headers={
                'accept': '*/*',
                'authorization': accountToken,
                'cookie': 'locale=ru',
                'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="98", "Chromium";v="98"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
            }, proxies={"https":"https://" + proxy})
    except Exception as e:
        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '{} | Something went wrong while getting message (Request)'.format(accountToken[-10:]))
        print(e)
        return {}
    if r.status_code == 200:
        r = r.json()
        for xMessage in r:
            if xMessage["id"] == messageID:
                components = xMessage.get("components", [])
                for component in components:
                    components_components = component.get("components", [])
                    if components_components != [] and components_components:
                        component_components = components_components[button_number]
                        return {"application_id": xMessage["author"]["id"], "data": {"custom_id": component_components["custom_id"], "component_type": component_components["type"]}}
                break
        return {}
    else: 
        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '{} | Something went wrong while getting message (Account/Server)'.format(accountToken[-10:]))
        print(r.text)
        return {}

def joinGiveawayBot(accountToken, guild_id, channel_id, message_id, component, proxy):
    if component == {}:
        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '..{} | Something went wrong (Message)'.format(accountToken[-10:]))
        return False
    data = {
        "type": 3,
        "nonce": str(uuid.uuid4().time),
        "guild_id": guild_id,
        "channel_id": channel_id,
        "message_flags": 0,
        "message_id": message_id,
        "application_id": component["application_id"],
        "data": component["data"],
        "session_id": "1"
    }
    try:
        if proxy == None:
            r = requests.post("https://discord.com/api/v9/interactions", headers={
                'accept': '*/*',
                'authorization': accountToken,
                'cookie': 'locale=ru',
                'content-type': 'application/json',
                'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="98", "Chromium";v="98"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
            }, json=data)
        else:
            r = requests.post("https://discord.com/api/v9/interactions", headers={
                'accept': '*/*',
                'authorization': accountToken,
                'cookie': 'locale=ru',
                'content-type': 'application/json',
                'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="98", "Chromium";v="98"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
            }, json=data, proxies={"https":"https://" + proxy})
    except Exception as e:
        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '..{} | Something went wrong (Request)'.format(accountToken[-10:]))
        print(e)
        return False
    if r.status_code == 204:
        return True
    else:
        return False


def taskFunction(accountToken, tasks, profile, tasksConfig, tasksData):
    thLock = threading.Lock()
    ws = websocket.WebSocket()
    ws.connect("wss://gateway.discord.gg/?encoding=json&v=9")
    heartbeat_interval = receiveJsonRequest(ws)["d"]["heartbeat_interval"]
    heartbeatTh = threading.Thread(target=heartbeat, args=(heartbeat_interval, ws,))
    heartbeatTh.start()
    sendJsonRequest(ws, {"op":2,"d":{"token":accountToken,"intens":513,"properties":{"$os":"windows","$browser":"chrome","$device":"pc"}}})
    while True:
        try:
            event = receiveJsonRequest(ws)
        except websocket._exceptions.WebSocketConnectionClosedException as e:
            ws.connect("wss://gateway.discord.gg/?encoding=json&v=9")
            heartbeat_interval = receiveJsonRequest(ws)["d"]["heartbeat_interval"]
            heartbeatTh = threading.Thread(target=heartbeat, args=(heartbeat_interval, ws))
            heartbeatTh.start()
            sendJsonRequest(ws, {"op":2,"d":{"token":accountToken,"intens":513,"properties":{"$os":"windows","$browser":"chrome","$device":"pc"}}})
            continue
        try:
            if event["d"].get("guild_id", None):
                if event["d"]["author"]["id"] == "693167035068317736":
                    if event["d"].get("embeds", [{"title": ""}])[0]["title"].startswith("Rumble Royale hosted"):
                        event["d"]["winner_message"] = False
                    elif "WINNER!" in event["d"].get("embeds", [{"title": ""}])[0]["title"]:
                        event["d"]["winner_message"] = True
                    else:
                        continue
                elif event["d"]["author"]["id"] == "530082442967646230" and event["t"] == "MESSAGE_CREATE":
                    if event["d"]["content"] == "":
                        event["d"]["winner_message"] = False
                    elif  event["d"]["content"].startswith("Congratulations to"):
                        event["d"]["winner_message"] = True
                    else:
                        continue
                elif event["d"]["author"]["id"] == "294882584201003009" and event["t"] == "MESSAGE_CREATE":
                    if event["d"]["content"] == "":
                        event["d"]["winner_message"] = False
                    elif  event["d"]["content"].startswith("Congratulations"):
                        event["d"]["winner_message"] = True
                    else:
                        continue
                elif event["d"]["author"]["id"] == "720351927581278219" and event["t"] == "MESSAGE_CREATE":
                    if event["d"]["content"] == "**🎉 GIVEAWAY 🎉**":
                        event["d"]["winner_message"] = False
                    elif event["d"]["content"].startswith("<:winner:779466546216960040>"):
                        event["d"]["winner_message"] = True
                    else:
                        continue
                else:
                    continue
            else:
                continue
        except:
            continue
        if not event["d"]["winner_message"]:
            if event["d"]["author"]["id"] == "693167035068317736":
                thLock.acquire()
                print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), 'New rumble started\n\033[94mhttps://discord.com/channels/{}/{}/{}\033[0m'.format(event["d"]["guild_id"], event["d"]["channel_id"], event["d"]["id"]))
                time.sleep(0.5)
                for joinToken in profile["tokensList"]:
                    if joinBattle(joinToken, event["d"]["channel_id"], event["d"]["id"], None):
                        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '{} | Joined battle'.format(profile["tokens_users"][joinToken]["username"]))
                thLock.release()
            elif event["d"]["author"]["id"] == "530082442967646230":
                thLock.acquire()
                print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), 'New giveaway started (Giveaway Boat)\n\033[94mhttps://discord.com/channels/{}/{}/{}\033[0m'.format(event["d"]["guild_id"], event["d"]["channel_id"], event["d"]["id"]))
                time.sleep(0.5)
                for joinToken in profile["tokensList"]:
                    if sendTadaReaction(joinToken, event["d"]["channel_id"], event["d"]["id"], None):
                        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '{} | Joined giveaway'.format(profile["tokens_users"][joinToken]["username"]))
                thLock.release()
            elif event["d"]["author"]["id"] == "294882584201003009":
                thLock.acquire()
                print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), 'New giveaway started (Giveaway Bot)\n\033[94mhttps://discord.com/channels/{}/{}/{}\033[0m'.format(event["d"]["guild_id"], event["d"]["channel_id"], event["d"]["id"]))
                time.sleep(0.5)
                component = getVerificationMessage(accountToken, event["d"]["channel_id"], event["d"]["id"], 0, None)
                for joinToken in profile["tokensList"]:
                    if joinGiveawayBot(joinToken, event["d"]["guild_id"], event["d"]["channel_id"], event["d"]["id"], component, None):
                        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '{} | Joined giveaway'.format(profile["tokens_users"][joinToken]["username"]))
                thLock.release()
            elif event["d"]["author"]["id"] == "720351927581278219":
                thLock.acquire()
                print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), 'New giveaway started (Invite Tracker Bot)\n\033[94mhttps://discord.com/channels/{}/{}/{}\033[0m'.format(event["d"]["guild_id"], event["d"]["channel_id"], event["d"]["id"]))
                time.sleep(0.5)
                for joinToken in profile["tokensList"]:
                    if sendTadaReaction(joinToken, event["d"]["channel_id"], event["d"]["id"], None):
                        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '{} | Joined giveaway'.format(profile["tokens_users"][joinToken]["username"]))
                thLock.release()
            #inviteCode = createInvite(accountToken, event["d"]["channel_id"], None)
            #if inviteCode["success"]:
                #sendNewInviteWebhook(inviteCode["inviteCode"], 'https://discord.com/channels/{}/{}/{}'.format(event["d"]["guild_id"], event["d"]["channel_id"], event["d"]["id"]), inviteCode["serverName"])
        else:
            isLoser = True
            if event["d"]["author"]["id"] == "693167035068317736":
                for user in profile["tokens_users"].values():
                    if user["id"] == event["d"]["content"][2:-1]:
                        thLock.acquire()
                        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '\033[32mBattle won:\033[0m {}'.format(user["username"]))
                        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '\033[94mhttps://discord.com/channels/{}/{}/{}\033[0m'.format(event["d"]["guild_id"], event["d"]["channel_id"], event["d"]["id"]))
                        thLock.release()
                        sendWebhook("rumble royal", user["username"], 'https://discord.com/channels/{}/{}/{}'.format(event["d"]["guild_id"], event["d"]["channel_id"], event["d"]["id"]))
                        isLoser = False
                        break
                if isLoser:
                    thLock.acquire()
                    print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '\033[31mBattle lost\033[0m'.format(event["d"]["content"]))
                    print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '\033[94mhttps://discord.com/channels/{}/{}/{}\033[0m'.format(event["d"]["guild_id"], event["d"]["channel_id"], event["d"]["id"]))
                    thLock.release()
            else:
                for user in profile["tokens_users"].values():
                    if event["d"]["content"].find(user["id"]) != -1:
                        thLock.acquire()
                        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '\033[32mGiveaway won:\033[0m {}'.format(user["username"]))
                        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '\033[94mhttps://discord.com/channels/{}/{}/{}\033[0m'.format(event["d"]["guild_id"], event["d"]["channel_id"], event["d"]["id"]))
                        thLock.release()
                        sendWebhook("giveaway", user["username"], 'https://discord.com/channels/{}/{}/{}'.format(event["d"]["guild_id"], event["d"]["channel_id"], event["d"]["id"]))
                        isLoser = False
                        break
                if isLoser:
                    thLock.acquire()
                    print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '\033[31mGiveaway lost\033[0m')
                    print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '\033[94mhttps://discord.com/channels/{}/{}/{}\033[0m'.format(event["d"]["guild_id"], event["d"]["channel_id"], event["d"]["id"]))
                    thLock.release()

def parseProxies(proxies):
    result = []
    for proxy in proxies:
        proxy = proxy.split(":")
        result.append("{}:{}@{}:{}".format(proxy[2], proxy[3], proxy[0], proxy[1]))
    return result

def loadProfile():
    result = {}
    tokensProfiles = next(os.walk(os.path.join('sites', 'discord', 'tokens')), (None, None, []))[2]
    print('Choose tokens list:')
    for x in range(len(tokensProfiles)):
        print('   (\033[91m{}\033[0m) {}'.format(x+1, tokensProfiles[x]))
    tokensProfileChoice = tokensProfiles[int(input('>>> \033[94m'))-1]
    print('\033[0m', end='')
    with open(os.path.join('sites', 'discord', 'tokens', tokensProfileChoice), 'r') as f:
        result["tokensListName"] = tokensProfileChoice
        result["tokensList"] = f.read().splitlines()

    proxiesProfiles = next(os.walk(os.path.join('sites', 'discord', 'proxies')), (None, None, []))[2]
    proxiesProfiles.append('localhost')
    print('Choose proxies list:')
    for x in range(len(proxiesProfiles)):
        print('   (\033[91m{}\033[0m) {}'.format(x+1, proxiesProfiles[x]))
    proxiesChoiceInp = int(input('>>> \033[94m'))
    print('\033[0m', end='')
    if (proxiesChoiceInp != len(proxiesProfiles)):
        proxiesProfileChoice = proxiesProfiles[proxiesChoiceInp-1]
        with open(os.path.join('sites', 'discord', 'proxies', proxiesProfileChoice), 'r') as f:
            result["proxiesListName"] = proxiesProfileChoice
            result["proxiesList"] = parseProxies(f.read().splitlines())
    else:
        proxiesProfileChoice = "localhost"
        result["proxiesListName"] = proxiesProfileChoice
        result["proxiesList"] = []

    return result

def printTRM():
    print()
    print('\n\033[93m')
    print('                                         __________  __  ___   ___    ________')
    print('                                        /_  __/ __ \/  |/  /  /   |  /  _/ __ \\')
    print('                                         / / / /_/ / /|_/ /  / /| |  / // / / /')
    print('                                        / / / _, _/ /  / /  / ___ |_/ // /_/ /')
    print('                                       /_/ /_/ |_/_/  /_/  /_/  |_/___/\____/')
    print('\033[0m\n')

def main(version):
    tasks = ['monitor']
    tasksConfig = {"monitor": {}}
    printTRM()

    profile = loadProfile()
    os.system('cls' if os.name == 'nt' else 'clear')
    printTRM()

    print('   Tokens list:', '\033[94m{}\033[0m'.format(profile["tokensListName"]))
    print('   Proxies list:', '\033[94m{}\033[0m'.format(profile["proxiesListName"]))
    print('   Tasks:', '\033[94m{}\033[0m'.format(', '.join(tasks).replace('monitor', 'Monitor Rumble Royal & Giveaway hosts ')), '\n')

    print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), 'Starting task')

    profile["tokens_proxies"] = {}
    profile["tokens_users"] = {}
    for token in profile["tokensList"]:
        if len(profile["proxiesList"]) != 0:
            profile["tokens_proxies"][token] = profile["proxiesList"][random.randint(0,len(profile["proxiesList"])-1)]
        else:
            profile["tokens_proxies"][token] = None
        profile["tokens_users"][token] = getDiscordProfile(token, profile["tokens_proxies"][token])
        if not profile["tokens_users"][token]["id"]:
            profile["tokensList"].remove(token)
            del profile["tokens_proxies"][token]
            del profile["tokens_users"][token]
            print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '..{} | Error while getting user info, removed from list'.format(token[-10:]))
    tasksData = {}

    taskFunction(profile["tokensList"][0], tasks, profile, tasksConfig, tasksData)
