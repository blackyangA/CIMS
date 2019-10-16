# -*- coding: utf-8 -*-
# @Time : 2019/8/20 10:29
# @Software: PyCharm
# @author: 洋
# @File : models.py
import abc, os, csv, datetime
from setting import *
from unit import get_age


#  模型/数据抽象类实现对数据的增删该查
class Model(metaclass=abc.ABCMeta):
    title = ["id"]

    # def __new__(cls, *args, **kwargs):
    #     pass
    """
    抽象类 用于对文件进行操作
    file_name
    将数据存储到文件
    修改文件内容
    删除中文内容
    查询文件中的内容
    """

    @abc.abstractmethod
    def __init__(self, file_name):
        self.file_name = file_name
        if os.path.exists(file_name):
            self.id = self.id_auto_increment()

    '''创建文件'''

    def create(self, data=None):
        #  data为列表
        if data is None:
            data = self.title
        if os.path.exists(self.file_name):
            #  self.__file_name 显示整个路径不好看
            #  用 os.path.basename(self.__file_name) 把路径最后的文件名切出来
            print(f"{os.path.basename(self.file_name)}文件已经存在!")
            return
        else:
            with open(self.file_name, "w", encoding="utf-8", newline="") as f:
                # newline=""防止csv文件输入数据自动空行
                if data is None:
                    pass
                else:
                    csv_write = csv.writer(f)
                    csv_write.writerow(data)

    '''删除文件'''

    def drop(self):
        os.remove(self.file_name)

    '''插入一条数据'''

    def insert_one(self, data=None):
        if data is None:
            data = str(self).split(",")
        #  line是列表
        if os.path.exists(self.file_name):
            with open(self.file_name, "a", encoding="utf-8", newline="") as f:
                # newline=""防止csv文件输入数据自动空行
                if data is None:
                    pass
                else:
                    csv_write = csv.writer(f)
                    csv_write.writerow(data)
        else:
            print(f"{os.path.basename(self.file_name)}不存在！请先创建！")

    '''插入多条数据'''

    def insert_many(self, data):
        if os.path.exists(self.file_name):
            with open(self.file_name, "a", encoding="utf-8", newline="") as f:
                # newline=""防止csv文件输入数据自动空行
                if data is None:
                    pass
                else:
                    csv_write = csv.writer(f)
                    csv_write.writerows(data)
        else:
            print(f"{os.path.basename(self.file_name)}不存在！请先创建！")

    '''查询所有数据'''

    def find_all(self):
        if os.path.exists(self.file_name):
            with open(self.file_name, encoding="utf-8") as f:
                data = list(csv.reader(f))
            return data

    '''根据条件查询数据'''

    def find(self, field_name, value):
        results = []
        try:
            #  找到所有数据
            data = self.find_all()
            #  通过字段名找到字段下标
            column_index = self.title.index(field_name.strip())
            # print(column_index)
            for i, row in enumerate(data[1:]):
                #  data[1:] 让for循环从下标一开始检索
                if row[column_index] == value:
                    results.append((i + 1, row))
            return results
        except Exception as e:
            print(f"由于{e},造成查询失败！")
            return results

    def find_username(self, value):
        results = self.find("username", value)
        if results:
            return results[0]

    '''根据条件删除数据'''

    def delete(self, field_name, value):
        try:
            #  找到所有数据
            data = self.find_all()
            #  通过字段名找到字段下标
            column_index = self.title.index(field_name)
            for i, row in enumerate(data[1:]):
                #  data[1:] 让for循环从下标一开始检索
                if row[column_index] == value:
                    #  如果i=0那么要删除的是第二行
                    data.pop(i + 1)
        except Exception as e:
            print(f"由于{e},造成查询失败！")
        else:
            self.__update(data)

    def __update(self, new_data):
        """
        将新的数据覆盖旧的文件
        :param new_data:
        :return:
        """
        try:
            with open(self.file_name, "w", encoding="utf-8", newline="") as f:
                csv_write = csv.writer(f)
                csv_write.writerows(new_data)
        except Exception as e:
            print(f"由于{e},造成修改失败！")
            return False
        return True

    '''修改数据'''

    def updata(self, row_index: int, field_name: str, value: str) -> bool:
        """
        更新数据
        :param row_index: 行的下标
        :param field_name: 字段名
        :param  value:更新的值
        :return: True/False
        """
        try:
            # 获取所有的原始数据
            data = self.find_all()
            if isinstance(row_index, int) and 0 < row_index < len(data):
                #  通过字段名找到字段下标
                column_index = self.title.index(field_name)
                #  通过行号和字段下标修改值
                data[row_index][column_index] = value
            else:
                print("输入行数有误！")
                raise IndexError
        except Exception as e:
            print(f"由于{e},造成修改失败！")
            #  保存修改后的值
            return False
        else:
            self.__update(data)
            #  # 当修改成功时
            # # 覆盖保存修改后的值
            # try:
            #     with open(self.file_name, "w", encoding="utf-8", newline="") as f:
            #         csv_write = csv.writer(f)
            #         csv_write.writerows(data)
            # except Exception as e:
            #     print(f"由于{e},造成修改失败！")
            #     return False
            # return True

    '''实现id自动增长'''

    def id_auto_increment(self):
        """
        获取下一个id
        :return: int
        """
        id_field = (self.find_all()[-1][0])
        if id_field.isdigit():
            next_id = int(id_field) + 1
        else:
            next_id = 1
        return next_id

    '''验证唯一值'''

    def unique(self, field_name, value):
        try:
            # 1.找标签下标
            index = self.title.index(field_name)
            # 2.获取数据
            data = self.find_all()
            for row in data:
                if row[index] == value:
                    #  找到了返回False
                    return False
            else:
                return True
        except Exception as e:
            print(e)


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


