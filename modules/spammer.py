import requests
import os
from datetime import datetime
import time
import random

def getChannel(accountToken, channelLink):
    try:
        channelID = channelLink.split('/')[-1]
        guildID = channelLink.split('/')[-2]
        guildName = requests.get("https://discord.com/api/v9/guilds/{}".format(guildID), headers={
            'accept': 'application/json, text/plain, */*',
            'authorization': accountToken,
            'content-type': 'application/json',
            'cookie': 'locale=ru',
            'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
        }).json()["name"]
        channelName = requests.get("https://discord.com/api/v9/channels/{}".format(channelID), headers={
            'accept': 'application/json, text/plain, */*',
            'authorization': accountToken,
            'content-type': 'application/json',
            'cookie': 'locale=ru',
            'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
        }).json()["name"]
        return "{} - #{}".format(guildName, channelName)
    except Exception as e:
        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), 'Something went wrong while getting channel')
        print(e)
        return None

def sendMessage(accountToken, channelLink, message, proxy):
    channelID = channelLink.split('/')[-1]
    try:
        if proxy == None:
            r = requests.post("https://discord.com/api/v9/channels/{}/messages".format(channelID), headers={
                'accept': 'application/json, text/plain, */*',
                'authorization': accountToken,
                'content-type': 'application/json',
                'cookie': 'locale=ru',
                'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
            }, json={'content': message, 'tts': False})
        else:
            r = requests.post("https://discord.com/api/v9/channels/{}/messages".format(channelID), headers={
                'accept': 'application/json, text/plain, */*',
                'authorization': accountToken,
                'content-type': 'application/json',
                'cookie': 'locale=ru',
                'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
            }, json={'content': message, 'tts': False}, proxies={"https":"https://" + proxy})
    except Exception as e:
        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '..{} | Something went wrong (Request)'.format(accountToken[-10:]))
        print(e)
        return {'channel_id': None, 'message_id': None}
    if r.status_code == 200:
        r = r.json()
        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '..{} | Successfully sent message: {}'.format(accountToken[-10:], message))
        return {'channel_id': r["channel_id"], 'message_id': r["id"]}
    else:
        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '..{} | Something went wrong (Account/Server)'.format(accountToken[-10:]))
        print(r.text)
        return {'channel_id': None, 'message_id': None}

def deleteMessage(accountToken, messageData, proxy):
    if messageData["channel_id"] and messageData["message_id"]:
        try:
            if proxy == None:
                r = requests.delete("https://discord.com/api/v9/channels/{}/messages/{}".format(messageData["channel_id"], messageData["message_id"]), headers={
                    'accept': '*/*',
                    'authorization': accountToken,
                    'cookie': 'locale=ru',
                    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
                })
            else:
                r = requests.delete("https://discord.com/api/v9/channels/{}/messages/{}".format(messageData["channel_id"], messageData["message_id"]), headers={
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
            return messageData
        if r.status_code == 204:
            print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '..{} | Successfully deleted message'.format(accountToken[-10:]))
            return {'channel_id': None, 'message_id': None}
        else:
            print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '..{} | Something went wrong (Account/Server)'.format(accountToken[-10:]))
            print(r.text)
            return messageData

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

    phrasesProfiles = next(os.walk(os.path.join('sites', 'discord', 'phrases')), (None, None, []))[2]
    print('Choose phrases list:')
    for x in range(len(phrasesProfiles)):
        print('   (\033[91m{}\033[0m) {}'.format(x+1, phrasesProfiles[x]))
    phrasesProfileChoice = phrasesProfiles[int(input('>>> \033[94m'))-1]
    print('\033[0m', end='')
    with open(os.path.join('sites', 'discord', 'phrases', phrasesProfileChoice), 'r') as f:
        result["phrasesListName"] = phrasesProfileChoice
        result["phrasesList"] = f.read().splitlines()

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
    tasks = ['send']
    tasksConfig = {"delete":{}, "send":{}, "rnd":{}}
    printTRM()

    profile = loadProfile()

    if ((input('Random message choice? Type Y/N\n>>> \033[94m')).upper() == "Y"):
        print('\033[0m', end='')
        tasks.append('rnd')
    print('\033[0m', end='')

    tasksConfig["delete"]["delay"] = 0
    if ((input('Delete messages? Type Y/N\n>>> \033[94m')).upper() == "Y"):
        print('\033[0m', end='')
        tasks.append('delete')
        tasksConfig["delete"]["delay"] = int(input('  Delete delay (ms)\n  >>> \033[94m'))
    print('\033[0m', end='')

    tasksConfig["send"]["channel_link"] = input('Channel link\n>>> \033[94m')
    print('\033[0m', end='')

    tasksConfig["send"]["delay"] = int(input('Enter delay (ms)\n>>> \033[94m')) - tasksConfig["delete"]["delay"]
    print('\033[0m', end='')
    if tasksConfig["send"]["delay"] < 0:
        tasksConfig["send"]["delay"] = 0

    os.system('cls' if os.name == 'nt' else 'clear')
    printTRM()

    print('   Tokens list:', '\033[94m{}\033[0m'.format(profile["tokensListName"]))
    print('   Proxies list:', '\033[94m{}\033[0m'.format(profile["proxiesListName"]))
    print('   Phrases list:', '\033[94m{}\033[0m'.format(profile["phrasesListName"]))
    print('   Channel:', '\033[94m/{}/{}\033[0m'.format(tasksConfig["send"]["channel_link"].split('/')[-2], tasksConfig["send"]["channel_link"].split('/')[-1]))
    print('   Tasks:', '\033[94m{}\033[0m'.format(', '.join(tasks).replace('send', 'Send messages').replace('delete', 'Delete messages').replace('rnd', 'Random message choice')), '\n')

    channelCheck = getChannel(profile["tokensList"][0], tasksConfig["send"]["channel_link"])
    if channelCheck != None:
        os.system("title TheRealMal AIO v{} : {}".format(version, channelCheck))

    print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), 'Starting task')

    profile["tokens_proxies"] = {}
    profile["tokens_phrases"] = {}
    for token in profile["tokensList"]:
        if len(profile["proxiesList"]) != 0:
            profile["tokens_proxies"][token] = profile["proxiesList"][random.randint(0,len(profile["proxiesList"])-1)]
        else:
            profile["tokens_proxies"][token] = None
        profile["tokens_phrases"][token] = profile["phrasesList"].copy()

    tasksData = {}
    while True:
        if "send" in tasks:
            for token in profile["tokensList"]:
                if len(profile["tokens_phrases"][token]) == 0:
                    profile["tokens_phrases"][token] = profile["phrasesList"].copy()
                phrase = random.choice(profile["tokens_phrases"][token])
                profile["tokens_phrases"][token].remove(phrase)
                time.sleep(random.randint(0,1000)/1000)
                tasksData[token] = sendMessage(token, tasksConfig["send"]["channel_link"], phrase, profile["tokens_proxies"][token])
        if "delete" in tasks:
            time.sleep(tasksConfig["delete"]["delay"]/1000)
            for token in profile["tokensList"]:
                tasksData[token] = deleteMessage(token, tasksData[token], profile["tokens_proxies"][token])
        time.sleep(tasksConfig["send"]["delay"]/1000)
    input('Press Enter to continue. . .')