
import os
from os import path
import json
from bs4 import BeautifulSoup as bsp
import urllib as ul
import re

# Remove all file contents before writing anything, but only if it exists
def rem_file(fname, dname):
  file_name = dname + '/' + os.path.basename(fname).split('.')[0] + '.' + dname
  if path.exists(file_name): open(file_name, 'w').close()
  return file_name

# Parse each part for each regulation
def parts_hrefs(htext):
  # Open the url and save it as an html object  
  base = 'https://www.acquisition.gov'
  hlink = base + htext
  html = ul.request.urlopen(hlink).read()
  hsoup = bsp(html, 'html.parser')
  # Finding this div applies to FAR, DFARS, and GSAM
  # If there were no results, it would be a null object
  hres = hsoup.find('div', id = 'parts-wrapper')
  if hres is not None:
    # All the a tags have our information within the div tag   
    res = hres.div.find_all('a')
    ind = 1
  # This only gets run for supplementals
  # The tbody tag will always have our information
  # The td tags have long class names, so regex was needed to parse it
  else:
    res = hsoup.tbody.find_all('td', class_ = re.compile('.*part-number'))
    ind = 0
  dlist = add_to_dict(res, base, ind)
  return dlist

# Returns the part number regardless of what type it is
def ret_part(ptext):
  sp_text = ptext.split()
  cnt = len(sp_text)
  # If its just a number, the list will be 1 object
  if cnt > 1: ptext = sp_text[cnt - 1]
  return ptext

# Returns dictionary of objects
def add_to_dict(rlist, addr, reg_ind):
  dlist = []
  for i in rlist:
    # The part numbers will always just be the text
    hpart = ret_part(i.get_text()).strip()
    # If its for the main regs, 'href' will be in the 'attrs'
    if reg_ind == 1:
      hlnk = addr + i.attrs['href'].strip()
    else:
      hlnk = addr + i.a['href'].strip()
    ret_text = {'part': hpart, 'link': hlnk, 'html': 'N/A'}
    dlist.append(ret_text)
  return dlist

