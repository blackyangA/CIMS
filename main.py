# -*- coding: utf-8 -*-
# @Time : 2019/8/20 10:29
# @Software: PyCharm
# @author: 洋
# @File : main.py
from views.auth import login
from views.student_views import student_view
from views.teacher_views import *

if __name__ == '__main__':

    user = login()
    if user.auth == "stu":
        student_view(user)
    if user.auth == "tea":
        pass
    if user.auth == "admin":
        pass
