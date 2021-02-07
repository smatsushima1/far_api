# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 12:15:39 2021

@author: smats
"""

lst = ['a', 'b', 1, 'c', 1, 2, 'ii', 'iv', 'xi', 3, 'A']
for i in lst:
     while True:
          try:
                print(i)
                print(i.isalpha())
                print('\n')
                break
          except:
                print(i)
                print('we got a problem...')
                print('\n')
                break


# print(chr(ord(char) - 25))


#charac = input()

# if charac == "Z": # If Z encountered change to A
#    print(chr(ord(charac)-25))

# else:
#    change = ord(charac) + 1
#    print(chr(change))

