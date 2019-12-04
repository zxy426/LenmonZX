# -*- coding:utf-8 -*-
# @Author:zxy




import unittest
import json

from scripts.Read_excel_obj import ReadExcel
from scripts.MyLogger import do_log
from scripts.MyRequest import HandleRequest
from scripts.MyYuml import do_yuml
from libs.ddt import ddt,data
from scripts.handle_Parameterization import Parameterization

@ddt
class TestLogin(unittest.TestCase):
    #获取用例数据
    excel=ReadExcel('login')
    case=excel.read_excel()
    do_log.info("读取用例数据成功")

    @classmethod
    def setUpClass(cls):
        cls.request=HandleRequest()
        cls.request.add_hesders(do_yuml.read_yuml('request','version'))

    @classmethod
    def tearDownClass(cls):
        cls.request.close()

    @data(*case)
    def test_login(self,cases):
#第一步：准备工作
    #获取用例行号
        row=cases.caseid+1
    #获取参数
        par=Parameterization.parmse_all(cases.datas)
    #获取url
        login_url=do_yuml.read_yuml('request','url')+cases.url
    #获取预期结果
        expected=json.loads(cases.expected,encoding='utf8')#因为用例是json格式的字符串通过loads转换为Python中的字典
    #获取用例标题
        msg=cases.title

#第二步:调用登录接口发送请求
        res=self.request.send(login_url,method=cases.method,data=par)
        actuall=res.json()

#第三步：预期与实际进行对比
        try:
            #用例中的多断言对比就是按照顺序，在异常处理中进行多次断言比较
            self.assertEqual(expected['code'],actuall['code'],msg=msg)
            self.assertEqual(expected['msg'],actuall['msg'],msg=msg)
        except AssertionError as e:
            # 将用例的实际结果写到excel的result这一列中
            self.excel.write_excel(han=row,
                                   column=do_yuml.read_yuml('excel','result'),
                                   value=do_yuml.read_yuml('msg','fail_result'))
            do_log.error("{},执行测试的具体的异常为：{}\n".format(msg, e))
            raise e

        else:
            self.excel.write_excel(han=row,
                           column=do_yuml.read_yuml('excel', 'result'),
                           value=do_yuml.read_yuml('msg', 'success_result'))
            do_log.info('{}，执行用例通过'.format(msg))
        finally:
            # 将响应的结果反写到excel的actall这一列中
            self.excel.write_excel(han=row, column=do_yuml.read_yuml('excel', 'case_result'), value=res.text)


if __name__ == '__main__':
    unittest.main()








