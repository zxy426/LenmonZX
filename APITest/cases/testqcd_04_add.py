# -*- coding:utf-8 -*-
# @Author:zxy


import unittest
import json
from scripts.Read_excel_obj import ReadExcel
from scripts.MyLogger import do_log
from scripts.MyRequest import HandleRequest
from scripts.MyYuml import do_yuml
from libs.ddt import ddt, data
from scripts.handle_Parameterization import Parameterization


@ddt
class TestAdd(unittest.TestCase):
    excel = ReadExcel('add')
    case = excel.read_excel()

    @classmethod
    def setUpClass(cls):
        cls.request = HandleRequest()
        cls.request.add_hesders(do_yuml.read_yuml('request', 'version'))

    @classmethod
    def tearDownClass(cls):
        cls.request.close()

    @data(*case)
    def test_add(self, cases):
        # 第一步：准备数据
        # 获取用例行号
        row = cases.caseid + 1
        # 获取请求参数
        par = Parameterization.parmse_all(cases.datas)
        # 获取url
        add_url = do_yuml.read_yuml('request', 'url') + cases.url
        # 获取预期结果
        expected = cases.expected  # 因为用例是json格式的字符串通过loads转换为Python中的字典
        # 获取标题
        msg = cases.title

        # 第二步：发送加标请求，获取响应结果
        res = self.request.send(add_url, method=cases.method,data=par)
        actuall = res.json()  # 将响应结果转换为json格式的数据

        # 第三步：对比预期与实际结果
        try:
            self.assertEqual(expected, actuall.get('code'), msg=msg)
        except AssertionError as e:
            # 将用例的实际结果写到excel的result这一列中
            self.excel.write_excel(han=row, column=do_yuml.read_yuml('excel', 'result'),
                                   value=do_yuml.read_yuml('msg', 'fail_result'))

            do_log.error('{},断言的具体异常为{}\n'.format(msg, e))
            raise e
        else:
            if cases.caseid == 2:  # 默认登录接口登录成功
                # 取值登录的token
                token = actuall['data']['token_info']['token']
                # 更新请求头
                new_header = {'Authorization': 'Bearer ' + token}
                # 将更新的请求头加的默认的请求头中，有则更新，无则添加
                self.request.add_hesders(new_header)

            self.excel.write_excel(han=row, column=do_yuml.read_yuml('excel', 'result'),
                                   value=do_yuml.read_yuml('msg', 'success_result'))
            do_log.info('{},测试用例执行通过'.format(msg))

        finally:
            # 将响应的结果反写到excel的actall这一列中
            self.excel.write_excel(han=row, column=do_yuml.read_yuml('excel', 'case_result'),
                                   value=res.text)


if __name__ == '__main__':
    unittest.main()
