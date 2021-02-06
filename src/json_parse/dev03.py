# Start extracting links to the Parts and save href in json file

import os
from os import path
import json
from bs4 import BeautifulSoup as bsp
import urllib as ul
import re

###############################################################################
# Functions

# Return html text
def ret_html(addr):
  # Open the url and save it as an html object
  srch1 = 'https://www.acquisition.gov'
  srch2 = srch1 + addr
  resp = ul.request.urlopen(srch2)
  html_res = resp.read()
  soup = bsp(html_res, 'html.parser')
  
  reg_num = addr.split('/')
  jf.write('"' + reg_num + '"' + ': [')

  # Finding this div applies to FAR, DFARS, and GSAM
  htxt = soup.find('div', id = 'parts-wrapper')
  if len(htxt) != 0:
    htxt = htxt.div
    htxt = htxt.find_all('a')
    for i in htxt:
      hpart = ret_part(i.get_text())
      href = srch1 + i.attrs['href']
      d = {
           'part': hpart,
           'href': href,
           'html_text': 'N/A'
          }
      json.dump(d, jf, indent = 2)
      
      
      
      #print(hnum + ' - ' + hreg)
      #jf.write(str(i))
      
  # These apply to the supplementals
  else:
    htxt = soup.tbody
    htxt = htxt.find_all('a')
    for i in htxt:
      hpart = ret_part(i.get_text())
      href = srch1 + i.attrs['href']
      d = {
           'part': hpart,
           'href': href,
           'html_text': 'N/A'
          }
      json.dump(d, jf, indent = 2)
      
      
      
      
      #print(hnum + ' - ' + hreg)
      #jf.write(str(i))
  
  jf.write(']')
  #jf.write(str(i))

# Returns the part number regardless of what type it is
def ret_part(txt):
  txt_sp = txt.split()
  cnt = len(txt_sp)
  if cnt > 1:
    txt = txt_sp[cnt - 1]
  return txt
  
###############################################################################

# Load file
# Remove all its contents before writing anything, but only if it exists
jname = os.path.basename(__file__).split('.')[0]
jname = 'json/' + jname + '.json'
# jname = 'html/' + jname + '.html'

reg = '/far'

if path.exists(jname):
  open(jname, 'w').close()
with open(jname, 'w', encoding = 'utf8') as jf: 
  jf.write('{')
  ret_html(reg)
  jf.write('}')

# # Convert all dictionaries to strings, then add commas inbetween each object
# # Then, overwrite old file with new changes as a list of strings
with open(jname, 'r') as jf:
  contents = jf.read()
  contents = contents.replace('}{', '},{')
with open(jname, 'w', encoding = 'utf8') as jf:
  jf.write(contents)

# # Finally, reconvert the file back to json
with open(jname, 'r') as jf:
  contents = json.load(jf)
with open(jname, 'w', encoding = 'utf8') as jf:
  json.dump(contents, jf, indent = 2)

print('Finished pushing data to ' + jname)  

  




  #print(html_contents)
  

  #rt = rt.find_all('a')


# Square brackets = array of objects (list)
# Curly brackets = object






















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







