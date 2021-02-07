# Start extracting links to the Parts and save href in json file

import json
from functions import rem_file, parts_hrefs

jname = rem_file(__file__, 'json')

data = json.load(open('json/02_href_regs.json', 'r'))
# An empty dictionary is created because, there will be objects with lists
d = {}
for i in data:
  htext = str(i['href'])
  part = htext.strip('/')
  print('Adding data to: ' + part)
  d[part] = parts_hrefs(htext)

json.dump(d, open(jname, 'w', encoding = 'utf8'), indent = 2)
print('Finished pushing data to ' + jname)  

  