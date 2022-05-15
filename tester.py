import sys
import time

program = sys.argv[1]

if program == '1':
    print('0000', end='')
    time.sleep(2)
    print('1111')
else:
    time.sleep(10)
