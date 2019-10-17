# -*- coding: utf-8 -*-
# @Time : 2019/10/17 11:50
# @Software: PyCharm
# @author: 洋
# @File : student.py
from models.user import User
from models.course import Course
from setting import PAY_COST
import csv


class Student(User):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    #  选择课程
    def select_course(self):
        while True:
            cou = Course().show_info()
            no = input("请选择课程：")
            try:
                self.course = cou[int(no)][1]
            except Exception as e:
                print(e, "选择错误请重新选择！")
            else:
                row_index = self.find_username(self.username)[0]
                self.updata(row_index, "course", self.course)
                break

    #  支付功能 购买课程
    def __pay(self, money):
        while True:
            pay_money = float(input(f"请支付{money}元"))
            if pay_money >= money:
                print("支付成功，您已成功购买该课程!")
                pay_info = [self.username, money]
                with open(PAY_COST, "a", encoding="utf-8") as f:
                    csv_obj = csv.writer(f)
                    csv_obj.writerow(pay_info)
                    return True

    def is_pay(self):
        with open(PAY_COST) as f:
            data = list(csv.reader(f))
        for row in data:
            if self.username in row:
                return True
            else:
                return False

    def pay(self):
        # 1.查询课程金额
        if self.is_pay():
            print("该课程您已购买,请勿重复操作！")
            return True
        if self.course is not None or self.course != "None":
            try:
                cou = Course().find("name", self.course)
                money = float(cou[0][1][2])
                self.__pay(money)
            except Exception as e:
                print(e)
        else:
            print("请先选择课程！")
            return False
