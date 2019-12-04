# -*- coding:utf-8 -*-
# @Author:zxy

''''
这里的封装用是requests中自带的类方法seesion
seesion中有个request方法

request(self, method, url,
            params=None, data=None, headers=None, cookies=None, files=None,
            auth=None, timeout=None, allow_redirects=True, proxies=None,
            hooks=None, stream=None, verify=None, cert=None, json=None)
除了 method, url,是必须要传值外，其他根据你自己的需求可传，可不传，所有这些不是必填字段可以用**kwargs不定长参数来参数定义
seesion可以理解为会话，运用这个在调用的时候，就像在浏览器中发请求一样，系统会自动把你的cook带上

根据上课老师的讲解，如果你的封装是根据源码来的，如果你看懂源码，封装对于你来说就是很容易的
'''

import requests
import json


class HandleRequest:

    def __init__(self):
        # 创建seesion会话对象，seesion为requests库中的一个类
        # 查看地址：python37——lib——sit-packages——requests——seesions
        self.session = requests.Session()

    def add_hesders(self, headers):
        """
        添加公共请求头
        :param headers: 需要添加的请求头, 为字典类型
        # Session会话对象中的headers类似于一个字典
        """

        # 可以将待添加的请求头字典与self.one_session.headers中的请求头(类似字典)进行合并覆盖,有就覆盖用你定义的，没有就用默认的
        self.session.headers.update(headers)

    def send(self, url, method="post", data=None, is_json=True, **kwargs):

        """
        :param url: url地址
        :param method: 请求方法, 通常为get、post、put、delete、patch
        :param data: 传递的参数, 可以传字典、json格式的字符串、字典类型的字符串, 默认为None
        :param is_json: 是否以json的形式来传递参数, 如果为True, 则以json形式来传, 如果为False则以www-form形式来传, 默认为True
        :param kwargs: 可变参数, 可以接收关键字参数, 如headers、params、files等
        :return: None 或者 Response对象
                """
        # data可以为如下三种类型：
        # data = {"name": '可优', 'gender': True}       # 字典类型
        # data = '{"name": "可优", "gender": true}'     # json格式的字符串
        # data = "{'name': '优优', 'gender': True}"     # 字典类型的字符串

        # 将method中的数据全部转化为小写
        method = method.lower()
        if isinstance(data, str):  # 如果data的数据是字符串
            try:
                data = json.loads(data)  # 将json格式的字符串转化为Python中的字典或者是嵌套字典的列表
            except AssertionError as e:
                """
                 if not isinstance(cookies, cookielib.CookieJar):
                       cookies = cookiejar_from_dict(cookies)
                """
                # isinstance这个源码中如果结果为False会把数据转化为字典，在利用eval进行脱衣把他转为Python中的表达式，这里是字典
                print("不是字符串怎么处理")
                data = eval(data)
        if method == "get":
            res = self.session.request(method, url, params=data, **kwargs)
        elif method in ("post", "put", "delete", "patch"):
            if is_json:  # 是否以json的形式来传递参数, 如果为True, 则以json形式来传, 如果为False则以www-form形式来传, 默认为True
                res = self.session.request(method, url, json=data, **kwargs)
            else:
                res = self.session.request(method, url, data=data, **kwargs)
        else:
            res = None
            print("不支持{}请求方法".format(method))
        return res

    def close(self):
        self.session.close()


if __name__ == '__main__':
    # 1：需要的请求参数
    login_url = "http://api.lemonban.com/futureloan/member/login"
    recharge_url = "http://api.lemonban.com/futureloan/member/recharge"
    withdraw_url = "http://api.lemonban.com/futureloan/member/withdraw"

    # 需要的参数
    login_data = {"mobile_phone": "18100000001", "pwd": "11111111"}
    headers = {"X-Lemonban-Media-Type": "lemonban.v2", "Content-Type": "application/json"}

    # 登录发送请求
    do_request = HandleRequest()  # 创建对象
    do_request.add_hesders(headers)  # 添加公共的请求头
    login_res = do_request.send(login_url, 'post', data=login_data, headers=headers)
    json_datas = login_res.json()  # 将响应体的数据转化为字典
    member_id = json_datas['data']['id']  # 根据字典的key来取值
    token = json_datas['data']['token_info']['token']

    # 充值
    # 请求参数
    recharge_data = {"member_id": member_id, "amount": "10000"}
    # 登录之后的操作都必须要加token的，否则会报鉴权错误
    token_header = {"Authorization": "Bearer " + token}
    # 将token加到headers中
    do_request.add_hesders(token_header)

    # 充值发送请求
    recharge_res = do_request.send(recharge_url, 'post', data=recharge_data)

    # 提现
    # 请求数据
    withdraw_data = {"member_id": "18100000001", "amount": "10"}

    # 提现发送请求
    withdraw_res = do_request.send(withdraw_url, 'post', data=withdraw_data)
    pass
