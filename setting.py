# -*- coding: utf-8 -*-
# @Time : 2019/8/20 10:30
# @Software: PyCharm
# @author: 洋
# @File : setting.py
import os

'''文件路径'''

#  项目路径(获取当前文件路径 os.getcwd())
BASE_PATH = os.getcwd()
#  把所有数据文件放入data目录下
DATA_DIR = os.path.join(BASE_PATH, "data")
#  把所有用户信息放到data目录下的userinfo.csv文件中
USER_FILE = os.path.join(DATA_DIR, "user_info.csv")
#  学校信息
SCHOOL_FILE = os.path.join(DATA_DIR, "school.csv")
#  课程信息
COURSE_FILE = os.path.join(DATA_DIR, "course.csv")
#  班级信息
CLASS_FILE = os.path.join(DATA_DIR, "class.csv")
#  支付表
PAY_COST = os.path.join(DATA_DIR, "pay_cost.csv")

'''正则表达式'''
# username 长度大于等于3小于等于10个字符，由数字字母下划线组成
USERNAME_RE = "^[a-zA-Z0-9_]{3,10}$"
# password 6-20位字符 "\w" 是除了空格特殊符号外的任意字符 即数字字母
PASSWORD_RE = "^\w{6,20}$"
# phone
PHONE_RE = "^1(3|4|5|7|8)\d{9}$"
# age "?0" 代表匹配0 一次或多次
BIRTHDAY_RE = "^((19|20)\d{2})-(1[0-2]|0[1-9])-(0[1-9]|[1-2][0-9]|3[0-1])$"
# sex M F
SEX_RE = "^[mfMF]$"
# name
NAME_RE = "\w{2,4}"

'''短信验证'''
API_URL = "https://sms_developer.zhenzikj.com"
APP_ID = 102972
APP_SECRET = "a02dfb0e-6199-422b-ab28-6c4b497dd5b0"
