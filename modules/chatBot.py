import requests
import os
from datetime import datetime
import time
import random
from multiprocessing import Process, Lock, Value, Manager
import uuid

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


def sendMessage(accountToken, channelLink, previousMessage, ifReply, username, proxy, nonce=str(uuid.uuid4().time)):
    guildID = channelLink.split('/')[-2]
    channelID = channelLink.split('/')[-1]
    if ifReply == "Y":
        data = {
            'allowed_mentions': {'parse': ["users", "roles", "everyone"], 'replied_user': False},
            'parse': ["users", "roles", "everyone"],
            'replied_user': False,
            'content': previousMessage["answer"],
            'tts': False,
            'message_reference': {
                'channel_id': channelID,
                'guild_id': guildID,
                'message_id': previousMessage["message_id"]
            }
        }
    elif ifReply == "N":
        data = {
            'content': previousMessage["answer"],
            'tts': False,
            'nonce': nonce
        }
    elif ifReply == "RANDOM":
        randomBool = bool(random.getrandbits(1))
        if randomBool:
            data = {
                'allowed_mentions': {'parse': ["users", "roles", "everyone"], 'replied_user': False},
                'parse': ["users", "roles", "everyone"],
                'replied_user': False,
                'content': previousMessage["answer"],
                'tts': False,
                'message_reference': {
                    'channel_id': channelID,
                    'guild_id': guildID,
                    'message_id': previousMessage["message_id"]
                }
            }
        else:
            data = {
                'content': previousMessage["answer"],
                'tts': False,
                'nonce': nonce
            }
    else:
        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '{} | Wrong reply choice, restart task'.format(username))
        return {'channel_id': None, 'message_id': None}

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
            }, json=data)
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
            }, json=data, proxies={"https":"https://" + proxy})
    except Exception as e:
        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '{} | Something went wrong while sending message (Request)'.format(username))
        print(e)
        return {'channel_id': None, 'message_id': None}
    if r.status_code == 200:
        r = r.json()
        if r["content"] == previousMessage["answer"]:
            print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '{} | Successfully sent message: {}'.format(username, previousMessage["answer"]))
            return {'channel_id': r["channel_id"], 'message_id': r["id"]}
        else:
            print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '{} | Something went wrong while sending message (???)'.format(username))
            return {'channel_id': None, 'message_id': None}
    else:
        try:
            r = r.json()
        except:
            print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '{} | Something went wrong while sending message (Account/Server)'.format(username))
            print(r.text)
            return {'channel_id': None, 'message_id': None}
        if r["code"] == 20028:
            print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '{} | Channel rate limit, waiting {}s'.format(username, r["retry_after"]))
            if r["retry_after"] > 1:
                r["retry_after"] -= 0.3
            time.sleep(r["retry_after"])
            return sendMessage(accountToken, channelLink, previousMessage, ifReply, username, proxy, nonce)
        elif r["code"] == 20016:
            print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '{} | Slowmode rate limit, waiting {}s'.format(username, r["retry_after"]))
            time.sleep(r["retry_after"]+1)
            return sendMessage(accountToken, channelLink, previousMessage, ifReply, username, proxy, nonce)
        else:
            print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '{} | Something went wrong while sending message (Account/Server)'.format(username))
            print(r)
            return {'channel_id': None, 'message_id': None}

def getPreviousMessages(accountToken, channelLink, username, proxy):
    channelID = channelLink.split('/')[-1]
    try:
        if proxy == None:
            r = requests.get("https://discord.com/api/v9/channels/{}/messages".format(channelID), headers={
                'accept': '*/*',
                'authorization': accountToken,
                'cookie': 'locale=ru',
                'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
            })
        else:
            r = requests.get("https://discord.com/api/v9/channels/{}/messages".format(channelID), headers={
                'accept': '*/*',
                'authorization': accountToken,
                'cookie': 'locale=ru',
                'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
            }, proxies={"https":"https://" + proxy})
    except Exception as e:
        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '{} | Something went wrong while getting prev. message (Request)'.format(username))
        print(e)
        return {'previous_message': '', 'message_id': None, 'author': None, 'author_id': None, 'referenced_message': None}
    if r.status_code == 200:
        r = r.json()[0]
        referencedMessage = r.get("referenced_message", {"content": ""})
        if referencedMessage != None:
            referencedMessage = r.get("referenced_message", {"content": ""})["content"]
        else:
            referencedMessage = ""
        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '{} | Successfully got last message: {}'.format(username, r["content"]))
        return {'previous_message': r["content"], 'message_id': r["id"], 'author': r["author"]["username"], 'author_id': r["author"]["id"], 'referenced_message': referencedMessage}
    else:
        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '{} | Something went wrong while getting prev. message (Account/Server)'.format(username))
        print(r.text)
        return {'previous_message': '', 'message_id': None, 'author': None, 'author_id': None, 'referenced_message': None}

