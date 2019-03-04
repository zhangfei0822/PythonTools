# !/urs/bin/env python
# 练习:模拟进度条动画
# 编写一个“动画”程序
# 1. 在屏幕上输出20个#
# 2. 将@符合从这一行#号间穿过
# 当@符号到了行尾，它又回到开头，重新穿越
# \r回车符不换行，既回到行首，覆盖以前写的东西   \n换行符
# encoding = utf-8
import time
import sys

counter = 20

print('旋转进度条演示')
for i in range(counter):
    for ch in '-\\|/':
        print('\r%s ##' % ch, sep = '##', end = '')
        # sys.stdout.flush()
        time.sleep(0.3)

print('横向移动进度条演示')
while True:
    for i in range(counter + 1):
        print('\r%s@%s' % ('#' * i, '#' * (counter - i)), end = '')
        time.sleep(0.3)


f = open('less.txt')
f.seek()