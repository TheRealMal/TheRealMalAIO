import requests
import os
from datetime import datetime
import time
import random
import urllib.parse
import uuid
import json
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
    driver = webdriver.Chrome(options=options, executable_path='C:/Users/TheRealMal/Desktop/TRM/pyBot_v2/chromedriver.exe')
    return driver

def joinServer_browser(driver, accountToken, inviteCode, proxy, captchaClientKey, captchaData={}):
    try:
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
    except Exception as e:
        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '..{} | Something went wrong (Request)'.format(accountToken[-10:]))
        print(e)
        return False
    if r.get("captcha_service", None) == None:
        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '..{} | Successfully joined'.format(accountToken[-10:]))
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
                    return joinServer_browser(driver, accountToken, inviteCode, proxy, captchaClientKey, captchaResult)
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

def joinServer(accountToken, inviteCode, proxy, captchaClientKey, captchaData={}):
    try:
        if proxy == None:
            r = requests.post("https://discord.com/api/v9/invites/{}".format(inviteCode), headers={
                'accept': 'application/json, text/plain, */*',
                'authorization': accountToken,
                'content-type': 'application/json',
                'cookie': 'locale=ru',
                'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="98", "Chromium";v="98"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
                'x-super-properties': sup_prop
            }, json=captchaData)
        else:
            r = requests.post("https://discord.com/api/v9/invites/{}".format(inviteCode), headers={
                'accept': 'application/json, text/plain, */*',
                'authorization': accountToken,
                'content-type': 'application/json',
                'cookie': 'locale=ru',
                'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="98", "Chromium";v="98"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
                'x-super-properties': sup_prop
            }, json=captchaData, proxies={"https":"https://" + proxy})
    except Exception as e:
        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '..{} | Something went wrong (Request)'.format(accountToken[-10:]))
        print(e)
        return False
    if r.status_code == 200:
        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '..{} | Successfully joined'.format(accountToken[-10:]))
        return True
    else:
        try:
            r = r.json()
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
                    captchaResult["captcha_rqtoken"] = r["captcha_rqtoken"]
                    print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '..{} | Got HCaptcha solution'.format(accountToken[-10:]))
                    return joinServer(accountToken, inviteCode, proxy, captchaClientKey, captchaResult)
                else:
                    input('Add capMonster site key to config.json and restart. . .')
                    return False
            else:
                print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '..{} | Something went wrong (Account)'.format(accountToken[-10:]))
                print(r)
                return False
        except:
            print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '..{} | Something went wrong (Account)'.format(accountToken[-10:]))
            print(r.text)
            return False

def sendMessage(accountToken, channelLink, message, proxy):
    channelID = channelLink.split('/')[-1]
    try:
        if proxy == None:
            r = requests.post("https://discord.com/api/v9/channels/{}/messages".format(channelID), headers={
                'accept': 'application/json, text/plain, */*',
                'authorization': accountToken,
                'content-type': 'application/json',
                'cookie': 'locale=ru',
                'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="98", "Chromium";v="98"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
            }, json={'content': message, 'tts': False})
        else:
            r = requests.post("https://discord.com/api/v9/channels/{}/messages".format(channelID), headers={
                'accept': 'application/json, text/plain, */*',
                'authorization': accountToken,
                'content-type': 'application/json',
                'cookie': 'locale=ru',
                'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="98", "Chromium";v="98"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
            }, json={'content': message, 'tts': False}, proxies={"https":"https://" + proxy})
    except Exception as e:
        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '..{} | Something went wrong (Request)'.format(accountToken[-10:]))
        print(e)
        return False
    if r.status_code == 200:
        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '..{} | Successfully sent message'.format(accountToken[-10:]))
        return True
    else:
        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '..{} | Something went wrong (Account/Server)'.format(accountToken[-10:]))
        print(r.text)
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
        return {}
    else: 
        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '{} | Something went wrong while getting message (Account/Server)'.format(accountToken[-10:]))
        print(r.text)
        return {}

def sendButtonPress(accountToken, messageLink, button_number, proxy):
    guildID = messageLink.split('/')[-3]
    channelID = messageLink.split('/')[-2]
    messageID = messageLink.split('/')[-1]
    component = getVerificationMessage(accountToken, channelID, messageID, button_number, proxy)
    if component == {}:
        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '..{} | Something went wrong (Message)'.format(accountToken[-10:]))
        return False
    data = {
        "type": 3,
        "nonce": str(uuid.uuid4().time),
        "guild_id": guildID,
        "channel_id": channelID,
        "message_flags": 0,
        "message_id": messageID,
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
        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '..{} | Successfully sent button press'.format(accountToken[-10:]))
        return True
    else:
        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '..{} | Something went wrong (Account)'.format(accountToken[-10:]))
        return False

