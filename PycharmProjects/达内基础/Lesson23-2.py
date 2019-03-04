# !/urs/bin/env python
# 联系： 模拟unix2dos程序
# 编写格式转换程序
# 1. 能够将Linux文本格式转换为windows文件格式
# 2. 待转换的文件从命令行参数接受
# 3. 不改变原文件
import sys


def unix2dos(fname, sep = '\r\n'):
    dst_fname = fname + '.txt'
    src_obj = open(fname)
    dst_obj = open(dst_fname, 'w')

    for line in src_obj:
        dst_obj.write(line.rstrip('\r\n') + sep)   # delete '\r',  '\n',   '\r\n'

    src_obj.close()
    dst_obj.close()


if __name__ == '__main__':
    unix2dos(sys.argv[1])