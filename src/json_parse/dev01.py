# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
from os import path
import json
from bs4 import BeautifulSoup as bsp
import urllib as ul
import re

hname1 = 'html/04_part_href.html'
hname2 = 'html/04_part_href2.html'
#if path.exists(hname2): open(hname2, 'w').close()

with open(hname2, 'r', encoding = 'utf8') as hn1:
  contents = hn1.read()
  soup = bsp(contents, 'html.parser')
  res = soup.find_all('td', class_ = re.compile('.*part-number'))
  for i in res:
    hpart = i.get_text()
    hpart = hpart.strip()
    href = i.a['href']
    href = href.strip()
    print(str(hpart) + ' - ' + str(href))







# for far, dfars, dfars pgi, gsam:
# h1 = Parts
# h2 = Subparts
# h3 = Sections
# h4 = Subsections
#
# TOC:
# div class= 'body'
#
# Content:
# article role= 'article'
# div class= 'body conbody'
# *To pull data, get all get_text between two headings
# *Each subsection gets its own division?




# for supplementals:
# h1 = Parts
# h2 = Subparts
# h3 = Sections
# h4 = Subsections
#
# TOC:
# *Usually not found...
# div class= 'field-items'
# div id='Table of Contents1"
# *Create my own? Ugh...
#
# Content:
# div class= 'field-items'
# *To pull data, get all get_text between two headings
# *Each subsection gets its own division?










# Steps:
# 1) Save current TOC into json file, links to each section
# 1a) Possibly save TOC and reformat structure, along with each a href
# 2) From this TOC json file, iterate over each section then save those sections
#    as independent json files
# 3) Fix paragraphs now or later?



















# with open(hname2, 'w', encoding = 'utf8') as hn2:
#   soup = bsp(contents, 'html.parser')
#   res = soup.find_all('tbody')
#   for i in res:
#     hn2.write(str(i.prettify()))
#     break






# open the url and save it as an html object
# resp = ul.request.urlopen(res)
# html_res = resp.read()

# turn it into html and parse out the content
# text is always found in the <div id="middlecontent"> area on the webpage
# soup = bsp(html_res, 'html.parser')
# reg_txt = soup.find('div', id = 'middlecontent')

# with open(hfile, 'w', encoding = 'utf8') as h:
#   h.write(reg_txt.prettify())
#   h.close()

#print(reg_txt.prettify())
# look into .extrar() for beautiful soup to extract contents in between tags
# changin the names of tags and attributes





# reg
# part
# subpart
# section
# http_link
# html

# regulation-index-browse_wrapper














