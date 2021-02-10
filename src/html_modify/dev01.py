
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

def return_d(citation, next_letter):
    d = {
        'citation': citation,
        'next_letter': next_letter
        # 'is_rnumeral': is_rom_numeral,
        # 'prev_val_alpha': prev_is_alpha
        }
    print(d)
    return d




from functions import paragraph_attributes
num = ['a', 'b', 1, 2, 'i', 'ii', 'iii', 'c', 1, 2, 'i', 'ii', 'iii', 3, 'd', \
       'e', 1, 'i', 'ii', 'iii', 2, 'f', 'g', 'h', 1, 'i', 2, 'i', 'i', 'j', 'k', 'l']

cdev = paragraph_attributes(num)
for x, i in enumerate(num):
    dev_attr = cdev.get_attributes(x)
    print(dev_attr)

# str1 = 'a'
# str2 = 'A'
# print(str2.isupper())

# if not str1.isupper() and str2.isupper():
#     print('yay')
# else:
#     print('nope')

# # lnum = 5
# # print(num[lnum:len(num)])
# for ugh in range(len(num)):
#     next_lett_alpha = False
#     citation = num[ugh]
#     if (ugh + 1) == len(num):
#         next_letter = 'N/A'
#         return_d(citation, next_letter)
#         break
#     # Dev testing if next leter is an alpha character
#     for x, i in enumerate(num[(ugh + 1):len(num)]):
#         # Last iteration of the loop assumes no alpha character
#         # if (x + 1) == len(num):
#         #     next_lett_alpha = False
#         #     next_letter = 'N/A'
#         #     continue
#         # # Break the loop here so that it stop repeating
#         # elif next_lett_alpha == True:
#         #     break
#         while True:
#             # next_letter will only be saved if it runs true
#             try:
#                 i.isalpha()  
#                 next_lett_alpha = True
#                 next_letter = i
#                 break
#             except:
#                 next_lett_alpha = False
#                 next_letter = ''
#                 break
#         # print(str(x) + ' - ' + str(i) + ' - ' + str(next_letter) + ' - ' + str(next_lett_alpha))
#         if next_lett_alpha == True:
#             return_d(citation, next_letter)            
#             break
#         else:
#             continue
#         # Save data in a dictionary, and return it
#         # d = {
#         #     'citation': citation,
#         #     'is_alpha': is_alpha,
#         #     'is_rnumeral': is_rom_numeral,
#         #     'prev_val_alpha': prev_is_alpha
#         #     }





# Dev testing if previous letter was an alpha character
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



















