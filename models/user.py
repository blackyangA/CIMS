# -*- coding: utf-8 -*-
# @Time : 2019/10/17 11:29
# @Software: PyCharm
# @author: 洋
# @File : user.py
import datetime
from unit import get_age
from setting import USER_FILE
from models.models import Model
from models._class import Class


#  用户抽象类
class User(Model):
    title = ["id", "username", "password", "user", "birthday", "sex", "phone", "class", "course", "school_name", "auth",
             "auth_id", "create_date", "update_date"]

    def __init__(self, username="", password="", name="", birthday="", sex="", phone="", _class=None, course=None,
                 school_name=None, auth=None, auth_id=None, create_data=None):
        super().__init__(USER_FILE)
        # self.__id = 0
        self.username = username
        self.password = password
        self.name = name
        self.birthday = birthday
        self.sex = sex
        self.phone = phone
        self._class = _class
        self.course = course
        self.school_name = school_name
        self.auth = auth
        self.auth_id = auth_id
        self.create_date = create_data  # datetime.datetime.now()
        self.update_date = None
        if self.create_date is None:
            self.create_date = datetime.datetime.now()
        else:
            self.update_date = datetime.datetime.now()

    def unique_username(self, value):
        """
        用户名验证
        :param value:
        :return:
        """
        # 偏函数
        return self.unique("username", value)

    def unique_phone(self, value):
        """
        手机号验证
        :param value:
        :return:
        """
        return self.unique("phone", value)

    def insert_one(self, data=None):
        if data is None:
            data = str(self).split(",")
        if self.unique_username(data[1]):
            if self.unique_phone(data[6]):
                super().insert_one(data)
                return True
            else:
                print(f"注册失败，{data[6]}该手机号已被注册！")
        else:
            print(f"注册失败，{data[1]}用户名已存在!")

    def insert_many(self, data):
        for row in data:
            self.insert_one(row)

    def show_info(self):
        print(f"""
用户名:{self.username}
性别:{self.sex}
生日:{self.birthday}
年龄:{get_age(self.birthday)}
电话:{self.phone}
        """)

    def select_class(self, course):
        try:
            lis = []
            all_class = Class().find_all()
            for row in all_class:
                if course == row[3]:
                    lis.append(row)
            for i, v in enumerate(lis):
                print(i, v)
            no = input("请选择班级：")
            return lis[int(no)][1]
        except Exception as e:
            print(e)

    def __str__(self):
        return f"{self.id},{self.username},{self.password},{self.name},{self.birthday},{self.sex},{self.phone}," \
            f"{self._class},{self.course},{self.school_name},{self.auth}," \
            f"{self.auth_id},{self.create_date},{self.update_date}"
