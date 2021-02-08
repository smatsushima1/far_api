
import os
from os import path
import json
from bs4 import BeautifulSoup as bsp
import urllib as ul
import re


# html = open('html/css_search.html', 'r').read()
# # Turn it into html and parse out the content
# soup = bsp(html, 'html.parser')
# htext = soup.find_all('style')
# list1 = []
# for i in htext:
#     for j in i:
#         list1.append(j)
# list2 = []
# for k in list1:
#     res = k.split('\n')
#     for l in res:
#         if l == '':
#             continue
#         else:
#             list2.append(l)
# print(list2)

# str1 = 'a'
# while True:
#     str1.isalpha()
#     try:
#         print(True)
#         break
#     except:
#         print(False)
#         break
    
#print(htext)

# htext = soup.find('div', class_ = 'reg-container clearfix')
# res = htext.find_all('a')

from dev03 import PCitation
num = ['a', 'b', 'c', 1, 2, 3, 'd', 'e', 1, 'i', 'f']
# print(len(num))
# print(num[11])
cdev = PCitation(num)
for x, i in enumerate(num):
    cdev.get_attributes(x)

# lnum = 7
# print(num[:lnum])

# prev_lalpha = False
# for x, i in reversed(list(enumerate(num[:(lnum - 1)]))):
#     # First iteration of the loop assumes no alpha character
#     if x == 0:
#         prev_lalpha = False
#     # Break the loop here so that it stop repeating
#     elif prev_lalpha == True:
#         break
#     while True:
#         # pletter will only be saved if it runs true
#         try:
#             i.isalpha()  
#             prev_lalpha = True
#             pletter = i
#             break
#         except:
#             prev_lalpha = False
#             pletter = ''
#             break
#     print(str(x) + ' - ' + str(i) + ' - ' + str(pletter) + ' - ' + str(prev_lalpha))
#     if prev_lalpha == True:
#         break
#     else:
#         continue
    
# print(str(x) + ' - ' + str(i) + ' - ' + str(pletter) + str(prev_lalpha))


# x = 'i'













# for i in reversed(num[:2]):
#     print(i)




# for x, i in enumerate(reversed(num[:lnum])):
# # for x, i in enumerate(num):
#     val = ''
#     if x == 0:
#         val_isalpha = False
#     elif val_isalpha == True:
#         break
#     while True:
#         str(i).isalpha()
#         try:
#             val_isalpha = True
#             print(i + ': this is a letter')
#             val = i
#             break
#         except:
#             val_isalpha = False
#             print('nope')
#             break
#     continue
# print(val)






















# so the point of this script was to test to see if I can append the DFARS files
#   to the main part file, but apparently there already is a main file
# also, this was eventually going to parse out the html for other text, but
#   not even Jon Skeet can parse html per: https://blog.codinghorror.com/parsing-html-the-cthulhu-way/
# this will only be saved to remind me of the troubles with parsing html...

# import os

# # main path to current folder
# dir_path = os.path.dirname(os.path.abspath(__file__))
# dfars_dir = "dfars_dev"
# dir_path = dir_path + "\\" + dfars_dir + "\\"

# # start the main loop with identifying the DFARS parts, then read file
# for i in range(201, 254):
#   pnum = str(i)  
#   print("################################################################################")
#   print("DFARS Part: " + pnum)

#   # create file, then read it from directory
#   mname = "PART_" + pnum + ".html"
#   mpath = dir_path + mname
#   mfile = open(mpath, "r")
#   mcont = mfile.read()
#   mfile.close()

#   # first append main file
#   apath = "_append_" + mname
#   apath = dir_path + apath
#   afile = open(apath, "a")
#   afile.write(mcont)
#   afile.write("<br>")
  
#   # now start appending everything else
#   for j in os.listdir(dir_path):
#     if j[0:3] == pnum:
#       jpath = dir_path + j
#       jfile = open(jpath, "r", encoding="utf8")
#       jcont = jfile.read()
#       jfile.close()
#       afile.write(jcont)
#       afile.write("<br>")

#   # operation finished
#   afile.close()
#   print("Finished with " + pnum)



















