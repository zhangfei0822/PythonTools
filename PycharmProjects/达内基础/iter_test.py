# !/urs/bin/env python
# 练习各种迭代机制
# 创建一个字符串，并通过for循环迭代各个字符
# 创建一个列表，并通过for循环迭代各个字符
# 打开一个文件，并通过for循环迭代各行
# 创建一个字典，并通过for循环迭代字典的键


def iter_t1(aiter):
    for item in aiter:
        print (item)


if __name__ == '__main__':
    astr = 'hello'
    alist = [10, 20, 30]
    atuple = (1, 2, 3)
    adict = {'name':'bob', 'age': 40}
    aset = set(['tedu', 'cn'])
    an_iter = iter(('tern', 'com'))
    fname = 'lesson8.log'

    print(next(an_iter))
    print(next(an_iter))

    fobj = open(fname)
    for line in fobj:
        print(line)