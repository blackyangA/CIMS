# -*- coding: utf-8 -*-
# @Time : 2019/10/17 11:53
# @Software: PyCharm
# @author: 洋
# @File : teacher.py
from models.user import User


class Teacher(User):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
