import requests
import os
from datetime import datetime
import time
import random
import uuid
import json
import threading
from re import findall
from selenium import webdriver
from modules.captchaSolver import CaptchaSolver

sup_prop = 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6InJ1IiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzk4LjAuNDc1OC4xMDIgU2FmYXJpLzUzNy4zNiIsImJyb3dzZXJfdmVyc2lvbiI6Ijk4LjAuNDc1OC4xMDIiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6Imh0dHBzOi8vZGlzY29yZC5jb20vIiwicmVmZXJyaW5nX2RvbWFpbiI6ImRpc2NvcmQuY29tIiwicmVmZXJyZXJfY3VycmVudCI6Imh0dHBzOi8vZGlzY29yZC5jb20vIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiZGlzY29yZC5jb20iLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjoxMTY1MDYsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9'

def createDriver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--window-position=0,0')
    options.add_argument('--disable-setuid-sandbox')
    options.add_argument('--ignore-certifcate-errors')
    options.add_argument('--ignore-certifcate-errors-spki-list')
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36')
    options.add_experimental_option("excludeSwitches", ['enable-automation','disable-extensions','enable-logging'])
    options.add_experimental_option('prefs', {'profile.default_content_setting_values': {
        'cookies': 1, 'images': 2, 'javascript': 1, 
        'plugins': 2, 'popups': 2, 'geolocation': 2, 
        'notifications': 2, 'auto_select_certificate': 2, 'fullscreen': 2, 
        'mouselock': 2, 'mixed_script': 2, 'media_stream': 2, 
        'media_stream_mic': 2, 'media_stream_camera': 2, 'protocol_handlers': 2, 
        'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2, 
        'push_messaging': 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop': 2, 
        'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement': 2, 
        'durable_storage': 2}})
    driver = webdriver.Chrome(options=options)
    return driver

def joinServer_browser(thLock, driver, accountToken, inviteCode, proxy, captchaClientKey, captchaData={}):
    try:
        thLock.acquire()
        r = driver.execute_script('''
        return await new Promise(async (resolve) => {
            await fetch("https://discord.com/api/v9/invites/''' + inviteCode + '''", {
                body: JSON.stringify(JSON.parse(\'''' + str(captchaData).replace('\'','"') + '''\')),
                headers: {
                    'Authorization': \'''' + accountToken + '''\',
                    'Content-Type': 'application/json',
                    'x-super-properties': \'''' + sup_prop + '''\'
                },
                method: "POST"
            }).then(response => {
                return response.json();
            }).then(function(data) {
                data['ua'] = window.navigator.userAgent
                resolve(data)
            });
        })''')
        thLock.release()
    except Exception as e:
        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '..{} | Something went wrong (Request)'.format(accountToken[-10:]))
        print(e)
        return False
    if r.get("captcha_service", None) == None:
        thLock.acquire()
        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '..{} | Successfully joined'.format(accountToken[-10:]))
        thLock.release()
        return True
    else:
        try:
            if r.get("captcha_service", "") == "hcaptcha":
                if captchaClientKey != "":
                    print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '..{} | Solving HCaptcha'.format(accountToken[-10:]))
                    captchaResult = CaptchaSolver({
                        "accountToken": accountToken,
                        "captchaClientKey": captchaClientKey,
                        "websiteKey": r["captcha_sitekey"],
                        "rqData": r["captcha_rqdata"],
                        "ua": r["ua"]
                    }, "capmonster").solve()
                    if captchaResult.get("captcha_key", None):
                        captchaResult["captcha_rqtoken"] = r["captcha_rqtoken"]
                    print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '..{} | Got HCaptcha solution'.format(accountToken[-10:]))
                    return joinServer_browser(thLock, driver, accountToken, inviteCode, proxy, captchaClientKey, captchaResult)
                else:
                    input('Add capMonster site key to config.json and restart. . .')
                    return False
            else:
                print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '..{} | Something went wrong (Account)'.format(accountToken[-10:]))
                print(r)
                return False
        except Exception as e:
            print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '..{} | Something went wrong (Account)'.format(accountToken[-10:]))
            print(e)
            return False

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

