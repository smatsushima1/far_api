
from bs4 import BeautifulSoup as bsp
import urllib as ul
import re
import psycopg2 as pg2
from functions import *
from functions_json import *

#search_css('autonumber')
#search_jscripts('autonumber')


#db_select_all('temp_dd_data')

# Remove file if already there
fname = 'contents_dev'
hname = rem_file('contents_dev', 'html')

conn = db_connect()
cur = conn.cursor()
qry = 'select * from all_parts_dev1;'
cur.execute(qry)
res = cur.fetchall()

# HTML link
for i in res:
    html = ul.request.urlopen(i[7]).read()
    soup = bsp(html, 'html.parser')
    hres = soup.find('div', class_ = 'nested0')

    if hres is not None:
        with open(hname, 'w', encoding = 'utf8') as hf:
            hf.write(results)
    else:
        hres = soup.find('div', class_ = 'field-items')
        with open(hname, 'w', encoding = 'utf8') as hf:
            hf.write(results)


conn.commit()
cur.close()










# with open(hname2, 'w', encoding = 'utf8') as hn2:
#   soup = bsp(contents, 'html.parser')
#   res = soup.find_all('tbody')
#   for i in res:
#     hn2.write(str(i.prettify()))
#     break





# Steps:
# 1) Save current TOC into json file, links to each section
# 1a) Possibly save TOC and reformat structure, along with each a href
# 2) From this TOC json file, iterate over each section then save those sections
#    as independent json files
# 3) Fix paragraphs now or later?


########################### For FAR, DFARS. GSAM... ###########################
# h1 = Parts
# h2 = Subparts
# h3 = Sections
# h4 = Subsections

# TOC:
# div class= 'body'

# Content (FAR, DFARS, GSAM):
# article role= 'article'
# div class= 'body conbody'
# *To pull data, get all get_text between two headings
# *Each subsection gets its own division?

# All contents:
# div class='nested0'


################################ Supplementals ################################
# h1 = Parts
# h2 = Subparts
# h3 = Sections
# h4 = Subsections

# TOC:
# *Usually not found...
# div class= 'field-items'
# div id='Table of Contents1"
# *Create my own? Ugh...

# Content:
# div class= 'field-items'
# div id='middlecontent'
# field-items consists of everything, including table of contents
# *To pull data, get all get_text between two headings
# *Each subsection gets its own division?

# All contents:
# div id='middlecontent'


# regulation-index-browse_wrapper
# look into .extrar() for beautiful soup to extract contents in between tags
# changin the names of tags and attributes























































