# !/urs/bin/env python
# 用户登录信息系统
# 使用字典模拟一个用户登录系统
# 1. 支持新用户注册，新用户名和密码注册到字典中
# 2. 支持老用户登录，用户名和密码正确提示登录成功
# 3. 主程序通过循环询问进行何种操作，根据用户的选择，执行注册或是登录操作
import getpass

db = {}

def register():
    name = input('username: ')
    if name in db:
        print('\033[31;1m%s already exist\033[0m' % name)
    else:
        password = input('password:')
        db[name] = password
        print(('\033[31;1m%s register success \033[0m' % name))


def login():
    name = input("username: ")
    password = getpass.getpass('Password: ')
    if db.get(name) == password:
            print('log in successfully')
    else:
        print('log in incorrect')


def show_manu():
    CMDs = {'0': register, '1':login}
    prompt = """
    (0) register user
    (1) login
    (2) quit
    please input your choice(0/1/2)
    """
    while True:
        choice = input(prompt).strip()[0]
        if choice not in '012':
            print('invalid choice,try again')
            continue
        if choice == '2':
            print('Exit successfully! ')
            break

        CMDs[choice]()


if __name__ == '__main__':
    show_manu()