def getPreviousMessages(accountToken, channelLink, username, proxy):
    channelID = channelLink.split('/')[-1]
    try:
        if proxy == None:
            r = requests.get("https://discord.com/api/v9/channels/{}/messages?limit=5".format(channelID), headers={
                'accept': '*/*',
                'authorization': accountToken,
                'cookie': 'locale=ru',
                'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
            })
        else:
            r = requests.get("https://discord.com/api/v9/channels/{}/messages?limit=5".format(channelID), headers={
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
        return []
    if r.status_code == 200:
        r = r.json()
        result = []
        for x in range(len(r)):
            result.append({'content': r[len(r)-1-x]["content"], 'id': r[len(r)-1-x]["id"]})
        return result
    else:
        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '{} | Something went wrong while getting prev. message (Account/Server)'.format(username))
        print(r.text)
        return []

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

def onMessage(driver, extractedInvites, tasks, profile, tasksConfig, tasksData):
    thLock = threading.Lock()
    if "join" in tasks:
        for inviteCode in extractedInvites:
            inviteCode = inviteCode.split('/')[-1]
            for accountToken in profile["joinTokensList"]:
                th = threading.Thread(target=joinServer_browser, args=(thLock, driver, accountToken, inviteCode, profile["join_tokens_proxies"][accountToken], profile["captchaClientKey"]))
                th.start()

def taskFunction(driver, accountToken, channelLink, tasks, profile, tasksConfig, tasksData):
    redeemedInvites = []
    currentLastMessages = []
    while True:
        try:
            msgs = getPreviousMessages(accountToken, channelLink, profile["monitoring_tokens_users"][accountToken]["username"], profile["monitoring_tokens_proxies"][accountToken])
        except:
            continue
        for msg in msgs:
            if msg["id"] not in redeemedInvites and msg["id"] not in currentLastMessages:
                currentLastMessages.insert(0, msg["id"])
                extractedInvites = [x for x in findall(r'(https?://\S+)', msg["content"]) if "discord." in x]
                if len(extractedInvites) > 0:
                    onMessage(driver, extractedInvites, tasks, profile, tasksConfig, tasksData)
                    print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '{} | Detected invites: \n{}'.format(profile["monitoring_tokens_users"][accountToken]["username"], "\n".join(extractedInvites)))
                    redeemedInvites.append(msg["id"])
        while len(currentLastMessages) > 5:
            currentLastMessages.pop()
        time.sleep(tasksConfig["join"]["monitoring_delay"])




def parseProxies(proxies):
    result = []
    for proxy in proxies:
        proxy = proxy.split(":")
        result.append("{}:{}@{}:{}".format(proxy[2], proxy[3], proxy[0], proxy[1]))
    return result

