from colorama import init
import requests
import readchar
import string
import json
import time
import os
import ctypes

version = "0.2.1"

kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
os.system("title TheRealMal AIO v{}".format(version))
init()

key = []

def printTRM():
    print()
    print('\n\033[93m')
    print('                                         __________  __  ___   ___    ________')
    print('                                        /_  __/ __ \/  |/  /  /   |  /  _/ __ \\')
    print('                                         / / / /_/ / /|_/ /  / /| |  / // / / /')
    print('                                        / / / _, _/ /  / /  / ___ |_/ // /_/ /')
    print('                                       /_/ /_/ |_/_/  /_/  /_/  |_/___/\____/')
    print('\033[0m\n')

def clearConsole():
    os.system('cls' if os.name == 'nt' else 'clear')

def authorization(key, attempt=0):
    if attempt < 2:
        try:
            r = requests.post('https://sresellera.ru/2.0/key/{}'.format(key), json={
                'module':'trm'
            }, verify=False).json()
        except:
            print("                                                   Authorizing. . . ({} attempt)".format(attempt+2), end="\r", flush=True)
            time.sleep(0.5)
            return authorization(key, attempt+1)
        if r["message"] == "Authorized":
            return {'authorized': True}
    return {'authorized': False}

def configInit(key):
    with open('config.json', 'r') as f:
        d = json.load(f)
        d["key"] = key
        if d.get("hcaptcha", None) == None:
            d["hcaptcha"] = ""
        if d.get("webhook", None) == None:
            d["webhook"] = ""
    with open('config.json', 'w') as f:
        json.dump(d, f, indent=4, sort_keys=True)
    try:
        os.makedirs("sites")
    except FileExistsError:
        pass
    try:
        os.makedirs("sites/discord")
    except FileExistsError:
        pass
    try:
        os.makedirs("sites/discord/tokens")
    except FileExistsError:
        pass
    try:
        os.makedirs("sites/discord/proxies")
    except FileExistsError:
        pass
    try:
        os.makedirs("sites/discord/phrases")
    except FileExistsError:
        pass
    try:
        f = open(os.path.join('sites', 'discord', 'tokens', 'default.txt'), 'x')
        f.close()
    except:
        pass
    try:
        f = open(os.path.join('sites', 'discord', 'proxies', 'default.txt'), 'x')
        f.close()
    except:
        pass
    try:
        f = open(os.path.join('sites', 'discord', 'phrases', 'default.txt'), 'x')
        f.close()
    except:
        pass
    
    try:
        f = open(os.path.join('sites', 'discord', 'deleteKeywords.txt'), 'x')
        f.close()
    except:
        pass
    try:
        f = open(os.path.join('sites', 'discord', 'invites.txt'), 'x')
        f.close()
    except:
        pass
    
def mainScreen():
    clearConsole()
    printTRM()
    print('Choose module:')
    print('   (\033[91m1\033[0m) Discord Joiner')
    print('   (\033[91m2\033[0m) Discord Joiner (FCFS)')
    print('   (\033[91m3\033[0m) Discord Invite Creator')
    print('   (\033[91m4\033[0m) Discord Phrase Spammer')
    print('   (\033[91m5\033[0m) Discord Chat Bot')
    print('   (\033[91m6\033[0m) Discord Replies Bot')
    print('   (\033[91m7\033[0m) Rumble Royal & Giveaway monitor')
    siteChoice = input('>>> \033[94m')
    print('\033[0m', end='')
    clearConsole()
    if siteChoice == "1":
        import modules.joiner
        modules.joiner.main()
    elif siteChoice == "2":
        import modules.joinerFCFS
        modules.joinerFCFS.main(version)
    elif siteChoice == "3":
        import modules.inviteCreator
        modules.inviteCreator.main()
    elif siteChoice == "4":
        import modules.spammer
        modules.spammer.main(version)
    elif siteChoice == "5":
        import modules.chatBot
        modules.chatBot.main(version)
    elif siteChoice == "6":
        import modules.replyBot
        modules.replyBot.main(version)
    elif siteChoice == "7":
        import modules.giveawayAndRumble
        modules.giveawayAndRumble.main(version)

def authScreen(key):
    clearConsole()
    printTRM()
    print('                                                  Enter your key')
    print('                                          [ ___________________________ ]            ', end="\r")
    print('                                          [ ', end="")

    try:
        f = open('config.json', 'x')
        f = open('config.json', 'w')
        json.dump({'key':'', 'webhook':'', 'hcaptcha': ''}, f, sort_keys=True, indent=4)
        f.close()
    except:
        pass
    with open('config.json', 'r') as f:
        f = json.load(f)
        inputKey = f["key"]
    if inputKey == "":
        while True:
            readedKey = readchar.readkey()
            if readedKey == readchar.key.ENTER:
                if len(inputKey) >= 26:
                    break
                else:
                    continue
            elif readedKey in string.printable and len(inputKey) < 27:
                inputKey += readedKey
                print(readedKey, end="")
            elif readedKey not in string.printable and len(inputKey) != 0:
                print('\b_\b', end="", flush=True)
                inputKey = inputKey[:-1]
                continue
            elif len(inputKey) == 27:
                continue
    else:
        for letter in inputKey:
            print(letter, end="")
            time.sleep(0.04)
    key.append(inputKey)
    print("\n                                                   Authorizing. . .", end="\r", flush=True)
    time.sleep(0.5)
    #isAuthorized = authorization(key[0])
    isAuthorized = {"authorized": len(key[0]) != 0}
    if isAuthorized["authorized"]:
        print("\033[94m                                             Successfully authorized!\033[0m              ")
        configInit(key[0])
        time.sleep(1.5)
        while True:
            mainScreen()
    else:
        print("\033[91m                                               Authorization failed\033[0m              ")
        time.sleep(1)
        input("                                             Press Enter to exit. . .")

if __name__ == '__main__':
    from multiprocessing import freeze_support
    freeze_support()
    authScreen(key)
    clearConsole()