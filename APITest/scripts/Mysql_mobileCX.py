# -*- coding:utf-8 -*-
# @Author:zxy


# -*- coding:utf-8 -*-
# @Author:zxy

import random
from scripts.MyYuml import do_yuml
import pymysql


class Hadle_Mysql():

    def __init__(self):
        """
        如果你后面需要用到这个变量你就加self,否则不需要加
        """
        # 建立数据库连接
        self.conn = pymysql.connect(host=do_yuml.read_yuml('mysql','host'),  # mysql服务器ip或者域名
                                    user=do_yuml.read_yuml('mysql','user'),  # 数据库连接的用户名
                                    password=do_yuml.read_yuml('mysql','password'),  # 数据库连接密码
                                    db=do_yuml.read_yuml('mysql','db'),  # 数据库名字
                                    port=do_yuml.read_yuml('mysql','port'),  # 连接数据库端口号
                                    charset='utf8',  # 编码格式
                                    cursorclass=pymysql.cursors.DictCursor
                                    # 可以指定cursorclass为DictCursor, 那么返回的结果为字典或者嵌套字典的列表
                                    )
        # 创建游标对象
        self.curse = self.conn.cursor()

    # 综合一起简单写法
    # 如果你的2个函数有很多相同之处，你就可以写个跟type=True差不多的形式然后在判断就好，这样代码不繁琐
    def run(self, sql, args=None, type=False):
        self.curse.execute(sql, args)  # 执行sql
        self.conn.commit()  # 提交数据
        if type:
            return self.curse.fetchall()  # 获取多条数据结果,这个获取的值是元祖，# 可以指定cursorclass为DictCursor, 那么返回的结果为字典或者嵌套字典的列表
        else:
            return self.curse.fetchone()  # 获取单条数据结果

    def close(self):
        self.curse.close()
        self.conn.close()

    # 为什么会出现蓝色的波浪线，因为你定义函数没有用到self，属于静态的，可以使用静态方法

    @staticmethod
    def creat_phone():
        """
        随机生成11位手机号
        random.sample('0123456789',8),这个表示前面的序列类型我随机取值，取值几次，看后面的数字是几
        """
        return '188' + "".join(random.sample('0123456789', 8))

    #存在的手机号
    def exist_phone(self, phone):
        """
        判断手机号是否被注册了
        :param phone:
        :return:
        """
        sql = do_yuml.read_yuml('mysql','sql')  # 动态查询手机号
        if self.run(sql, args=[phone]):
            return True
        else:
            return False

   #不存在的手机号
    def notexist_phone(self):
        """
         随机生成一个在数据库中不存在的手机号
        :return:
        """
        while True:
            mobile=self.creat_phone()
            if not self.exist_phone(mobile):#调用存在手机的函数，判断，如果手机号不存在，就终止否则一直循环下去
                break
        return mobile

if __name__ == '__main__':
    # 当封装好了一个类之后, 要在下面自测一下
    sql_2 = "SELECT * FROM member LIMIT 0,10;"
    do_mysql = Hadle_Mysql()
    # print(do_mysql.creat_phone())
    # print(do_mysql.run(sql_2, type=True))  # 默认为False显示的是一条数据，如果想显示多条用Ture
    print(do_mysql.run(sql_2))
    do_mysql.close()
