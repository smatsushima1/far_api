# Finds href of supplements

from bs4 import BeautifulSoup as bsp
import urllib as ul
import json
from functions import rem_file

jname = rem_file(__file__, 'json')

# The following string could have been anywhere on acq.gov
srch = 'https://www.acquisition.gov/browse/index/far'
# Open the url and save it as an html object
resp = ul.request.urlopen(srch)
html_res = resp.read()
# Turn it into html and parse out the content
soup = bsp(html_res, 'html.parser')
htext = soup.find('div', class_ = 'reg-container clearfix')
res = htext.find_all('a')

# Create empty list to add objects to
dlist = []
# Take-out the attributes
for i in res:
  rtext = i.get_text()
  reg = rtext.strip()
  hrtext = i.attrs['href']
  href = hrtext.strip().replace('/browse/index', '')
  # Error checks
  if 'Smart' in reg: continue  
  # Append each formatted value as a dictionary into our list
  dlist.append({'reg': reg, 'href': str(href)})

# Dump the contents into the file
json.dump(dlist, open(jname, 'w', encoding = 'utf8'), indent = 2)  
print('Finished pushing data to ' + jname)

