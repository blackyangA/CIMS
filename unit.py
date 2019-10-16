# -*- coding: utf-8 -*-
# @Time : 2019/8/20 10:30
# @Software: PyCharm
# @author: 洋
# @File : unit.py
import hashlib
import random
import re
import datetime
from setting import *
# from zhenzismsclient import send_dx

'''
工具模块
密码加密
验证码
'''


def md5_password(psw):
    """

    :param psw: str
    :return: 16进制字符串
    """
    md5 = hashlib.md5(psw.encode("utf-8"))
    md5.update("👍".encode("utf-8"))
    return md5.hexdigest()


def sha256_password(psw):
    sha256 = hashlib.sha256(psw.encode("utf-8"))
    sha256.update("👍".encode("utf-8"))
    return sha256.hexdigest()


def verification_code(n):
    code = ""
    for i in range(n):
        num = random.randint(1, 10)
        if num % 2 == 0:
            code += chr(random.randint(65, 90))
        else:
            code += str(random.randint(0, 9))
    return code


def _check(res, value):
    result = re.match(res, value)
    if result:
        return value
    raise ValueError(f"{value},不符合规则！")


def check_name(value):
    return _check(NAME_RE, value)


def check_username(value):
    return _check(USERNAME_RE, value)


def check_password(value):
    return _check(PASSWORD_RE, value)


def check_phone(value):
    return _check(PHONE_RE, value)


def check_birthday(value):
    if _check(BIRTHDAY_RE, value):
        try:
            #  高阶函数 转换数据类型
            date = map(int, value.split("-"))
            #  date里面必须传整数年月日
            #  *解包 列表
            new_date = datetime.date(*date)
            return str(new_date)
        except Exception as e:
            print(e)
            return False
    else:
        return False


# 颜色函数
def _color(string, color=None):
    color_dict = {'black': 30,
                  'red': 31,
                  'green': 32,
                  'yellow': 33,
                  'blue': 34,
                  'purple': 35,
                  'blueness': 36,
                  'white': 37}
    start = '\033[%dm' % color_dict[color]
    end = '\033[0m'
    return start + string + end


def red(value):
    return _color(value, "red")


def green(value):
    return _color(value, "green")


def yellow(value):
    return _color(value, "yellow")


def blue(value):
    return _color(value, "blue")


def check_sex(value):
    return _check(SEX_RE, value)


# 通过生日获取年龄
def get_age(value):
    date = map(int, value.split("-"))
    birthday = datetime.date(*date)
    today = datetime.date.today()
    age = today.year - birthday.year
    if today.month >= birthday.month:
        pass
    elif today.month == birthday.month:
        if today.day >= birthday.day:
            pass
        else:
            age -= 1
    else:
        age -= 1
    return age


# #  短信验证
# def sms_verification():
#     # result = send_dx(phone)
#     #     # code = input("请输入短信验证码:").strip()
#     #     # if result == code:
#     #     #     return True
#     #     # else:
#     #     #     return False
#     while True:
#         phone = check_phone(input("请输入你的电话号码："))
#         code = verification_code(6)
#         print(f"验证码:{code}")
#         newcode = input("请输入验证码:").strip()
#         if code == newcode:
#             result = send_dx(phone)
#             sms_code = input("请输入短信验证码:").strip()
#             if result == sms_code:
#                 return phone
