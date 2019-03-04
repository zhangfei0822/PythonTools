# import random
from random import choice
dd = 'abcdefghigklmnopqrst'

adict = {
    '0':'abc',
    '1':'cde',
    '3':'aaaaa',
}

def generatePassword(num):
    password = ''
    for i in range(num):
        # password = p8
        # password + random.choice(dd)
        password = password \
                   + choice(dd)           # 续行符, 斜杠 \
    return password


if __name__ == '__main__':
    num = int(input('Please input the number of password: '))
    print(generatePassword(num))