#  用户抽象类
class User(Model):
    title = ["id", "username", "password", "user", "birthday", "sex", "phone", "class", "course", "school_name", "auth",
             "auth_id", "create_date", "update_date"]

    # def __new__(cls, *args, **kwargs):
    #     pass
    '''
        def __init__(self, username="", password="", name="", birthday="", sex="", phone="", _class=None,
                 course=None,
                 school_name=None,
                 auth=None,
                 auth_id=None,
                 create_date=None,
                 ):
        super().__init__(USER_FILE)
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
        self.create_date = create_date
        self.update_date = None
        if self.create_date is None:
            self.create_date = datetime.datetime.now()
        else:
            self.update_date = datetime.datetime.now()
    '''

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
        # new_data = []
        # for i, row in enumerate(data):
        #     if self.unique_username(row[1]):
        #         new_data.append(row)
        #     else:
        #         print(f"{row[1]}", "用户名已存在，不能重复注册！")
        # super().insert_many(new_data)
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

    # def create(self, data=None):
    #     if data is None:
    #         data = self.title
    #     super().create(data)
    #
    # def insert_one(self, line=None):
    #     if line is None:
    #         line = str(self).split(",")
    #     super().insert_one(line)
    def __str__(self):
        return f"{self.id},{self.username},{self.password},{self.name},{self.birthday},{self.sex},{self.phone}," \
            f"{self._class},{self.course},{self.school_name},{self.auth}," \
            f"{self.auth_id},{self.create_date},{self.update_date}"


class Student(User):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    #  选择课程
    def select_course(self):
        while True:
            cou = Course().show_info()
            no = input("请选择课程：")
            try:
                self.__course = cou[int(no)][1]
            except Exception as e:
                print(e, "选择错误请重新选择！")
            else:
                row_index = self.find_username(self.username)[0]
                self.updata(row_index, "course", self.__course)
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


class Teacher(User):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Admin(User):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

# school = School("人通", "空港天保公寓", "天津")
# user = User(username="zj1007", password="123", name="zj", age=20, sex="男", phone="15023332345", _class="TJ190501T",
#             course="大数据",
#             school_name="人通", auth="tea", auth_id="0024")
# # user.insert_one()
#
# if __name__ == '__main__':
#     user.insert_one()