def sendInteraction(accountToken, payload, proxy):
    try:
        if proxy == None:
            r = requests.post("https://discord.com/api/v9/interactions", headers={
                'accept': '*/*',
                'authorization': accountToken,
                'cookie': 'locale=ru',
                'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="98", "Chromium";v="98"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
            }, files={'payload_json': (None, payload)})
        else:
            r = requests.post("https://discord.com/api/v9/interactions", headers={
                'accept': '*/*',
                'authorization': accountToken,
                'cookie': 'locale=ru',
                'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="98", "Chromium";v="98"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
            }, files={'payload_json': (None, payload)}, proxies={"https":"https://" + proxy})
    except Exception as e:
        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '..{} | Something went wrong (Request)'.format(accountToken[-10:]))
        print(e)
        return False
    if r.status_code == 204:
        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '..{} | Successfully interacted'.format(accountToken[-10:]))
        return True
    else:
        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '..{} | Something went wrong (Account/Server)'.format(accountToken[-10:]))
        print(r.text)
        return False

def sendReaction(accountToken, messageLink, reaction, proxy):
    channelID = messageLink.split('/')[-2]
    messageID = messageLink.split('/')[-1]
    try:
        if proxy == None:
            r = requests.put("https://discord.com/api/v9/channels/{}/messages/{}/reactions/{}/%40me".format(channelID, messageID, reaction), headers={
                'accept': 'application/json, text/plain, */*',
                'authorization': accountToken,
                'content-type': 'application/json',
                'cookie': 'locale=ru',
                'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="98", "Chromium";v="98"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
            })
        else:
            r = requests.put("https://discord.com/api/v9/channels/{}/messages/{}/reactions/{}/%40me".format(channelID, messageID, reaction), headers={
                'accept': 'application/json, text/plain, */*',
                'authorization': accountToken,
                'content-type': 'text/plain',
                'cookie': 'locale=ru',
                'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="98", "Chromium";v="98"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
            }, proxies={"https":"https://" + proxy})
    except Exception as e:
        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '..{} | Something went wrong (Request)'.format(accountToken[-10:]))
        print(e)
        return False
    if r.status_code == 204:
        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '..{} | Successfully reacted'.format(accountToken[-10:]))
        return True
    else:
        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '..{} | Something went wrong (Account/Server)'.format(accountToken[-10:]))
        print(r.text)
        return False

def getRules(accountToken, messageLink, proxy):
    guildID = messageLink.split('/channels/')[1].split('/')[0]
    try:
        if proxy == None:
            r = requests.get("https://discord.com/api/v9/guilds/{}/member-verification?with_guild=false".format(guildID), headers={
                'accept': '*/*',
                'authorization': accountToken,
                'content-type': 'application/json',
                'cookie': 'locale=ru',
                'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="98", "Chromium";v="98"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
            })
        else:
            r = requests.get("https://discord.com/api/v9/guilds/{}/member-verification?with_guild=false".format(guildID), headers={
                'accept': '*/*',
                'authorization': accountToken,
                'content-type': 'application/json',
                'cookie': 'locale=ru',
                'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="98", "Chromium";v="98"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
            }, proxies={"https":"https://" + proxy})
    except Exception as e:
        return {}
    if r.status_code == 200:
        return r.json()
    else:
        return {}

def sendRules(accountToken, messageLink, proxy):
    data = getRules(accountToken, messageLink, proxy)
    guildID = messageLink.split('/channels/')[1].split('/')[0]
    try:
        if proxy == None:
            r = requests.put("https://discord.com/api/v9/guilds/{}/requests/@me".format(guildID), headers={
                'accept': '*/*',
                'authorization': accountToken,
                'content-type': 'application/json',
                'cookie': 'locale=ru',
                'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="98", "Chromium";v="98"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
            }, json=data)
        else:
            r = requests.put("https://discord.com/api/v9/guilds/{}/requests/@me".format(guildID), headers={
                'accept': '*/*',
                'authorization': accountToken,
                'content-type': 'application/json',
                'cookie': 'locale=ru',
                'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="98", "Chromium";v="98"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
            }, json=data, proxies={"https":"https://" + proxy})
    except Exception as e:
        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '..{} | Something went wrong (Request)'.format(accountToken[-10:]))
        print(e)
        return False
    if r.status_code == 201:
        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '..{} | Successfully accepted rules'.format(accountToken[-10:]))
        return True
    else:
        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '..{} | Something went wrong (Account/Server)'.format(accountToken[-10:]))
        print(r.text)
        return False

