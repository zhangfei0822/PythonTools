# !/urs/bin/env python

stack = []


def pop_it():
    if stack:
        stack.pop()
    else:
        print("\033[31;lmempty stack.\033[0m")
        # linux 表示红色字体

def push_it():
    item = input('item to push: ')
    stack.append(item)

def view_it():
    print(stack)

def show_manu():
    CMDs = {'0':push_it, '1':pop_it, '2':view_it}
    # 函数字典，注意：仅放置函数名
    prompt = """(0) push it
(1) pop it
(2) view it
(3) quit
please input you choic(0/1/2/3)
    """
    while True:
        choice = input(prompt).strip()[0]
        if choice not in '0123':
            print('invalid choice. Try again')
            continue
        if choice == '3':
            break
        # if choice == '0':
        #     push_it()
        # elif choice == '1':
        #     pop_it()
        # else:
        #     view_it()
        CMDs[choice]()

if __name__ == '__main__':
    show_manu()