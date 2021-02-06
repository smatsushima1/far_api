# Finds href of supplements

import os
from os import path
from bs4 import BeautifulSoup as bsp
import urllib as ul
import json

###############################################################################
# FUNCTIONS

# Add commas and convert to json
def conv_json(file):
  # Convert all dictionaries to strings, then add commas inbetween each object
  with open(file, 'r') as jf:
    contents = jf.read()
    contents = contents.replace('}{', '},{')
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

# Remove all its contents before writing anything, but only if it exists
jname = os.path.basename(__file__).split('.')[0]
jname = 'json/' + jname + '.json'
if path.exists(jname): open(jname, 'w').close()

# The following string could have been anywhere on acq.gov
srch = 'https://www.acquisition.gov/browse/index/far'
# Open the url and save it as an html object
resp = ul.request.urlopen(srch)
html_res = resp.read()
# Turn it into html and parse out the content
soup = bsp(html_res, 'html.parser')
rt = soup.find('div', class_ = 'reg-container clearfix')
rt = rt.find_all('a')

# At this stage, json files are actually lists with strings
# This turns them into actual json files
with open(jname, 'w', encoding = 'utf8') as jf:
  # Add open bracket before adding data through loop
  jf.write('[')
  # Take-out the attributes
  for i in rt:
    reg_abb = i.get_text()
    reg_abb = reg_abb.strip()
    reg_name = i.attrs['href']
    reg_name = reg_name.strip()
    # Create dictionary to start adding values
    d = {
         'reg': reg_abb,
         'href': reg_name
        }
    json.dump(d, jf, indent = 2)
  # Add closing bracket to signify the end
  jf.write(']')

# At this stage, json files are actually lists with strings
# This turns them into actual json files
conv_json(jname)

print('Finished pushing data to ' + jname)

###############################################################################
# CLEAN-UP DATA

with open(jname, 'r') as jf:
  data = json.load(jf)
  for i in data:
    # Save each element as a string
    reg = i['reg']
    href = i['href']
    hrefc = href.count('/')
    # Remove objects that are not a regulation
    if 'Smart' in reg:
      data.remove(i)
    # Some of the results display the '/browse/index' location
    # This will remove that and only leave '/[REGULATION]'
    elif hrefc > 1:
      hrefs = href.split('/')
      hrefsc = len(hrefs)
      href = '/' + hrefs[hrefsc - 1]
      i['href'] = href
  # Save the old data over the new data
  data = data

# New data overrites old data
with open(jname, 'w', encoding = 'utf8') as jf:
  json.dump(data, jf, indent = 2)

print("Fished updating " + jname)