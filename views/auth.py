# -*- coding: utf-8 -*-
# @Time : 2019/10/17 10:05
# @Software: PyCharm
# @author: 洋
# @File : auth.py
# 注册视图函数
from models.student import Student
from models.teacher import Teacher
from models.admin import Admin
from models.user import User
from unit import *
from views.student_views import *


def _register(user_type, *args, **kwargs):
    # *args **kwargs 可变长传参
    #  工厂模式
    if user_type == "stu":
        # 学生用户
        user = Student(*args, **kwargs, auth="stu")
    elif user_type == "tea":
        # 老师
        user = Teacher(*args, **kwargs, auth="tea")
    elif user_type == "admin":
        # 管理员
        user = Admin(*args, **kwargs, auth="admin")
    else:
        raise TypeError("类型错误！")
    #  使用多态特性
    user.insert_one()


def register():
    user_type = None
    while True:
        no = input("""
        1.学生注册
        2.讲师注册
        3.注册管理员
        """)
        if no == "1":
            user_type = "stu"
            break
        elif no == "2":
            user_type = "tea"
            break
        elif no == "3":
            user_type = "admin"
            break
        else:
            print("选择有误！")
    user_info = get_user_info()
    _register(user_type, **user_info)


def get_user_info():
    while True:
        try:
            username = check_username(input("请输入用户账号名："))
            password = check_password(input("请输入密码："))
            re_password = check_password(input("请再次输入密码："))
            if password == re_password:
                password = md5_password(password)
            else:
                print("两次输入密码不一致，请重新注册！")
                break
            name = check_name(input("请输入你的真实姓名："))
            birthday = check_birthday(input("请输入你的出生日期："))
            sex = check_sex(input("请输入你的性别："))
            # phone = sms_verification()
            phone = check_phone(input("请输入你的电话号码："))
        except Exception as e:
            print(e)
        else:
            user_info = {
                "username": username,
                "password": password,
                "name": name,
                "birthday": birthday,
                "sex": sex,
                "phone": phone
            }
            return user_info


#  锁定账户
def _lock_user(username, pwd, user, user_list, index):
    #  验证用户输入密码 三次机会
    for i in range(3):
        #  接收用户从控制台输入的密码
        password = check_password(input("请输入密码："))
        #  对接收的密码进行md5加密后和数据库取得的密码进行比对
        if md5_password(password) == pwd:
            #  两者一致登录成功
            print(f"欢迎{username}用户成功登录！")
            #  返回用户数据列表user_list
            return user_list
        else:
            #  否则 提示错误及剩余机会
            print(f"密码错误，还有{3 - (i + 1)}次机会！")
    else:
        # 密码三次验证不成功将原数据库MD5加密后的密码加一个“！”
        lock_password = "!" + pwd
        #  将修改后的密码更新到数据库
        user.updata(index, "password", lock_password)
        #  提示用户账号被锁定
        print("三次密码输入错误账户已被锁定！")


#  实现登录验证
def _to_login(username, user, user_list, index):
    #  如果user_list不为空
    if user_list:
        #  从user_list中获得password数据
        pwd = user_list[2]
        #  如果获取的password字符中含有“！”
        if "!" in pwd:
            #  说明账号已被锁定
            print(f"账号{username}已被锁定，请重置密码！")
            #  返回假
            return False
        #  账号没有被锁定的话执行_lock_user方法
        return _lock_user(username, pwd, user, user_list, index)
    else:
        print("用户不存在!")


def _login():
    while True:
        try:
            #  初始化一个user对象
            user = User()
            #  从控制台获取用户输入的用户名并验证
            username = check_username(input("请输入用户名："))
            #  通过find_username方法得到该用户名所在列下标及所在列数据
            #  （find_username返回值为元组）
            index, user_list = user.find_username(username)
            #  成功登录_to_login返回user_list列表如果不为空 结束while循环
            return _to_login(username, user, user_list, index)
        except Exception as e:
            print(e)


#  实现登录视图
def login():
    user_list = _login()
    if user_list:
        user_list = user_list[1:-1]
        auth = user_list[9]
        user = None
        if auth == "stu":
            print("身份：学生")
            user = Student(*user_list)
        elif auth == "tea":
            print("身份：老师")
            user = Teacher(*user_list)
        elif auth == "admin":
            print("身份：管理员")
            user = Admin(*user_list)
        return user


#  找回密码
def _get_back_password(user_list, user, index):
    if user_list:
        pwd = user_list[2]
        if "!" in pwd:
            password = check_password(input("请输入新密码:"))
            re_password = check_password(input("请再次输入新密码："))
            if password == re_password:
                user.updata(index, "password", md5_password(password))
                print("找回密码操作成功！")
                return True


def retrieve_password():
    #  1.如果用户存在,重置密码
    #  2.用户不存在,则选择注册
    while True:
        try:
            user = User()
            username = check_username(input("请输入用户名："))
            index, user_list = user.find_username(username)
            if _get_back_password(user_list, user, index):
                break
        except Exception as e:
            print(e)


#  查看个人信息
def show_info(user):
    user.show_info()
