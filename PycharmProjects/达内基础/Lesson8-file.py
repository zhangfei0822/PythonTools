# file object
# encoding=utf-8
f = open('lesson8.log', 'r')
# f.write('\n next ')
for line in f:
    print(line)
f.close()

