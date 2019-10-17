# -*- coding: utf-8 -*-
# @Time : 2019/10/17 11:27
# @Software: PyCharm
# @author: 洋
# @File : course.py
from models.models import Model
from setting import COURSE_FILE


class Course(Model):
    title = ["id", "name", "money", "desc"]

    def __init__(self, name="", money=0, desc=""):
        super().__init__(COURSE_FILE)
        self.__name = name
        self.__money = money
        self.__desc = desc

    @property
    def name(self):
        return self.__name

    @property
    def money(self):
        return self.__money

    @property
    def desc(self):
        return self.__desc

    def __str__(self):
        return f"{self.id},{self.__name}, {self.__money}, {self.__desc}"

    def show_info(self):
        data = Course().find_all()
        for v in data:
            for j in v:
                print(j, end=" ")
            print("")
        return data

    # def create(self, data=None):
    #     if data is None:
    #         data = str(self).split(",")
    #     super().create(data)
