# -*- coding: utf-8 -*-
# @Time : 2019/8/20 10:29
# @Software: PyCharm
# @author: 洋
# @File : views.py.py
from models import Student, Teacher, Admin, User
from unit import *
from zhenzismsclient import send_dx

'''
MVC
models 管理数据和数据打交道
view 视图操作，让用户操作的执行操作
controller 管理器，从models中获取数据
'''


# 注册视图函数
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

    """"004登录注册   27:31"""


"""
username,
password,
name,
birthday,
sex,
phone,
_class=None,
course=None,
school_name=None,
auth=None,
auth_id=None,
create_date = None
"""


def sms_verification():
    # result = send_dx(phone)
    # code = input("请输入短信验证码:").strip()
    # if result == code:
    #     return True
    # else:
    #     return False
    while True:
        phone = check_phone(input("请输入你的电话号码："))
        code = verification_code(6)
        print(f"验证码:{code}")
        newcode = input("请输入验证码:").strip()
        if code == newcode:
            result = send_dx(phone)
            sms_code = input("请输入短信验证码:").strip()
            if result == sms_code:
                return phone


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


#  实现登录验证
def _login():
    while True:
        try:
            user = User()
            username = check_username(input("请输入用户名："))
            index, user_list = user.find_username(username)
            if user_list:
                pwd = user_list[2]
                if "!" in pwd:
                    print(f"账号{username}已被锁定，请重置密码！")
                    return False
                for i in range(3):
                    password = check_password(input("请输入密码："))
                    if md5_password(password) == pwd:
                        print(f"欢迎{username}用户成功登录！")
                        return user_list
                    # print(f"密码输入错误{i+1}次，还有{2-(i+1)}次机会！")
                    else:
                        print(f"密码错误，还有{3 - (i + 1)}次机会！")
                else:
                    # 锁定，让原密码失效
                    lock_password = "!" + pwd
                    user.updata(index, "password", lock_password)
                    print("三次密码输入错误账户已被锁定！")
            else:
                print("用户不存在!")
        except Exception as e:
            print(e)


#  实现登录视图
def login():
    user_list = _login()
    print(user_list)
    if user_list:
        print("aaaa")
        user_list = user_list[1:-1]
        print(user_list)
        auth = user_list[9]
        print(auth)
        user = None
        if auth == "stu":
            print("身份：学生")
            user = Student(*user_list)
            student_view(user)
        elif auth == "tea":
            print("身份：老师")
            user = Teacher(*user_list)
        elif auth == "admin":
            print("身份：管理员")
            user = Admin(*user_list)
        return user


#  找回密码
def retrieve_password():
    #  1.如果用户存在,重置密码
    #  2.用户不存在,则选择注册
    while True:
        try:
            user = User()
            username = check_username(input("请输入用户名："))
            index, user_list = user.find_username(username)
            if user_list:
                pwd = user_list[2]
                if "!" in pwd:
                    password = check_password(input("请输入新密码:"))
                    re_password = check_password(input("请再次输入新密码："))
                    if password == re_password:
                        user.updata(index, "password", md5_password(password))
                        print("找回密码操作成功！")
                        return
        except Exception as e:
            print(e)


#  查看个人信息
def show_info(user):
    user.show_info()


#  学生视图
def student_view(user):
    while True:
        no = input("""
        1.显示个人信息
        2.选择课程
        3.购买课程
        4.上课
        5.退出
         """)
        if no == "1":
            user.show_info()
        elif no == "2":
            user.select_course()
        elif no == "3":
            user.pay()
        elif no == "4":
            pass
        elif no == "5":
            break
        else:
            print("输入错误！")

#  讲师视图


#  管理员视图
