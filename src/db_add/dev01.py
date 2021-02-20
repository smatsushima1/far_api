
from bs4 import BeautifulSoup as bsp
import urllib as ul
import re
import psycopg2 as pg2
from functions import *
from functions_json import *


def db_update_html(cur, table_name, html, id_num):
    qry = "update %s set html = '''%s''' where id_num = %s;" % (table_name, html, id_num)
    cur.execute(qry)






# Remove file if already there
fname = 'contents_dev'
hname = rem_file('contents_dev', 'html')

conn = db_connect()
cur = conn.cursor()
tname = 'all_parts_dev1'
qry = 'select * from %s;' % (tname)
cur.execute(qry)
res = cur.fetchall()

# HTML link
for x, i in enumerate(res):
    print(x)
    html = ul.request.urlopen(i[7]).read()
    idnum = i[8]
    soup = bsp(html, 'html.parser')
    hres = soup.find('div', class_ = 'nested0')
    if hres is None:
        hres = soup.find('div', class_ = 'field-items')
    # hres_final = "'''" + str(hres) + "'''"
    db_update_html(cur, tname, str(hres), idnum)

conn.commit()
cur.close()




# conn = db_connect()
# cur = conn.cursor()
# t = 'temp_dd_data'
# qry = 'select * from %s' % t
# qry2 = qry + ' where reg = %s;'
# cur.execute(qry2, ('far', ))
# res = cur.fetchall()
# print(res)






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























































