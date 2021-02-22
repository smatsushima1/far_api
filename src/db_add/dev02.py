
import json
import os
import datetime
from functions import *


# str1 = '''I can't do work'''
# str1_sp = str1.split()
# str1_sp[1] = 'can'
# print(str1_sp.join())
# print(str1_sp)

lfile = init_write_file('log/log_add_headers.txt')
with open(lfile, 'w', encoding = 'utf8') as lf:
    print('ugh derp', file = lf)

