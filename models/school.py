# -*- coding: utf-8 -*-
# @Time : 2019/10/17 11:22
# @Software: PyCharm
# @author: 洋
# @File : school.py
from models.models import Model
from setting import SCHOOL_FILE


class School(Model):
    __slots__ = ("__name", "__address", "__city")
    title = ["id", "name", "address", "city"]

    def __init__(self, name, city, address):
        # 全部定义为私有属性
        super().__init__(SCHOOL_FILE)
        self.__name = name
        self.__city = city
        self.__address = address

    # def create(self, data=None):
    #     if data is None:
    #         data = self.title
    #     super().create(data)
    #
    # def insert_one(self, data=None):
    #     if data is None:
    #         data = str(self).split(",")
    #     super().insert_one(data)

    '''支持外部直接获取上述属性'''

    @property
    def name(self):
        return self.__name

    @property
    def address(self):
        return self.__address

    @property
    def city(self):
        return self.__city

    '''加一个str魔法方法 直接打印学校对象的时候 能显示学校信息'''

    def __str__(self):
        return f"{self.id}{self.__name},{self.__city},{self.__address}"
