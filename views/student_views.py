# -*- coding: utf-8 -*-
# @Time : 2019/10/17 10:18
# @Software: PyCharm
# @author: 洋
# @File : student_views.py
"""
学生视图
"""


#  学生视图
def student_view(user):
    while True:
        no = input("""
1.显示个人信息 2.选择课程 3.购买课程 4.上课 5.退出
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
