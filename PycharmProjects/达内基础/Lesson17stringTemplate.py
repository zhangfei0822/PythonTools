# !/urs/bin/env python
from string import Template
import sys
import subprocess


content = """new user infomation:
username: ${name}
password: ${password}
"""

t = Template(content)

def add_user(username):
    pwd = 'fafehdff'
    subprocess.call('username %s' % username, shell = True)
    subprocess.call('echo % | passwd -- stdin %s' % (pwd, username), shell = True)
    # data = t.substitute(name = username, password = pwd)


if __name__ == '__main__':
    origTxt = 'Hi ${name}, I will see you ${day}'
    t = Template(origTxt)
    aa = t.substitute(name = 'bob', day = 'tomorrow')
    print(aa)

    add_user(sys.argv[1])

