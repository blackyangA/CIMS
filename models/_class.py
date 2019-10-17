# -*- coding: utf-8 -*-
# @Time : 2019/10/17 11:28
# @Software: PyCharm
# @author: 洋
# @File : _class.py
from models.models import Model
from setting import CLASS_FILE


class Class(Model):
    title = ["id", "name", "teacher", "course"]

    def __init__(self, name, teacher, course):
        super().__init__(CLASS_FILE)
        self.__name = name
        self.__teacher = teacher
        self.__course = course

    @property
    def name(self):
        return self.__name

    @property
    def teacher(self):
        return self.__teacher

    @property
    def course(self):
        return self.__course

    def __str__(self):
        return f"{self.id},{self.__name}, {self.__teacher}, {self.__course}"
