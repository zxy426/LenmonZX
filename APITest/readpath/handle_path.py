# -*- coding:utf-8 -*-
# @Author:zxy

'''
# 魔法变量
# __file__:代表当前文件在电脑中的绝对路径
# os.path.dirname:获取路径的父级目录
res = os.path.dirname(__file__)#获取当前路径的父级目录
res2 = os.path.dirname(res)  #在res的这个路径基础上在获取他的父级目录
base_dir = os.path.dirname(res2)#在res2的这个路径基础上在获取他的父级目录，以此可以得到这项目的根目录
# os.path.join: 做路径拼接的
'''
import os

# one_path=os.path.abspath(__file__)#获取当前文件的绝对路径
# two_path=os.path.dirname(one_path)#获取当前文件的上级文件的绝对路径
# three_path=os.path.dirname(two_path)#获取当前文件的上级文件的上级绝对路径
# four_path=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))#这个的意思是从里到外先获取当前文件的绝对路径，在逐级往上找，找到项目路径
# pass


#获取项目根目录所在路径
Project_Path=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#获取配置文件夹所在路径
Configs_Path=os.path.join(Project_Path,'configs')#利用os模块中的join方法来进行路径拼接
#获取配置文件所在路径下的文件路径
Configs_File_Path=os.path.join(Configs_Path,'api.yaml')
#获取日志文件所在目录路径
Logs_Path=os.path.join(Project_Path,'logs')

#获取测试报告文件所在目录路径
Reports_Path=os.path.join(Project_Path,'reports')

#获取excel文件所在目录路径
Datas_Path=os.path.join(Project_Path,'datas')

#获取用户信息的目录路径
User_File_Path=os.path.join(Configs_Path,'user.yaml')

#获取项目的测试用例目录的路径
Case_Path=os.path.join(Project_Path,'cases')

