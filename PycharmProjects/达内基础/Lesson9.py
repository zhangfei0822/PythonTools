# function
# 需要斟酌函数的输入和输出
def gen_fib(num):
    nlist = []
    for i in range(num):
        if len(nlist) < 2:
            nlist.append(i)
            continue
        nlist.append(nlist[- 1] + nlist[- 2])
    # print('FBNQlist should be :')
    # print(nlist)
    return nlist


def mtable(num):
    for i in range(1, num + 1):
        # log = ''
        for j in range(1, i + 1):
            # log = log + "    {} X {} = {}".format(j, i, i*j)
            print('%d X %d = %d' % (j, i, i * j), ' ', end='  ')
        # print(log)
        print()


if __name__ == '__main__':
    num = int(input('Please input the length of the FBNQlist: '))
    a = gen_fib(num)
    print(a)
    # num = int(input('Please input the num of multiplication table: '))
    mtable(6)