def sendTyping(accountToken, channelLink, proxy):
    channelID = channelLink.split('/')[-1]
    try:
        if proxy == None:
            requests.post("https://discord.com/api/v9/channels/{}/typing".format(channelID), headers={
                'accept': '*/*',
                'authorization': accountToken,
                'cookie': 'locale=ru',
                'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
            })
        else:
            requests.post("https://discord.com/api/v9/channels/{}/typing".format(channelID), headers={
                'accept': '*/*',
                'authorization': accountToken,
                'cookie': 'locale=ru',
                'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
            }, proxies={"https":"https://" + proxy})
    except Exception as e:
        pass

def generateAnswer(username, mainMessage, mainMessageAnswer, mainMessageAuthor, mainMessageAnswerAuthor, languageChoice):
    data = {
        'request': mainMessageAnswer,
        'request_1': '',
        'answer_1': mainMessage,
        'request_2':'',
        'answer_2':'',
        'request_3':'',
        'answer_3': '',
        'bot_name': mainMessageAuthor,
        'user_name': mainMessageAnswerAuthor,
        'dialog_lang': languageChoice,
        'dialog_greeting': 'false',
        **requests.get("https://sresellera.ru/2.0/trm/pbot/", verify=False).json()["data"]
    }
    try:
        r = requests.post("http://p-bot.ru/api/getAnswer", headers={
            'accept': '*/*',
            'content-type': 'application/x-www-form-urlencoded',
            'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'origin': 'http://p-bot.ru',
            'referer': 'http://p-bot.ru/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
            'cookie': 'dialog_id={};'.format(data["dialog_id"])
        }, data=data).json()
    except Exception as e:
        return {'answer': None }
    if r["answer"] != "" and r.get("pattern", {"answerNotFound": True}).get("answerNotFound", False) != True:
        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '{} | Successfully generated answer'.format(username))
        if r["answer"][-1] == ".":
            r["answer"] = r["answer"][:-1]
        return {'answer': r["answer"].replace('pBot', '...').capitalize() }
    else:
        return {'answer': None }
    

def deleteMessage(accountToken, messageData, username, proxy):
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
            print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '{} | Something went wrong while deleting (Request)'.format(username))
            print(e)
            return messageData
        if r.status_code == 204:
            print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '{} | Successfully deleted message'.format(username))
            return {'channel_id': None, 'message_id': None}
        if r.status_code == 429:
            try:
                r = r.json()
            except:
                print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '{} | Something went wrong while deleting (Account/Server)'.format(username))
                print(r.text)
                return {'channel_id': None, 'message_id': None}
            if r["code"] == 20028:
                print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '{} | Channel rate limit, waiting {}s'.format(username, r["retry_after"]))
                if r["retry_after"] > 1:
                    r["retry_after"] -= 0.3
                time.sleep(r["retry_after"])
                return deleteMessage(accountToken, messageData, username, proxy)
        else:
            print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '{} | Something went wrong while deleting (Account/Server)'.format(username))
            print(r.text)
            return messageData

