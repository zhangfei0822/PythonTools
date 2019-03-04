# /urs/bin/env python
import sys
import time
sys.stdout.write('hello world\n')
sys.stderr.write('error\n')

for i in range(1, 11):
    sys.stderr.write('%s\n' % i)
    time.sleep(1)
    sys.stdout.write('%s\n' % i)
    time.sleep(1)