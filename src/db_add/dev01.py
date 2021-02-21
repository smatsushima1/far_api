
from bs4 import BeautifulSoup as bsp
import urllib as ul
import re
import psycopg2 as pg2
from functions import *
from functions_json import *



# Updates table to include html portion of the web link provided
def split_sections():
    jname = rem_file('contents_dev', 'html')
    # Connect to database
    conn = db_connect()
    cur = conn.cursor()
    tname = 'all_parts_dev_2'
    qry = 'select * from %s where id_num = %s;'
    cur.execute(qry, (AsIs(tname), '1'))
    res = cur.fetchall()
    soup = bsp(res[0][8], 'html.parser')
    # hres = soup.prettify()
    hres = str(soup)
    
    with open(jname, 'w', encoding = 'utf8') as jf:
        jf.write(hres)
        jf.close()
    # Finish
    conn.commit()
    cur.close()


def read_html():
    # jname = rem_file('contents_dev', 'html')
    with open('html/contents_dev.html', 'r', encoding = 'utf8') as jf:
        rhtml = jf.read()
    soup = bsp(rhtml, 'html.parser')
    soup2 = soup.find('main')
    # Remove all span classes
    for i in soup2.find_all('span'):
        i.unwrap()
    # Separate each article by section and save this into another table
    for x, j in enumerate(soup2.find_all('h2')):
        if x == 2:
            # h2res = soup2.find('h2', id = j['id'])
            print(j.get_text().lstrip())
            print(j)
            print(j.next_sibling.next)
        else:
            continue
        # print(j['id'])
        # print(soup2.find_next_sibling('h2', id = j['id']))
    # print(soup2.find('h2', id="ariaid-title3").nextSibling.next)

# Just separate everything by headers
read_html()







# Insert all headings as titles
# Meaning, we will have:
# - main: all text combined
# - toc: table of contents
# - title: titles of subparts
# - body: sections and subsections






# Updates table to include html portion of the web link provided
def split_sections2():
    jname = rem_file('contents_dev5', 'html')
    # Connect to database
    conn = db_connect()
    cur = conn.cursor()
    tname = 'all_parts_dev_2'
    qry = 'select * from %s where part = %s;'
    cur.execute(qry, (AsIs(tname), '1'))
    res = cur.fetchall()
    soup = bsp(res[4][8], 'html.parser')
    hres = soup.prettify()
    #hres = str(soup)
    
    with open(jname, 'w', encoding = 'utf8') as jf:
        jf.write(hres)
        jf.close()
    # Finish
    conn.commit()
    cur.close()


def read_html2():
    # jname = rem_file('contents_dev', 'html')
    with open('html/contents_dev5.html', 'r', encoding = 'utf8') as jf:
        rhtml = jf.read()
    soup = bsp(rhtml, 'html.parser')
    soup2 = soup.find('main')
    # Remove all span classes
    for i in soup2.find_all('span'):
        i.unwrap()
    # Separate each article by section and save this into another table
    for j in soup2.find_all('article'):
        print(j)    
    
# split_sections2()
# read_html2()    

    # print(soup)
    # break
        # print(i)
        # break
        # res = i.get_text().strip()
        # print(str(res))
        # break
        # res_spl = res.split()
        # # print(len(res.split()))
        # str1 = ''
        # for j in res_spl:
        #     str1 += j + ' '
        # print(str1)
    




    # # HTML link
    # for x, i in enumerate(res):
    #     pass
    #     print(x)
    #     url = str(str(i[7]).encode('utf-8'))
    #     url_final = url[2:len(url) - 1]
    #     html = ul.request.urlopen(url_final).read()
    #     idnum = i[9]
    #     soup = bsp(html, 'html.parser')
    #     # For FAR, DFARS, GSAM: all content is listed under 'nested0'
    #     hres = soup.find('div', class_ = 'nested0')
    #     # For all others, content is listed under 'field-items'
    #     if hres is None:
    #         hres = soup.find('div', class_ = 'field-items')
    #     update_one2(cur, tname, 'html', str(hres), idnum)
    














#add_html2()

#print('\u2014')


















# # Remove file if already there
# fname = 'contents_dev'
# hname = rem_file('contents_dev', 'html')

# conn = db_connect()
# cur = conn.cursor()
# tname = 'all_parts_dev1'
# qry = 'select * from %s order by id_num;'
# cur.execute(qry, (AsIs(tname), ))
# res = cur.fetchall()

# with open(hname, 'w', encoding = 'utf8') as hw:
#     hw.write(res[0][8])
#     hw.close()



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























































