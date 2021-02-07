# Start extracting links to the Parts and save href in json file

import os
from os import path
import json
from bs4 import BeautifulSoup as bsp
import urllib as ul
import re
from functions import rem_file

rem_file(__file__, 'json')

# print(__file__)












#   # Add closing bracket to signify the end
#   jf.write(']')

















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







