# -*- coding:utf-8 -*-
# @Author:zxy

import unittest
from libs.ddt import ddt,data
from scripts.Read_excel_obj import ReadExcel
from scripts.MyRequest import HandleRequest
from scripts.Mysql_mobileCX import Hadle_Mysql
from scripts.MyYuml import do_yuml
from scripts.handle_Parameterization import Parameterization
from scripts.MyLogger import do_log
import json

@ddt
class TestRecharge(unittest.TestCase):
    excel=ReadExcel('recharge')#获取excel中充值的表单用例列表
    case=excel.read_excel()#读取用例数据

    @classmethod
    def setUpClass(cls):
        cls.request=HandleRequest()
        cls.request.add_hesders(do_yuml.read_yuml('request','version'))
        cls.do_sql=Hadle_Mysql()

    @classmethod
    def tearDownClass(cls):
        cls.request.close()
        cls.do_sql.close()

    @data(*case)
    def test_rechargd(self,cases):
##第一步：准备工作
    #获取用例行号
        row=cases.caseid+1
    #获取参数
        par=Parameterization.parmse_all(cases.datas)
    #获取url
        rechargd_url=do_yuml.read_yuml('request','url')+cases.url
    #获取预期结果
        expected=cases.expected
    #获取用例标题
        msg=cases.title
        check_sql = cases.check_sql  # 取出check_sql
        if check_sql:   # 如果check_sql不为空, 则代表当前用例需要进行数据校验
            check_sql = Parameterization.parmse_all(check_sql)  # 将check_sql进行参数化，根据sql查找数据库充值前的金额
            mysql_data = self.do_sql.run(check_sql)   # 执行sql
            amount_before = float(mysql_data['leave_amount'])    # 不是float类型, 也不是int类型, 是decimal类型
            # 由于使用float转化之后的数, 有可能小数位数超过2位, 需要使用round保留2位小数
            amount_before = round(amount_before, 2)

#第二步:调用充值接口发送请求
        res=self.request.send(rechargd_url,method=cases.method,data=par)
        actuall=res.json()

#第三步：预期与实际进行对比
        try:
            #用例中的多断言对比就是按照顺序，在异常处理中进行多次断言比较
            self.assertEqual(expected,actuall['code'],msg=msg)
            if check_sql:
                check_sql = Parameterization.parmse_all(check_sql)  # 前面的断言成功，获取充值后的金额
                mysql_data = self.do_sql.run(check_sql)  # 执行sql
                amount_after = round(float(mysql_data['leave_amount']),2)  # 不是float类型, 也不是int类型, 是decimal类型
                actual_amount=round(amount_after - amount_before,2)#充值后的金额减去充值钱的金额获取差值，保留2位小数进行断言

                one_dict = json.loads(par, encoding='utf8')#将json的字符串转化为Python的字典
                recharge_amount = one_dict['amount']#获取充值的金额
                self.assertEqual(recharge_amount,actual_amount,msg="实际充值金额与数据库存储金额不符")
        except AssertionError as e:
            # 将用例的实际结果写到excel的result这一列中
            self.excel.write_excel(han=row,
                                   column=do_yuml.read_yuml('excel','result'),
                                   value=do_yuml.read_yuml('msg','fail_result'))
            do_log.error("{},执行测试的具体的异常为：{}\n".format(msg, e))
            raise e

        else:
            # 默认充值接口的第二条测试用例登录成功
            if cases.caseid == 2:
                # 取值登录的token
                token = actuall['data']['token_info']['token']
                # 更新header的请求头
                new_header = {'Authorization': 'Bearer ' + token}
                self.request.add_hesders(new_header)
            # 将用例的实际结果写到excel的result这一列中
            self.excel.write_excel(han=row,
                           column=do_yuml.read_yuml('excel', 'result'),
                           value=do_yuml.read_yuml('msg', 'success_result'))
            do_log.info('{}，执行用例通过'.format(msg))
        finally:
            # 将响应的结果反写到excel的actall这一列中
            self.excel.write_excel(han=row, column=do_yuml.read_yuml('excel', 'case_result'), value=res.text)


if __name__ == '__main__':
    unittest.main()