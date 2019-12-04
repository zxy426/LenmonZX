# -*- coding:utf-8 -*-
# @Author:zxy



import unittest
import json
from scripts.Read_excel_obj import ReadExcel
from libs.ddt import ddt, data
from scripts.MyYuml import do_yuml
from scripts.MyLogger import do_log
from scripts.handle_Parameterization import Parameterization
from scripts.MyRequest import HandleRequest


@ddt
class TestRegister(unittest.TestCase):
    # 读取excel数据
    excel = ReadExcel('register')
    case = excel.read_excel()
    do_log.debug('读取excel用例数据成功')

    # 第一步：准备所有要用的数据
    # 调用封装的请求，才可以发送请求，可以在用例发生时候调用，调用结束之后一定要关闭
    @classmethod
    def setUpClass(cls):  # 所有用例执行前, 会被调用一次
        cls.do_request = HandleRequest() # 创建MyRequest对象
        cls.do_request.add_hesders(do_yuml.read_yuml('request', 'version'))

    @classmethod
    def tearDownClass(cls):  # 所有用例执行结束之后, 会被调用一次
        cls.do_request.close()  # 用例测试结束，关闭会话释放内存

    @data(*case)
    def test_register(self,cases):

    #获取用例的行号
        row=cases.caseid+1
    #获取用例的参数
        par=Parameterization.parmse_all(cases.datas)
    #获取用例的url
        register_url=do_yuml.read_yuml('request','url')+cases.url
    #获取用例的期望结果
        expected=cases.expected
    #获取用例标题
        msg=cases.title

    #第二步：调用请求接口，发送请求，执行注册
        res=self.do_request.send(url=register_url,method=cases.method,data=par,is_json=True)#这里的method=cases.method跟is_json=True因为是默认参数，可以省略不写
        data_json=res.json()#将响应报文转化为json的字典数据

    #第三步：预期与实际结果进行比较
        try:
            # assertEqual第三个参数为用例执行失败之后的提示信息
            # assertEqual第一个参数为期望值, 第二个参数为实际值
            self.assertEqual(expected,data_json['code'],msg=msg)#预期与实际的2个code进行对比
        except AssertionError as e:
            #将用例的实际结果写到excel的result这一列中
            self.excel.write_excel(han=row,
                                   column=do_yuml.read_yuml('excel','result'),
                                   value=do_yuml.read_yuml('msg','fail_result'))
            do_log.error("{},执行测试的具体的异常为：{}\n".format(msg,e))
            raise e
        else:
            # 将用例的实际结果写到excel的result这一列中
            self.excel.write_excel(han=row,
                                   column=do_yuml.read_yuml('excel', 'result'),
                                   value=do_yuml.read_yuml('msg', 'success_result'))
            do_log.info('{}，执行用例通过'.format(msg))
        finally:
            # 将响应的结果反写到excel的actall这一列中
            self.excel.write_excel(han=row, column=do_yuml.read_yuml('excel', 'case_result'), value=res.text)





if __name__ == '__main__':
    """
    运行这个文件要么这main函数下右击调试运行，要么鼠标放到类上右击运行否则会报错
    """
    unittest.main()




















