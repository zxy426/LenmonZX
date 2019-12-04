# -*- coding:utf-8 -*-
# @Author:zxy


import unittest
import json
from scripts.Read_excel_obj import ReadExcel
from libs.ddt import ddt, data
from scripts.MyRequest import HandleRequest
from scripts.Mysql_mobileCX import Hadle_Mysql
from scripts.MyYuml import do_yuml
from scripts.handle_Parameterization import Parameterization
from scripts.MyLogger import do_log


@ddt
class TestInvest(unittest.TestCase):
    excel = ReadExcel('invest')  # 获取excel中要测的测试用例表单
    case = excel.read_excel()  # 读取测试用例数据
    do_log.info("测试用例开始执行")

    @classmethod
    def setUpClass(cls):
        cls.request = HandleRequest()  # 创建请求对象
        cls.request.add_hesders(do_yuml.read_yuml('request', 'version'))  # 读取yaml文件获取请求数据的头更新到默认的请求头中
        cls.do_sql = Hadle_Mysql()  # 创建执行sql的对象

    @classmethod
    def tearDownClass(cls):
        cls.request.close()  # 调用请求结束之后一定要记得关闭释放内存
        cls.do_sql.close()  # 执行sql结束之后一定要记得关闭释放内存

    @data(*case)
    def test_invest(self, cases):

        # 第一步：准备数据
        # 获取用例行号
        row = cases.caseid + 1
        # 获取请求参数
        par = Parameterization.parmse_all(cases.datas)
        # 获取url
        invest_url = do_yuml.read_yuml('request', 'url') + cases.url
        # 获取预期结果
        expected = cases.expected
        # 获取标题
        msg = cases.title

        # 第二步：调用投资接口，进行投资
        res = self.request.send(invest_url, method=cases.method, data=par)
        actuall = res.json()
        # 第三步：比对预期与实际结果
        try:
            self.assertEqual(expected, actuall.get('code'), msg=msg)
        except AssertionError as e:
            # 将用例的实际结果写到excel的result这一列中
            self.excel.write_excel(han=row, column=do_yuml.read_yuml('excel', 'result'),
                                   value=do_yuml.read_yuml('msg', 'fail_result'))

            do_log.error('{},执行测试用例的具体异常为{}'.format(msg, e))
            raise e
        else:

            if 'token_info' in res.text:
                token = actuall['data']['token_info']['token']  # 在获取响应结果的字典数据，从中查找token_info
                new_header = {"Authorization": "Bearer " + token}  # 获取请求的token值
                self.request.add_hesders(new_header)  # 将获取到的token值加更新到请求头中

            # check_sql=cases.check_sql
            # if check_sql:
            #     sql=Parameterization.parmse_all(check_sql)
            #     res_sql=self.do_sql.run(sql)
            #     loan_id=res_sql['id']
            #     setattr(Parameterization,'a',loan_id)


            # # 获取loan_id
            if cases.caseid == 2:
                loan_id = actuall.get('data').get('id')  # 获取响应的json数据中的data,再获取它下面的id
                setattr(Parameterization, 'loan_id', loan_id)  ## 动态创建属性的机制, 来解决接口依赖的问题

            # 将用例的实际结果写到excel的result这一列中
            self.excel.write_excel(han=row, column=do_yuml.read_yuml('excel', 'result'),
                                   value=do_yuml.read_yuml('msg', 'success_result'))
            do_log.info('{},测试用例执行成功'.format(msg))
        finally:
            # 将响应的结果反写到excel的actall这一列中
            self.excel.write_excel(han=row, column=do_yuml.read_yuml('excel', 'case_result'),
                                   value=res.text)


if __name__ == '__main__':
    """如果要运行这个测试用例一定要在这里右击运行，别的地方会报错，也有可能会导致你的excel损坏"""
    # unittest.main()

