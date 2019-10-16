#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Date: 2019/8/20 10:28
# Author: ZuoJie
# Version: 1.0
import os
import csv
import abc
from settings import USER_FILE


class Model(metaclass=abc.ABCMeta):
    def __init__(self, file_name=USER_FILE):
        self.file_name = file_name

    def create(self, data=None):
        if os.path.exists(self.file_name):
            print(f"{os.path.basename(self.file_name)}文件已存在！不能重复创建！")
            return
        else:
            with open(self.file_name, "x", encoding="utf-8", newline="") as f:
                csv_write = csv.writer(f)
                if data:
                    csv_write.writerow(data)

    def drop(self):
        os.remove(self.file_name)

    def insert_one(self, line):
        if os.path.exists(self.file_name):
            with open(self.file_name, "a", encoding="utf-8", newline="") as f:
                csv_write = csv.writer(f)
                if line:
                    csv_write.writerow(line)
        else:
            print(f"{os.path.basename(self.file_name)}不存在！请先创建！")


class School:
    __slots__ = ("__name", "__city", "__address")

    def __init__(self, name, address, city):
        self.__name = name
        self.__city = city
        self.__address = address

    @property
    def name(self):
        return self.__name

    @property
    def city(self):
        return self.__city

    @property
    def address(self):
        return self.__address

    def __str__(self):
        return f"{self.__name}学校,{self.__city}市,{self.__address}"


class User(Model):
    title = ["id", "username", "password", "name", "age", "sex", "phone", "class", "course", "school_name", "auth",
             "auth_id"]

    def __init__(self, username, password, name, age, sex, phone, _class, course, school_name, auth, auth_id):
        super().__init__()
        self.__id = 0
        self.__username = username
        self.__password = password
        self.__name = name
        self.__age = age
        self.__sex = sex
        self.__phone = phone
        self.__class = _class
        self.__course = course
        self.__school_name = school_name
        self.__auth = auth
        self.__auth_id = auth_id

    def create(self, data=None):
        if data is None:
            data = self.title
        super().create(data)

    def insert_one(self, line=None):
        if line is None:
            line = str(self).split(",")
        super().insert_one(line)

    def __str__(self):
        return f"{self.__id},{self.__username},{self.__password},{self.__name},{self.__age},{self.__sex},{self.__phone},{self.__class},{self.__course},{self.__school_name},{self.__auth},{self.__auth_id}"


if __name__ == '__main__':
    user = User(username="zj1007", password="123", name="zj", age=20, sex="男", phone="15023332345", _class="TJ190501T",
                course="大数据",
                school_name="人通", auth="tea", auth_id="0024")
    user.create()
    user.insert_one()
