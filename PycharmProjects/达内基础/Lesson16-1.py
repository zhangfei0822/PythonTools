# !/urs/bin/env python


def get_contents():
    print('input the world you want:')
    aa = []
    while True:
        a = input('(. to quit)>')
        if a == '.':
            break
        aa.append(a)
    return aa


def format1(aaa):
    width = 48
    print('+%s+' % ('*' * width) )
    for line in aaa:
        sp_wid, mod = divmod(width - len(line), 2)
        print('+%s%s%s+' %(' '*sp_wid, line, ' ' * (sp_wid + mod)))
    print('+%s+' % ('*' * width))


if __name__ == '__main__':
    contents = get_contents()
    format1(contents)

    aa = ' '
    aa.rstrip()