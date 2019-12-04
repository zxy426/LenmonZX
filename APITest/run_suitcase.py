# -*- coding:utf-8 -*-
# @Author:zxy

import unittest
import os
from readpath.handle_path import Reports_Path
from datetime import datetime
from libs.HTMLTestRunnerNew import HTMLTestRunner
from scripts.MyYuml import do_yuml
from readpath.handle_path import User_File_Path
from scripts.user import getuserinfo

from readpath.handle_path import Case_Path

# from Interface.cases import testqcd_01_register,testqcd_02_login




if not os.path.exists(User_File_Path):
    getuserinfo()

# 创建测试套件对象
suit = unittest.TestSuite()

# 将测试用例加载到测试套件中
#方法一：运行2个测试用例
# from Interface.cases import testqcd_01_register,testqcd_02_login
# load = unittest.TestLoader()
# suit.addTest(load.loadTestsFromModule(testqcd_01_register))
# suit.addTest(load.loadTestsFromModule(testqcd_02_login))


#方法二：通过目录来加载测试用例
suit=unittest.defaultTestLoader.discover(Case_Path)


#读取匹配文件写法
#添加时间戳可以生成根据时间段生成新的日志
result_path=do_yuml.read_yuml('report','report_name')+"_"+\
            datetime.strftime(datetime.now(),'%Y%m%d%H%M%S')+'.html'

result_path=os.path.join(Reports_Path,result_path)

runner = HTMLTestRunner(stream=open(result_path, 'wb'),#这个的意思是，读取yaml的配置文件，找到对应值并写到报告中
                         title = do_yuml.read_yuml('report','title'),
                         description = do_yuml.read_yuml('report','description'),
                         tester = do_yuml.read_yuml('report','tester'),)
# 运行测试套件
runner.run(suit)