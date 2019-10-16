# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import random
import ssl
from setting import API_URL, APP_ID, APP_SECRET


class ZhenziSmsClient(object):
    def __init__(self, apiUrl, appId, appSecret):
        self.apiUrl = apiUrl
        self.appId = appId
        self.appSecret = appSecret

    def send(self, number, message, messageId=''):
        data = {
            'appId': self.appId,
            'appSecret': self.appSecret,
            'message': message,
            'number': number,
            'messageId': messageId
        }
        data = urllib.parse.urlencode(data).encode('utf-8')
        req = urllib.request.Request(self.apiUrl + '/sms/send.do', data=data)
        res_data = urllib.request.urlopen(req, context=ssl._create_unverified_context())
        res = res_data.read()
        res = res.decode('utf-8')
        return res

    def balance(self):
        data = {
            'appId': self.appId,
            'appSecret': self.appSecret
        }
        data = urllib.parse.urlencode(data).encode('utf-8')
        req = urllib.request.Request(self.apiUrl + '/account/balance.do', data=data)
        res_data = urllib.request.urlopen(req)
        res = res_data.read()
        return res

    def findSmsByMessageId(self, messageId):
        data = {
            'appId': self.appId,
            'appSecret': self.appSecret,
            'messageId': messageId
        }
        data = urllib.parse.urlencode(data).encode('utf-8')
        req = urllib.request.Request(self.apiUrl + '/smslog/findSmsByMessageId.do', data=data)
        res_data = urllib.request.urlopen(req)
        res = res_data.read()
        return res


def send_dx(mobile):
    code = str(random.randint(1000, 9999))
    # api_url = "https://sms_developer.zhenzikj.com"
    # app_id = 102972
    # app_secret = "a02dfb0e-6199-422b-ab28-6c4b497dd5b0"
    client = ZhenziSmsClient(API_URL, APP_ID, APP_SECRET)
    result = client.send(mobile, "您的验证码是%s" % code)
    print(result)
    return code
