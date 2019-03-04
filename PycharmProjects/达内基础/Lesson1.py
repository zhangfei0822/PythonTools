aa = input('user name:')
print('the input is ' + aa)
type(aa)   # str
type(1)  # int
bb = int(aa) + 1
print(bb)

# Exercise 1
# Linux always contains next line:
# !/usr/bin/env/ python
# 如果Python2 显示汉语，需要修改编码格式为utf-8
# -*- coding:utf-8 -*-
# encoding=utf-8
# 注释annotation ctrl + ？
user_name = input('User Name(用户名): ')
print('Welcome ' + user_name)

import start
print(start.hi)
print(start.pstar())