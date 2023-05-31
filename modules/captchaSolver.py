import requests
import datetime
import time

class CaptchaSolver:
    def __init__(self, data, captchaService):
        self.__captchaData = data
        self.__captchaServie = captchaService.lower()
        self.__captchaType = "hcaptcha"
        self.solution = {}
    
    def solve(self):
        if self.__captchaServie == "capmonster":
            taskId = self.__sendCapmonsterRequest(self.__captchaData.get("accountToken", "undefined"), self.__captchaData["captchaClientKey"], self.__captchaData["websiteKey"], self.__captchaData["rqData"], self.__captchaData["ua"])
            result = self.__getCapmonsterResult(self.__captchaData.get("accountToken", "undefined"), self.__captchaData["captchaClientKey"], taskId)
            return result

    def __sendCapmonsterRequest(self, accountToken, captchaClientKey, websiteKey, rqData, ua="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"):
        try:
            taskId = requests.post("https://api.capmonster.cloud/createTask", headers={
                'content-type': 'application/json',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
            }, json={
                "clientKey":captchaClientKey,
                "task":
                {
                    "type": "HCaptchaTaskProxyless",
                    "websiteURL": "https://discord.com",
                    "websiteKey": websiteKey,
                    "isInvisible": True,
                    "userAgent": ua,
                    "data": rqData
                }
            }).json()["taskId"]
        except Exception as e:
            print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '..{} | Something went wrong (HCaptcha)'.format(accountToken[-10:]))
            print(e)
            return None
        return taskId

    def __getCapmonsterResult(self, accountToken, captchaClientKey, taskId, count=0):
        try:
            result = requests.post("https://api.capmonster.cloud/getTaskResult", headers={
                'content-type': 'application/json',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
            }, json={
                "clientKey": captchaClientKey,
                "taskId": taskId
            }).json()
        except Exception as e:
            if count < 5:
                return self.__getCapmonsterResult(accountToken, captchaClientKey, taskId, count+1)
            else:
                print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '..{} | Something went wrong (HCaptcha)'.format(accountToken[-10:]))
                print(e)
                return {}
        if result["status"] == "ready":
            return {"captcha_key": result["solution"]["gRecaptchaResponse"]}
        elif result["status"] == "processing":
            time.sleep(2.5)
            return self.__getCapmonsterResult(accountToken, captchaClientKey, taskId, count)
        else:
            print('\033[33mDiscord\033[0m | [{}]'.format(datetime.now().strftime('%H:%M:%S.%f')[:-3]), '..{} | Unsolvable captcha'.format(accountToken[-10:]))
            print(e)
            return {}
