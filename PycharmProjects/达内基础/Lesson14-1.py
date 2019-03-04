# bubble sorting
# !/usr/bin/env python
from random import randint
import copy

def bubble(numlist1):
    # compare n - 1
    # deepcopy will not change orginal list
    numlist = copy.deepcopy(numlist1)
    length = len(numlist)
    # print(numlist)
    for i in range(length - 1):
        for j in range(length - 1 - i):
            if numlist[j] > numlist[j + 1]:
                numlist[j + 1], numlist[j] = numlist[j], numlist[ j + 1]
    return numlist


if __name__ == "__main__":
    num_list = [randint(1, 100) for i in range(10)]
    print(num_list)
    print(bubble(num_list))
    print('after apply a function: numlist = ')
    print(num_list)