def getDiscordProfile(accountToken, proxy):
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
        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '..{} | Something went wrong (Request)'.format(accountToken[-10:]))
        print(e)
        return {'username': None, 'id': None}
    if r.status_code == 200:
        r = r.json()
        return {'username': r["username"], 'id': r["id"]}
    else:
        return {'username': None, 'id': None}

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
    tasks = ['send']
    tasksConfig = {"delete":{}, "send":{}}
    printTRM()

    profile = loadProfile()

    tasksConfig["delete"]["delay"] = 0
    if ((input('Delete messages? Type Y/N\n>>> \033[94m')).upper() == "Y"):
        print('\033[0m', end='')
        tasks.append('delete')
        tasksConfig["delete"]["delay"] = int(input('  Delete delay (ms)\n  >>> \033[94m'))
    print('\033[0m', end='')

    os.system('cls' if os.name == 'nt' else 'clear')
    printTRM()

    tasksConfig["send"]["channel_link"] = input('Channel link\n>>> \033[94m')
    print('\033[0m', end='')

    tasksConfig["send"]["reply"] = (input('Reply to messages? Type RANDOM/Y/N\n>>> \033[94m')).upper()
    print('\033[0m', end='')

    print('Choose language:')
    print('   (\033[91m1\033[0m) Russian')
    print('   (\033[91m2\033[0m) English')
    languageChoice = ['ru', 'en'][int(input('>>> \033[94m'))-1]
    print('\033[0m', end='')

    tasksConfig["send"]["delay"] = int(input('Enter delay (ms)\n>>> \033[94m')) - tasksConfig["delete"]["delay"]
    print('\033[0m', end='')
    if tasksConfig["send"]["delay"] < 0:
        tasksConfig["send"]["delay"] = 0
    os.system('cls' if os.name == 'nt' else 'clear')
    printTRM()

    print('   Tokens list:', '\033[94m{}\033[0m'.format(profile["tokensListName"]))
    print('   Proxies list:', '\033[94m{}\033[0m'.format(profile["proxiesListName"]))
    print('   Channel:', '\033[94m/{}/{}\033[0m'.format(tasksConfig["send"]["channel_link"].split('/')[-2], tasksConfig["send"]["channel_link"].split('/')[-1]))
    print('   Tasks:', '\033[94m{}\033[0m'.format(', '.join(tasks).replace('send', 'Send messages').replace('delete', 'Delete messages').replace('rnd', 'Random message choice')), '\n')

    channelCheck = getChannel(profile["tokensList"][0], tasksConfig["send"]["channel_link"])
    if channelCheck != None:
        os.system("title TheRealMal AIO v{} : {}".format(version, channelCheck))

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

    with open(os.path.join('sites', 'discord', 'deleteKeywords.txt'), 'r') as f:
        profile["deleteKeywords"] = f.read().splitlines()
    tasksData = {}
    while True:
        if "send" in tasks:
            for token in profile["tokensList"]:
                flag = 1
                while flag:
                    previousMessage = {'previous_message': '', 'message_id': None, 'author': None, 'author_id': None, 'referenced_message': None, 'answer': None}
                    previousMessage = getPreviousMessages(token, tasksConfig["send"]["channel_link"], profile["tokens_users"][token]["username"], profile["tokens_proxies"][token])
                    if previousMessage["previous_message"] != "" and profile["tokens_users"][token]["id"] != previousMessage["author_id"]:
                        sendTyping(token, tasksConfig["send"]["channel_link"], profile["tokens_proxies"][token])
                        previousMessage["answer"] = generateAnswer(profile["tokens_users"][token]["username"], previousMessage["referenced_message"], previousMessage["previous_message"], profile["tokens_users"][token]["username"], previousMessage["author"], languageChoice)["answer"]
                        if previousMessage["answer"] != "" and previousMessage["answer"] != None:
                            for deleteKeyword in profile["deleteKeywords"]:
                                if deleteKeyword in previousMessage["answer"]:
                                    flag = 2
                                    break
                            if flag == 2:
                                flag = 1
                                print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '{} | Found negative keyword, retrying'.format(profile["tokens_users"][token]["username"]))
                                continue
                            else:
                                flag = 0
                            time.sleep(random.randint(0,1000)/1000)
                            tasksData[token] = sendMessage(token, tasksConfig["send"]["channel_link"], previousMessage, tasksConfig["send"]["reply"], profile["tokens_users"][token]["username"], profile["tokens_proxies"][token])
                            if tasksData[token]["message_id"] == None:
                                flag = 1
                        else:
                            print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '{} | Failed to generate answer'.format(profile["tokens_users"][token]["username"]))
                            tasksData[token] = {'channel_id': None, 'message_id': None}
                        time.sleep(random.randint(0,1000)/1000)
                    elif profile["tokens_users"][token]["id"] == previousMessage["author_id"]:
                        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '{} | Last message is your, waiting...'.format(profile["tokens_users"][token]["username"]))
                        tasksData[token] = {'channel_id': None, 'message_id': None}
                    else:
                        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '{} | Last message is empty, waiting...'.format(profile["tokens_users"][token]["username"]))
                        tasksData[token] = {'channel_id': None, 'message_id': None}
                if len(profile["tokensList"]) > 1:
                    time.sleep(random.randint(1000,2000)/1000)
        if "delete" in tasks:
            time.sleep(tasksConfig["delete"]["delay"]/1000)
            for token in profile["tokensList"]:
                tasksData[token] = deleteMessage(token, tasksData[token], profile["tokens_users"][token]["username"], profile["tokens_proxies"][token])
        time.sleep(tasksConfig["send"]["delay"]/1000)
    input('Press Enter to continue. . .')