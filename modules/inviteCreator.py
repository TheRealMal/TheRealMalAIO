import requests
import os
from datetime import datetime
import time
import random

def createInvite(accountToken, channelLink, proxy):
    channelID = channelLink.split('/')[-1]
    try:
        if proxy == None:
            r = requests.post("https://discord.com/api/v9/channels/{}/invites".format(channelID), headers={
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
            r = requests.post("https://discord.com/api/v9/channels/{}/invites".format(channelID), headers={
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
        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '..{} | Unable to create invite (Request)'.format(accountToken[-10:]))
        print(e)
        return {'success': False}
    if r.status_code == 200:
        r = r.json()
        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '..{} | Successfully created invite: {}'.format(accountToken[-10:], r["code"]))
        return {'success': True, 'inviteCode': r["code"]}
    else:
        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '..{} | Unable to create invite (Limit)'.format(accountToken[-10:]))
        return {'success': False}

def appendNewInvite(accountToken, invite):
    with open(os.path.join('sites', 'discord', 'invites.txt'), 'a') as f:
        f.write("{} | https://discord.gg/{}\n".format(accountToken, invite))

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

def main():
    tasks = ["createInvite"]
    tasksConfig = {"createInvite":{}}
    printTRM()

    profile = loadProfile()

    tasksConfig["createInvite"]["channel_link"] = input('Channel link\n>>> \033[94m')
    print('\033[0m', end='')

    tasksConfig["createInvite"]["delay"] = int(input('Enter delay (ms)\n>>> \033[94m'))
    print('\033[0m', end='')

    os.system('cls' if os.name == 'nt' else 'clear')
    printTRM()

    print('   Tokens list:', '\033[94m{}\033[0m'.format(profile["tokensListName"]))
    print('   Proxies list:', '\033[94m{}\033[0m'.format(profile["proxiesListName"]))
    print('   Channel:', '\033[94m/{}/{}\033[0m'.format(tasksConfig["createInvite"]["channel_link"].split('/')[-2], tasksConfig["createInvite"]["channel_link"].split('/')[-1]))
    print('   Tasks:', '\033[94m{}\033[0m'.format(', '.join(tasks).replace('createInvite', 'Create invite')), '\n')
    print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), 'Starting task')

    profile["tokens_proxies"] = {}
    profile["tokens_success"] = {}
    for token in profile["tokensList"]:
        if len(profile["proxiesList"]) != 0:
            profile["tokens_proxies"][token] = profile["proxiesList"][random.randint(0,len(profile["proxiesList"])-1)]
        else:
            profile["tokens_proxies"][token] = None
        profile["tokens_success"][token] = {'success': False}

    if "createInvite" in tasks:
        while len(profile["tokensList"]) != 0:
            for token in profile["tokensList"]:
                profile["tokens_success"][token] = createInvite(token, tasksConfig["createInvite"]["channel_link"], profile["tokens_proxies"][token])
                if profile["tokens_success"][token]["success"]:
                    appendNewInvite(token, profile["tokens_success"][token]["inviteCode"])
                    del profile["tokens_success"][token]
                    del profile["tokens_proxies"][token]
                    profile["tokensList"].remove(token)
                time.sleep(tasksConfig["createInvite"]["delay"]/1000)
    input('Press Enter to continue. . .')