def prepareSettings():
    tasks = [{"method": "join", "config":{"delay": 0}}]
    tasksString = ['Join server']
    os.system('cls' if os.name == 'nt' else 'clear')
    printTRM()
    print('Tasks:', '\033[94m{}\033[0m'.format(', '.join(tasksString)), '\n')
    print('Choose what to do:')
    print('   (\033[91m1\033[0m) Join server: {}'.format("Yes" if len(tasks) > 0 and tasks[0]["method"] == "join" else "No"))
    print('   (\033[91m2\033[0m) Accept rules')
    print('   (\033[91m3\033[0m) React to message')
    print('   (\033[91m4\033[0m) Send message')
    print('   (\033[91m5\033[0m) Interact (Use command)')
    print('   (\033[91m6\033[0m) Press button')
    print('   (\033[91m7\033[0m) Start task')
    methodChoice = input('>>> \033[94m')
    print('\033[0m', end='')
    while methodChoice != "7":
        if (methodChoice == "1"):
            if len(tasks) > 0 and tasks[0]["method"] == "join":
                del tasks[0]
                del tasksString[0]
            else:
                tasks.insert(0, {"method": "join", "config":{"delay": 0}})
                tasksString.insert(0, "Join server")
        if (methodChoice == "2"):
            data = {"method": "rules", "config":{"message_link":"", "delay": 0}}
            data["config"]["message_link"] = input('  Message/channel link\n  >>> \033[94m')
            print('\033[0m', end='')
            if (len(tasks) >= 1):
                data["config"]["delay"] = int(input('  Enter delay before this action (ms)\n  >>> \033[94m'))
                print('\033[0m', end='')
            tasks.append(data)
            tasksString.append("Accept rules")
        elif (methodChoice == "3"):
            data = {"method": "react", "config":{"message_link":"","react":"", "delay": 0}}
            data["config"]["message_link"] = input('  Message link\n  >>> \033[94m')
            print('\033[0m', end='')
            data["config"]["react"] = urllib.parse.quote_plus(input('  Reaction\n  >>> \033[94m'))
            print('\033[0m', end='')
            if (len(tasks) >= 1):
                data["config"]["delay"] = int(input('  Enter delay before this action (ms)\n  >>> \033[94m'))
                print('\033[0m', end='')
            tasks.append(data)
            tasksString.append("React to message")
        elif (methodChoice == "4"):
            data = {"method": "send", "config":{"channel_link":"","message":"", "delay": 0}}
            data["config"]["channel_link"] = input('  Channel link\n  >>> \033[94m')
            print('\033[0m', end='')
            data["config"]["message"] = input('  Message\n  >>> \033[94m')
            print('\033[0m', end='')
            if (len(tasks) >= 1):
                data["config"]["delay"] = int(input('  Enter delay before this action (ms)\n  >>> \033[94m'))
                print('\033[0m', end='')
            tasks.append(data)
            tasksString.append("Send message")
        elif (methodChoice == "5"):
            data = {"method": "interact", "config":{"payload":"", "delay": 0}}
            data["interact"]["payload"] = input('  Payload\n  >>> \033[94m')
            print('\033[0m', end='')
            if (len(tasks) >= 1):
                data["config"]["delay"] = int(input('  Enter delay before this action (ms)\n  >>> \033[94m'))
                print('\033[0m', end='')
            tasks.append(data)
            tasksString.append("Interact")
        elif (methodChoice == "6"):
            data = {"method": "button", "config":{"message_link":"", "button_number":0, "delay": 0}}
            data["config"]["message_link"] = input('  Message link\n  >>> \033[94m')
            print('\033[0m', end='')
            data["config"]["button_number"] = int(input('  Button number\n  >>> \033[94m'))-1
            print('\033[0m', end='')
            if (len(tasks) >= 1):
                data["config"]["delay"] = int(input('  Enter delay before this action (ms)\n  >>> \033[94m'))
                print('\033[0m', end='')
            tasks.append(data)
            tasksString.append("Press button")
        os.system('cls' if os.name == 'nt' else 'clear')
        printTRM()
        print('Tasks:', '\033[94m{}\033[0m'.format(', '.join(tasksString)), '\n')
        print('Choose method:')
        print('   (\033[91m1\033[0m) Join server: {}'.format("Yes" if len(tasks) > 0 and tasks[0]["method"] == "join" else "No"))
        print('   (\033[91m2\033[0m) Accept rules')
        print('   (\033[91m3\033[0m) React to message')
        print('   (\033[91m4\033[0m) Send message')
        print('   (\033[91m5\033[0m) Interact (Use command)')
        print('   (\033[91m6\033[0m) Press button')
        print('   (\033[91m7\033[0m) Start task')
        methodChoice = input('>>> \033[94m')
        print('\033[0m', end='')
    return tasks, tasksString

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

