# -*- coding: utf-8 -*-
# @Time : 2019/10/17 11:02
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
            #  找到所有数据 -->二维数组
            data = self.find_all()
            #  通过字段名从title列表找到对应字段下标
            column_index = self.title.index(field_name.strip())
            #  通过枚举函数enumerate找到参数value所在的行
            #  从下标为1第二行开始遍历
            for i, row in enumerate(data[1:]):
                if row[column_index] == value:
                    #  将查询到的行号(i+1)及所在行数据(row) 以元组的形式添加到列表results中
                    results.append((i + 1, row))
            #  将列表results作为返回值返回
            return results
        except Exception as e:
            print(f"由于{e},造成查询失败！")
            #  查找失败则返回空列表
            return results

    def find_username(self, value):
        #  通过find方法查得用户名为value的行数据
        #  ——>返回值为内嵌元组的列表 元组中为数据所在行号及数据
        results = self.find("username", value)
        if results:
            #  返回results列表中的元组
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

    '''修改数据'''

    def __update(self, new_data):
        try:
            #  以"w"模式打开数据储存文件（哪个对象调用该方法便打开该对象所对应的file_name文件）
            with open(self.file_name, "w", encoding="utf-8", newline="") as f:
                csv_write = csv.writer(f)
                csv_write.writerows(new_data)
        except Exception as e:
            print(f"由于{e},造成修改失败！")
            return False
        return True

    def updata(self, row_index: int, field_name: str, value: str) -> bool:
        try:
            # 获取所有的原始数据
            data = self.find_all()
            # 判断row_index是否为整型且大于0小于数据总长
            if isinstance(row_index, int) and 0 < row_index < len(data):
                #  通过字段名在title列表中找到字段下标
                column_index = self.title.index(field_name)
                #  通过行号和字段下标修改值
                data[row_index][column_index] = value
            else:
                #  提示输入错误
                print("输入行数有误！")
                raise IndexError
        except Exception as e:
            #  打印造成异常的错误原因
            print(f"由于{e},造成修改失败！")
            #  给出返回值假
            return False
        else:
            #  将修改后的数据更新到数据中
            self.__update(data)

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
