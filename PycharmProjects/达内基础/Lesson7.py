# 斐波那契数列
#   1. 斐波那契数列就是一个数，总是前两个数之和，比如0,1,1,2,3,5,8,13
# 2. 使用for 循环和range函数编写一个程序，计算有10个数字的斐波那契数列
# 3. 改进程序，要求用户输入一个数字，可以生成用户需要长度的斐波那契数列
# step1
nlist = []
for i in range(10):
    if len(nlist) < 2:
        nlist.append(i)
        continue
    nlist.append(nlist[-1] + nlist[-2])
print(nlist)
# step2--improve step2
nlist = []
num = int(input('Please input the length of the FBNQlist: '))
for i in range(num):
    if len(nlist) < 2:
        nlist.append(i)
        continue
    nlist.append(nlist[- 1] + nlist[- 2])
print('FBNQlist should be :')
print(nlist)
