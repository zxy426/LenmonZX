# -*- coding:utf-8 -*-
# @Author:zxy

import openpyxl
import os
from readpath.handle_path import Datas_Path
from scripts.MyYuml import do_yuml


class CaseDate:
    pass


class ReadExcel(object):
    def __init__(self, sheet,filename=None):  # 初始化
        """
        对传入的文件进行判端，如果不传文件名，默认读取我定义的文件
        否则使用，你重新定义的新的文件
        :param sheet:
        :param filename:
        """
        if filename is None:
            self.filename=os.path.join(Datas_Path, do_yuml.read_yuml('excel', 'case_path'))
        else:
            self.filename = filename
        self.sheet = sheet

    def open_excel(self):
        self.wb = openpyxl.load_workbook(self.filename)  # 打开excel
        self.sh = self.wb[self.sheet]  # 调用打开excel的对象，再来打开你要操作的表单

    def read_excel(self):

        self.open_excel()  # 调用打开excel的方法打开excel
        rows = list(self.sh.rows)  # 这个的结果是元祖嵌套列表的格式[(),()]
        # print(rows)
        res = []
        title = [a.value for a in rows[0]]  # 遍历所有行的第一列，并把他的值取出来
        for b in rows[1:]:  # 遍历除了第一行之外的所以内容，放到b中，结果是元祖格式
            # print(b)
            b1 = [c.value for c in b]  # 这个遍历出来的c是一个个的格子，c.value获取格子的值
            b2 = list(zip(title, b1))  # 进行聚合打包，并转化为列表格式
            casedata = CaseDate()
            for d in b2:
                setattr(casedata, d[0], d[1])
            res.append(casedata)
        self.wb.close()  # 关闭工作簿
        return res

    def write_excel(self, han, column, value):  # 把测试结果回写到excel中，不知道行，列，值给他定义一个
        # 打开excel
        self.open_excel()
        # 写入数据，到excel的行中
        self.sh.cell(row=han, column=column, value=value)
        # 保存数据到excel中
        self.wb.save(self.filename)
        # 关闭excel
        self.wb.close()


if __name__ == '__main__':
    # read=ReadExcel('case01.xlsx','register')#创建ReadExcel的对象，并且传参
    filename = os.path.join(Datas_Path, do_yuml.read_yuml('excel', 'case_path'))
    read = ReadExcel(filename, 'invest')
    cases = read.read_excel()  # 用对象来调用类里面的类方法
    print(cases)
