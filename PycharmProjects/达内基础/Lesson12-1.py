# !/urs/bin/env python
# -*encode:utf8*-
"This is a practice for the pythonic program"

# 创建文件
# 根据用户的输入文本，创建文件
# 1. 要求用户输入文件名
# 2. 如果文件已经存在，要求用户重新输入
# 3. 提示用户输入数据，每行数据先写到列表中
# 4. 将列表中的数据写入用户创建的文件中
import os


def store_file(file_path, content_list):
    f = open(file_path, 'w')
    # for line_str in content_list:
    #     f.write(line_str)
    f.writelines(content_list)
    f.flush()
    f.close()

    return True


def get_file_name():
    final_file = ''
    print('Please input the file name or letter "N" to stop create file \
                     \nexample1: abc.txt  \
                     \nexample2: N\n')
    while True:
        temp_str = input()       # no enter
        if temp_str == 'N':
            print('stop create file')
            break
        elif os.path.exists(temp_str):
            print('%s has been existed, please retry: ' % temp_str)
            continue
        else:
            final_file = temp_str
            break

    return final_file


def get_contents():
    content = []

    while True:
        line = input('(#N to quit)>')
        if line == '#N':
            break
        content.append(line)

    return content


if __name__ == "__main__":
    file_name = get_file_name()
    if file_name != '':
        print('please input the content by line and #N to end input:')
        data = get_contents()
        if store_file(file_name, ['%s\n' % line for line in data]):
            print('Create file and store the content successfully')
            f = open(file_name)
            print(f.readlines())
    else:
        print('No new file was created!!!')


