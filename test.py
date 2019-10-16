# -*- coding: utf-8 -*-
# @Time : 2019/8/21 22:01
# @Software: PyCharm
# @author: 洋
# @File : test.py
from models import *


def test_create_school():
    s = School(name="人通科技", city="天津", address="天保公寓")
    s.insert_one()


def test_school():
    s = School(name="人通科技", city="天津", address="天保公寓")
    s.create()


def test_user():
    u = User(username="zj1007", password="123", name="zj", age=20, sex="男", phone="15023332345", _class="TJ190501T",
             course="大数据",
             school_name="人通", auth="tea", auth_id="0024")
    u.insert_one()


def test_class():
    c = Class(name="python", teacher="左老师", course="python")
    c.insert_one()


data = {'username': '小飞',
        'password': '123',
        'name': 'lyy',
        'birthday': '20',
        'sex': '男',
        'phone': '13920008888',
        '_class': '001',
        'course': '人工智能',
        'school_name': '北大',
        'auth': 'stu',
        'auth_id': '001'
        }
data1 = [['5', '小明', '123', 'lyy', '20', '男', '13920005838', '001', '人工智能', '北大', 'stu', '001'],
         ['6', '小红', '123', 'lyy', '20', '男', '13920005838', '001', '人工智能', '北大', 'stu', '001'],
         ['7', '小张', '123', 'lyy', '20', '男', '13920005838', '001', '人工智能', '北大', 'stu', '001']]
stu = Student()
stu.find("id","1")