def loadProfile():
    result = {}
    tokensProfiles = next(os.walk(os.path.join('sites', 'discord', 'tokens')), (None, None, []))[2]
    print('Choose monitoring tokens list:')
    for x in range(len(tokensProfiles)):
        print('   (\033[91m{}\033[0m) {}'.format(x+1, tokensProfiles[x]))
    tokensProfileChoice = tokensProfiles[int(input('>>> \033[94m'))-1]
    print('\033[0m', end='')
    with open(os.path.join('sites', 'discord', 'tokens', tokensProfileChoice), 'r') as f:
        result["monitoringTokensListName"] = tokensProfileChoice
        result["monitoringTokensList"] = f.read().splitlines()

    print('Choose \'join\' tokens list:')
    for x in range(len(tokensProfiles)):
        print('   (\033[91m{}\033[0m) {}'.format(x+1, tokensProfiles[x]))
    tokensProfileChoice = tokensProfiles[int(input('>>> \033[94m'))-1]
    print('\033[0m', end='')
    with open(os.path.join('sites', 'discord', 'tokens', tokensProfileChoice), 'r') as f:
        result["joinTokensListName"] = tokensProfileChoice
        result["joinTokensList"] = f.read().splitlines()

    os.system('cls' if os.name == 'nt' else 'clear')
    printTRM()

    proxiesProfiles = next(os.walk(os.path.join('sites', 'discord', 'proxies')), (None, None, []))[2]
    proxiesProfiles.append('localhost')
    print('Choose monitoring proxies list:')
    for x in range(len(proxiesProfiles)):
        print('   (\033[91m{}\033[0m) {}'.format(x+1, proxiesProfiles[x]))
    proxiesChoiceInp = int(input('>>> \033[94m'))
    print('\033[0m', end='')
    if (proxiesChoiceInp != len(proxiesProfiles)):
        proxiesProfileChoice = proxiesProfiles[proxiesChoiceInp-1]
        with open(os.path.join('sites', 'discord', 'proxies', proxiesProfileChoice), 'r') as f:
            result["monitoringProxiesListName"] = proxiesProfileChoice
            result["monitoringProxiesList"] = parseProxies(f.read().splitlines())
    else:
        proxiesProfileChoice = "localhost"
        result["monitoringProxiesListName"] = proxiesProfileChoice
        result["monitoringProxiesList"] = []

    print('Choose \'join\' proxies list:')
    for x in range(len(proxiesProfiles)):
        print('   (\033[91m{}\033[0m) {}'.format(x+1, proxiesProfiles[x]))
    proxiesChoiceInp = int(input('>>> \033[94m'))
    print('\033[0m', end='')
    if (proxiesChoiceInp != len(proxiesProfiles)):
        proxiesProfileChoice = proxiesProfiles[proxiesChoiceInp-1]
        with open(os.path.join('sites', 'discord', 'proxies', proxiesProfileChoice), 'r') as f:
            result["joinProxiesListName"] = proxiesProfileChoice
            result["joinProxiesList"] = parseProxies(f.read().splitlines())
    else:
        proxiesProfileChoice = "localhost"
        result["joinProxiesListName"] = proxiesProfileChoice
        result["joinProxiesList"] = []
    with open(os.path.join('config.json'), 'r') as f:
        fJSON = json.load(f)
        result["captchaClientKey"] = fJSON.get("hcaptcha")
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
    tasks = ['join']
    tasksConfig = {"join":{}}
    printTRM()

    profile = loadProfile()

    os.system('cls' if os.name == 'nt' else 'clear')
    printTRM()

    tasksConfig["join"]["channel_link"] = input('Channel link\n>>> \033[94m')
    print('\033[0m', end='')

    tasksConfig["join"]["monitoring_delay"] = int(input('Monitoring delay\n>>> \033[94m'))/1000
    print('\033[0m', end='')

    os.system('cls' if os.name == 'nt' else 'clear')
    printTRM()

    print('   Monitoring | Join tokens list:', '\033[94m{} | {}\033[0m'.format(profile["monitoringTokensListName"], profile["joinTokensListName"]))
    print('   Monitoring | Join proxies list:', '\033[94m{} | {}\033[0m'.format(profile["monitoringProxiesListName"], profile["joinProxiesListName"]))
    print('   Channel:', '\033[94m/{}/{}\033[0m'.format(tasksConfig["join"]["channel_link"].split('/')[-2], tasksConfig["join"]["channel_link"].split('/')[-1]))
    print('   Tasks:', '\033[94m{}\033[0m'.format(', '.join(tasks).replace('join', 'Monitor channel and join invites')), '\n')

    channelCheck = getChannel(profile["monitoringTokensList"][0], tasksConfig["join"]["channel_link"])
    if channelCheck != None:
        os.system("title TheRealMal AIO v{} : {}".format(version, channelCheck))

    profile["monitoring_tokens_proxies"] = {}
    profile["monitoring_tokens_users"] = {}
    for token in profile["monitoringTokensList"]:
        if len(profile["monitoringProxiesList"]) != 0:
            profile["monitoring_tokens_proxies"][token] = profile["monitoringProxiesList"][random.randint(0,len(profile["monitoringProxiesList"])-1)]
        else:
            profile["monitoring_tokens_proxies"][token] = None
        profile["monitoring_tokens_users"][token] = getDiscordProfile(token, profile["monitoring_tokens_proxies"][token])
        if not profile["monitoring_tokens_users"][token]["id"]:
            profile["monitoringTokensList"].remove(token)
            del profile["monitoring_tokens_proxies"][token]
            del profile["monitoring_tokens_users"][token]
            print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '..{} | Error while getting user info, removed from list'.format(token[-10:]))
    
    profile["join_tokens_proxies"] = {}
    profile["join_tokens_users"] = {}
    for token in profile["joinTokensList"]:
        if len(profile["joinProxiesList"]) != 0:
            profile["join_tokens_proxies"][token] = profile["joinProxiesList"][random.randint(0,len(profile["joinProxiesList"])-1)]
        else:
            profile["join_tokens_proxies"][token] = None
        profile["join_tokens_users"][token] = getDiscordProfile(token, profile["join_tokens_proxies"][token])
        if not profile["join_tokens_users"][token]["id"]:
            profile["joinTokensList"].remove(token)
            del profile["join_tokens_proxies"][token]
            del profile["join_tokens_users"][token]
            print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '..{} | Error while getting user info, removed from list'.format(token[-10:]))

    tasksData = {}

    print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), 'Starting task')
    driver = createDriver()
    driver.get("https://discord.com/")
    driver.execute_script('''let token = \''''+profile["joinTokensList"][0]+'''\'; function login(token){setInterval(() => {document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"${token}"`}, 50); setTimeout(() => {location.reload();}, 2500);}login(token);''')
    driver.get("https://discord.com/app")
    time.sleep(3)

    print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), 'Monitoring channel')

    taskFunction(driver, profile["monitoringTokensList"][0], tasksConfig["join"]["channel_link"], tasks, profile, tasksConfig, tasksData)
