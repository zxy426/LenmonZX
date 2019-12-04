
import logging
import os

from readpath.handle_path import Logs_Path
from scripts.MyYuml import do_yuml

class MyLogger(object):

    @classmethod#加这个表示下面的是类方法
    def create_logger(cls):
        # 创建日志收集器
        mylog = logging.getLogger(do_yuml.read_yuml('log','logname'))
        # 获取日志等级
        mylog.setLevel(do_yuml.read_yuml('log','log_Level'))
        # 设置日志输出格式
        format = logging.Formatter(do_yuml.read_yuml('log','log_format'))
        # 创建一个输出导控制台的日志输出渠道
        sh = logging.StreamHandler()
        sh.setLevel(do_yuml.read_yuml("log", "Steram_Level"))
        # 设置输出导控制台的格式
        sh.setFormatter(format)
        # 将输出渠道添加到日志收集器中
        mylog.addHandler(sh)
        # 创建一个输出导文件的渠道
        fh = logging.FileHandler(filename=os.path.join(Logs_Path,do_yuml.read_yuml('log','log_Filename')),
                                 encoding='utf8')
        # 设置日志的输出等级
        fh.setLevel(do_yuml.read_yuml('log','FilenameLevel'))
        # 设置输出到文件的日志格式
        fh.setFormatter(format)
        # 将输出渠道加到日志收集器中
        mylog.addHandler(fh)
        return mylog

do_log=MyLogger.create_logger()

# # if __name__ == '__main__':  这样写不好，如果你不小心多个文件创建多个日志收集器，每个日志收集器就都会收集一遍日志
#     log=MyLogger.create_logger()
#     log.info('Hello Python')