def main():
    printTRM()

    profile = loadProfile()

    tasks, tasksString = prepareSettings()

    os.system('cls' if os.name == 'nt' else 'clear')
    printTRM()
    print('Tasks:', '\033[94m{}\033[0m'.format(', '.join(tasksString)), '\n')
    if "join" == tasks[0]["method"]:
        inviteCode = input('Enter invite (Link or Code)\n>>> \033[94m')
        print('\033[0m', end='')
        if "discord.gg/" in inviteCode:
            inviteCode = inviteCode.split('discord.gg/')[1]

    inviteDelay = int(input('Enter delay between accounts (ms)\n>>> \033[94m'))
    print('\033[0m', end='')

    if "join" == tasks[0]["method"]:
        safeMode = input('Safe mode? (Y/N)\n>>> \033[94m')
        print('\033[0m', end='')
        if safeMode.lower() == "y":
            safeMode = True
        else:
            safeMode = False
    else:
        safeMode = False
    os.system('cls' if os.name == 'nt' else 'clear')
    printTRM()

    print('   Tokens list:', '\033[94m{}\033[0m'.format(profile["tokensListName"]))
    print('   Proxies list:', '\033[94m{}\033[0m'.format(profile["proxiesListName"]))
    if "join" == tasks[0]["method"]:
        print('   Invite code:', '\033[94m{}\033[0m'.format(inviteCode))
    print('   Tasks:', '\033[94m{}\033[0m'.format(', '.join(tasksString)), '\n')
    
    if safeMode:
        print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), 'Safe mode')
        driver = createDriver()
        driver.get("https://discord.com/")
        driver.execute_script('''let token = \''''+profile["tokensList"][0]+'''\'; function login(token){setInterval(() => {document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"${token}"`}, 50); setTimeout(() => {location.reload();}, 2500);}login(token);''')
        driver.get("https://discord.com/app")
        time.sleep(3)
    print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), 'Starting task')
    for token in profile["tokensList"]:
        if len(profile["proxiesList"]) != 0:
            proxy = profile["proxiesList"][random.randint(0,len(profile["proxiesList"])-1)]
        else:
            proxy = None
        for x in range(len(tasks)):
            time.sleep(tasks[x]["config"]["delay"]/1000)
            if "join" == tasks[x]["method"]:
                if safeMode:
                    task_join = joinServer_browser(driver, token, inviteCode, proxy, profile["captchaClientKey"])
                else:
                    task_join = joinServer(token, inviteCode, proxy, profile["captchaClientKey"])
                if not task_join:
                    break
            elif "rules" == tasks[x]["method"]:
                time.sleep(random.randint(0,500)/1000)
                task_rules = sendRules(token, tasks[x]["config"]["message_link"], proxy)
            elif "send" == tasks[x]["method"]:
                time.sleep(random.randint(0,500)/1000)
                task_send = sendMessage(token, tasks[x]["config"]["channel_link"], tasks[x]["config"]["message"], proxy)
            elif "react" == tasks[x]["method"]:
                time.sleep(random.randint(0,500)/1000)
                task_react = sendReaction(token, tasks[x]["config"]["message_link"], tasks[x]["config"]["react"], proxy)
            elif "interact" == tasks[x]["method"]:
                time.sleep(random.randint(0,500)/1000)
                task_interact = sendInteraction(token, tasks[x]["config"]["payload"], proxy)
            elif "button" == tasks[x]["method"]:
                time.sleep(random.randint(0,500)/1000)
                task_button = sendButtonPress(token, tasks[x]["config"]["message_link"], tasks[x]["config"]["button_number"], proxy)
        time.sleep(inviteDelay/1000)
    if safeMode:
        driver.close()
    input('Press Enter to continue. . .')