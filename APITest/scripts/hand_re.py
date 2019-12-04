# -*- coding:utf-8 -*-
# @Author:zxy

import re

from scripts.Mysql_mobileCX import Hadle_Mysql
"""
# re.match方法
# a. 正则表达式中一定要加r, 如果有些字符有特殊含义, 需要在前面加一个\
# re_str = r'{not_existed_tel}'
# b. match方法第一个参数为正则表达式, 第二个参数为待查询的字符串
# c. match方法只能从头开始匹配
# d. 如果匹配不上, 会返回None
# f. 如果能匹配上, 会返回Match对象
# mtch = re.match(r'${not_existed_tel}', one_str)
# 可以使用mtch.group()获取匹配成功之后的值
# mtch = re.match(r'{"mobile_phone": "{not_existed_tel}', one_str)

# 3. re.search方法
# search方法, 不用从头开始匹配, 只要能匹配上, 就直接返回
# 如果能匹配上, 返回Match
# 如果匹配不上, 会返回None
# 可以使用mtch.group()获取匹配成功之后的值
# mtch = re.search(r'{not_existed_tel}', one_str)

# 3. re.sub方法
# sub方法, 第一个参数为正则表达式字符串, 第二个参数为新的值(字符串),
# 第三个参数为待替换的字符串(原始字符串)
# 如果能匹配上, 会返回替换之后的值(一定为字符串类型)
# 如果匹配不上, 会返回原始字符
res = re.sub(r'{not_existed_tel}', '18822223333', one_str)


# 在项目中search方法和sub方法会合在一起用
# 如果one_str原始字符串中能匹配{not_existed_tel}, 则if条件为True, 否则if为False
if re.search('{not_existed_tel}', one_str):
    res = re.sub(r'{not_existed_tel}', '18822223333', one_str)
# split:全部匹配，返回列表 
# findall:全部匹配，返回迭代器 
# finditer:分割字符串，返回列表
"""

#1:代替换的内容
content='{"mobile_phone": "${notexit_tel}","pwd": "12345611","type":"1","reg_name":"小西斯"}'

#2：使用正则表达式
res=r'{"mobile_phone": "\${notexit_tel}"'
result=re.match(res,content)

do_mysql=Hadle_Mysql()
phone=do_mysql.notexist_phone()
a=re.sub(res,phone,content)
do_mysql.close()
