# Start extracting links to the Parts and save href in json file

import os
from os import path
import json
from bs4 import BeautifulSoup as bsp
import urllib as ul
import re

###############################################################################
# FUNCTIONS

# Parse each part for each regulation
def parts_hrefs(addr):
  # Add before adding everything else
  # Square brackets = array of objects (list)
  # Curly brackets = object
  reg_num = addr.strip('/')
  jf.write('"' + reg_num + '"' + ': [')  
  
  # Open the url and save it as an html object  
  srch1 = 'https://www.acquisition.gov'
  srch2 = srch1 + addr
  resp = ul.request.urlopen(srch2)
  html_res = resp.read()
  soup = bsp(html_res, 'html.parser')
  
  # Finding this div applies to FAR, DFARS, and GSAM
  # If there were no results, it would be a null object
  htxt = soup.find('div', id = 'parts-wrapper')
  if htxt is not None:
    htxt = htxt.div
    # All the a tags have our information within the div tag
    htxt = htxt.find_all('a')
    for j in htxt:
      # The part numbers will always just be the text
      hpart = ret_part(j.get_text()).strip()
      href = srch1 + j.attrs['href'].strip()
      add_to_dict(hpart, href)

  # This only gets run for supplementals
  # The tbody tag will always have our information
  # The td tags have long class names, so regex was needed to parse it
  else:
    htxt = soup.tbody
    htxt = soup.find_all('td', class_ = re.compile('.*part-number'))
    for j in htxt:
      hpart = ret_part(j.get_text()).strip()
      href = srch1 + j.a['href'].strip()
      add_to_dict(hpart, href)
  # Close the bracket  
  jf.write(']')

# Returns the part number regardless of what type it is
def ret_part(txt):
  txt_sp = txt.split()
  cnt = len(txt_sp)
  # If its just a number, the list will be 1 object
  if cnt > 1:
    txt = txt_sp[cnt - 1]
  return txt

# Adds values to the dictionary, which dumps json into the file
def add_to_dict(hpart, href):
  d = {
       # Figure out how to change to int
       'part': hpart,
       'href': href,
       'html_text': 'N/A'
       }
  json.dump(d, jf, indent = 2, sort_keys = True)

# Add commas and convert to json
def conv_json(file):
  # Convert all dictionaries to strings, then add commas inbetween each object
  with open(file, 'r') as jf:
    contents = jf.read()
    contents = contents.replace('}{', '},{')
    contents = contents.replace(']"', '],"')
  # Overwrite old file with new changes as a list of strings
  with open(file, 'w', encoding = 'utf8') as jf:
    jf.write(contents)
  # Finally, reconvert the file back to a json file
  with open(file, 'r') as jf:
    contents = json.load(jf)
  with open(file, 'w', encoding = 'utf8') as jf:
    json.dump(contents, jf, indent = 2)

###############################################################################
# ADD DATA

# Load file
# Remove all its contents before writing anything, but only if it exists
jname = os.path.basename(__file__).split('.')[0]
jname = 'json/' + jname + '.json'
if path.exists(jname): open(jname, 'w').close()

# Write html for each section just to get an idea of each structure
# This would be required at the start, but not once it starts running
# hname = os.path.basename(__file__).split('.')[0]
# hname = 'html/' + hname + '.html'
# if path.exists(hname): open(hname, 'w').close()

# Save the data from the regs file to loop through
jname2 = 'json/02_href_regs.json'
with open(jname2) as jf2:
  data = json.load(jf2)

# File will open here to start being added to
# Won't close until all the regs have been looped through
with open(jname, 'w', encoding = 'utf8') as jf:
  jf.write('{')  
  for i in data:
    reg = str(i['href'])
    # Just to see the progess of the code in the console
    print(reg)
    parts_hrefs(reg)
  # Close off final bracket
  jf.write('}')

# At this stage, json files are actually lists with strings
# This turns them into actual json files
conv_json(jname)

print('Finished pushing data to ' + jname)  

  