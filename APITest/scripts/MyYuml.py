# -*- coding:utf-8 -*-
# @Author:zxy

import yaml
from readpath.handle_path import Configs_File_Path


class MyYuml(object):
    def __init__(self, filename):
        with open(filename, encoding='utf8') as file:
            self.datas = yaml.full_load(file)

    def read_yuml(self, section, option):
        return self.datas[section][option]

    @staticmethod
    def write_yuml(datas,filename):
        with open(filename, mode="w", encoding="utf-8") as one_file:
            yaml.dump(datas, one_file, allow_unicode=True)  # allow_unicode=True这个表示配置中的乱码进行编码装化


do_yuml = MyYuml(Configs_File_Path)
pass


# if __name__ == '__main__':
#     do_yuml = MyYuml('ce.yaml')
    # datas = {
    #     "excel": {
    #         "cases_path": "cases.xlsx"
    #     },
    #     "user": {
    #         "username": "小花",
    #         "password": "666666",
    #         "age": 16
    #     }
    # }
#
# do_yuml.write_yuml(datas,'write_datas.yuml')
# do_yuml.read_yuml['user']['age']
