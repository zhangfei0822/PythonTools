# pythonic
# !/urs/bin/env python      # 起始行，Python 解释下面的语言
# -*encode:utf-8*-          # 编码声明
# "This is a test module "    # 模块文档字符串

import  sys                 # 导入模块
import os

debug = True                # 全局变量


class FooClass(object):    # 类定义
    'Foo class'
    pass


def test():
    'test function'
    foo = FooClass()


if __name__ == '__main__':
    test()