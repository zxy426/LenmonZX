# -*- coding:utf-8 -*-
# @Author:zxy


import re
import pandas as pd
from scripts.Mysql_mobileCX import Hadle_Mysql
from scripts.MyYuml import MyYuml
from readpath.handle_path import User_File_Path
from scripts.Read_excel_obj import ReadExcel




class Parameterization(object):
    notexist = r'\${notexit_tel}'  # 不存在的手机号
    notuserid = r'{notinvest_user_id}'  # 不存在的用户id
    notexisted_loan_id=r'{not_existed_loan_id}'

    invest_tel = r'{invest_tel}'  # 投资人电话
    invest_pwd = r'{pwd}'  # 投资人密码
    invest_id = r'{invest_user_id}'  # 投资人id

    # 借款人相关正则表达式
    borrow_id= r'{borrow_user_id}'  # 借款用户id
    borrow_tel = r'{borrow_user_tel}'  # 借款人手机号
    borrow_pwd= r'{borrow_user_pwd}'  # 借款人密码

    # 管理员相关正则表达式
    admin_tel = r'{admin_user_tel}'  # 管理员手机号
    admin_pwd = r'{admin_user_pwd}'  # 管理员密码

    loan_id_pattern=r'{loan_id}'  #加标项目id

    user_info = MyYuml(User_File_Path)  # 定义为类属性方便后面的调用



    @classmethod
    def parmse_all(cls, content):
        """
        参数化手机号
        search：如果content原始字符串中能匹配{not_existed_tel}, 则if条件为True, 否则if为False
        下面content的意思是，如果内容匹配正确覆盖content使用新值，匹配失败使用原content
        :param content:
        :return:
        """
        if re.search(cls.notexist, content):
            do_sql = Hadle_Mysql()
            content = re.sub(cls.notexist, do_sql.notexist_phone(), content)  # 把写的正则的手机号替换为我定义的不存在的手机号
            do_sql.close()

        if re.search(cls.invest_tel, content):
            # 投资人手机号替换
            # user_info=MyYuml(User_File_Path)因为后面的操作会经常用到这个用户信息所以可以定义为类属性，方便后面的调用
            content = re.sub(cls.invest_tel,
                             cls.user_info.read_yuml('investor', 'mobile_phone'),
                             content)  # 把用例中的投资人号码替换为yaml文件中投资人手机号

        if re.search(cls.invest_pwd, content):
            # 投资人密码替换
            # user_info=MyYuml(User_File_Path)因为后面的操作会经常用到这个用户信息所以可以定义为类属性，方便后面的调用
            content = re.sub(cls.invest_pwd,
                             cls.user_info.read_yuml('investor', 'pwd'),
                             content)  # 把用例中的投资人密码替换为yaml文件中投资人密码

        if re.search(cls.invest_id, content):
            # 投资人id替换
            # user_info=MyYuml(User_File_Path)因为后面的操作会经常用到这个用户信息所以可以定义为类属性，方便后面的调用
            invest_user_id = cls.user_info.read_yuml('investor', 'id')
            content = re.sub(cls.invest_id,
                             str(invest_user_id),
                             content)  # 把用例中的投资人密码替换为yaml文件中投资人密码

        if re.search(cls.notuserid, content):
            # 用户id不存在
            do_sql = Hadle_Mysql()
            sql = "SELECT id FROM member ORDER BY id DESC LIMIT 0,1;"
            not_existed_id =do_sql.run(sql).get('id') + 1# 获取最大的用户id + 1
            content = re.sub(cls.notuserid,
                             str(not_existed_id),
                             content)  # 把用例中的不存在的用户id替换为数据库中最大用户id+1

            do_sql.close()

        if re.search(cls.borrow_id, content):
            # 借款人id替换
            # user_info=MyYuml(User_File_Path)因为后面的操作会经常用到这个用户信息所以可以定义为类属性，方便后面的调用
            borrow_user_id = cls.user_info.read_yuml('borrow', 'id')
            content = re.sub(cls.borrow_id,
                             str(borrow_user_id),
                             content)  # 把用例中的借款人id替换为yaml文件中投借款人id

        if re.search(cls.borrow_tel, content):
            # 借款人电话号码替换
            # user_info=MyYuml(User_File_Path)因为后面的操作会经常用到这个用户信息所以可以定义为类属性，方便后面的调用
            borrow_user_tel = cls.user_info.read_yuml('borrow', 'mobile_phone')
            content = re.sub(cls.borrow_tel,
                             borrow_user_tel,
                             content)  # 把用例中的借款人电话号码替换为yaml文件中借款人电话号码

        if re.search(cls.borrow_pwd, content):
            #借款人密码替换
            # user_info=MyYuml(User_File_Path)因为后面的操作会经常用到这个用户信息所以可以定义为类属性，方便后面的调用
            borrow_user_pwd = cls.user_info.read_yuml('borrow', 'pwd')
            content = re.sub(cls.borrow_pwd,
                             borrow_user_pwd,
                             content)  # 把用例中的借款人密码替换为yaml文件中借款人密码

        if re.search(cls.admin_tel, content):
            # 管理员手机号替换
            # user_info=MyYuml(User_File_Path)因为后面的操作会经常用到这个用户信息所以可以定义为类属性，方便后面的调用
            admin_user_tel = cls.user_info.read_yuml('admin', 'mobile_phone')
            content = re.sub(cls.admin_tel,
                             admin_user_tel,
                             content)  # 把用例中的管理员手机号替换为yaml文件中管理员

        if re.search(cls.admin_pwd, content):
            #管理员密码替换
            # user_info=MyYuml(User_File_Path)因为后面的操作会经常用到这个用户信息所以可以定义为类属性，方便后面的调用
            admin_user_pwd = cls.user_info.read_yuml('admin', 'pwd')
            content = re.sub(cls.admin_pwd,
                             admin_user_pwd,
                             content)  # 把用例中的管理员密码替换为yaml文件中管理员密码
         #loan_id替换
        if re.search(cls.loan_id_pattern,content):
            loan_id=getattr(cls,'loan_id')#通过动态属性获取loan_id(我们先从投资的用例中通过setter反射出loan_id,在从封装的参数类中来参数化)
            content=re.sub(cls.loan_id_pattern,str(loan_id),content)
            # content = re.sub(cls.loan_id_pattern, str('5260'), content)

        if re.search(cls.notexisted_loan_id, content):
            # 不存在的项目id
            do_sql = Hadle_Mysql()
            sql = "SELECT id FROM loan ORDER BY id DESC LIMIT 0,1;"
            not_existed_loan_id =do_sql.run(sql).get('id') + 1
            content = re.sub(cls.notexisted_loan_id,
                             str(not_existed_loan_id),
                             content)

        return content


if __name__ == '__main__':
    # # 注册接口参数化
    # res = '{"mobile_phone": "${notexit_tel}","pwd": "12345611","type":"1","reg_name":"小西斯"}'
    # print(Parameterization.parmse_all(res))
    #
    # # 登录接口参数化
    # res1 = '{"mobile_phone":"{invest_tel}","pwd":"{pwd}"}'
    # print(Parameterization.parmse_all(res1))
    # pass

    excel=ReadExcel('invest')
    data=excel.read_excel()

    for cases in data:
        value=Parameterization.parmse_all(cases.datas)
        print(value)

    pass
