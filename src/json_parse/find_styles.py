
import os
from os import path
import json
from bs4 import BeautifulSoup as bsp
import urllib as ul
import re


# First find CSS sheets
html = open('html/css_sheets.html', 'r').read()
# Turn it into html and parse out the content
soup = bsp(html, 'html.parser')
htext = soup.find_all('style')
# First add all values in list
list1 = []
for i in htext:
    for j in i:
        list1.append(j)
# Add the values of the previous list into another list
list2 = []
for k in list1:
    res = k.split(';')
    for l in res:
        if l == '': continue
        list2.append(l)
# Parse the html out of each item and save to a new list
list3 = []
for m in list2:
    start = m.find('("') + len('("')
    end = m.find('")')
    link = m[start:end]
    if link == '': continue
    list3.append(link)
# Search in each link and print each result if it contains the styles
for n in list3:
    html = ul.request.urlopen(n).read()
    srch1 = 'auto-number'
    if srch1 in str(html):
        print('Results found in: ' + n)
# Results found in: https://www.acquisition.gov/sites/all/themes/acquisition-responsive/styles/styles.css?qo0j39


# # Search through each script tag
# html = open('html/css_sheets.html', 'r').read()
# # Turn it into html and parse out the content
# soup = bsp(html, 'html.parser')
# htext = soup.find_all('script')
# # First add all values in list
# list4 = []
# for p in htext:
#     if p.attrs['src'].startswith('//code'): continue
#     list4.append(p.attrs['src'])
# # Search for string inside each jscript file
# for q in list4:
#     txt = ul.request.urlopen(q).read()
#     srch1 = 'autonumber'
#     if srch1 in str(txt):
#         print('Results found in: ' + q)
# # Nothing found...


'''
The results suggest that the tags I'm looking for are embedded somewhere
else. If I can't find them anywhere, then the only other way to go about this
is to save everything as is and apply my own tags. For obvious reasons, this
would be much too impractical. It would invovled:
- saving all the text as is, only find non-header tags, check to see if it
starts with an open parenthesis then go to the first close parenthesis
    - this would leave me to parse-out the paragraph
    - depending on what type of paragraph it is, it could require a specific
      indent
    - we already know the strucutre of the FAR, so this would be a simple test
    - they will always go a, 1, i, A, 1, I
    - knowing this would mean I can set-up indents based on what value this is
'''










# htext = soup.find('div', class_ = 'reg-container clearfix')
# res = htext.find_all('a')


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



















