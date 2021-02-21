
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


def extract_headers():
    # jname = rem_file('contents_dev', 'html')
    with open('html/contents_dev.html', 'r', encoding = 'utf8') as jf:
        rhtml = jf.read()
    soup = bsp(rhtml, 'html.parser')
    #soup2 = soup.find('main')

    headers = soup.find_all('h2')
    header = headers.get_text().lstrip().strip().rstrip()
    hsplit = header.split()
    hstr = ''
    for k in hsplit:
        hstr += k + ' '
    hstr = hstr.rstrip()
    print(hstr)
    soup2 = bsp(hstr, 'html.parser')
    htag = soup2.new_tag('h2')
    htag.string = hstr
    htag['href'] = '#ugh_derp'
    print(htag)
    
    for i in headers:
        break
        header = i.get_text().strip()
        hsplit = header.split()
        hstr = ''
        for j in hsplit:
            hstr += j + ' '
        print(hstr)
        soup2 = bsp(hstr, 'html.parser')
        htag = soup2.new_tag('h2')
        htag.string = hstr
        htag['href'] = '#ugh_derp'
        print(htag)


def extract_headers2():
    start_time = time.time()
    print('\nFunction: extract_headers\nStarting...')
    # Connect to database
    conn = db_connect()
    cur = conn.cursor()
    tname = 'dev_all_parts_headers'
    tname_orig = 'dev_all_parts_2'
    qry = '''drop table if exists %s;
             create table %s as
             select * from %s limit 1;
             truncate table %s;
             alter table %s drop column id_num;
             '''
    # Truncate everything since it will be identical in format to dev_all_parts_2
    cur.execute(qry,
                (AsIs(tname),
                AsIs(tname),
                AsIs(tname_orig),
                AsIs(tname),
                AsIs(tname)
                ))
    
    cur.execute('select * from %s order by %s;',
                (AsIs(tname_orig),
                AsIs('id_num')
                ))
    results = cur.fetchall()
    for i in results:
        id_num = i[9] + 1
        print('%s - %s - %s - Working' % (str(id_num), i[0], i[4]))
        # Start extracting headers
        extract_h1(conn, tname, i)
        extract_h2(conn, tname, i)
    # Finish
    conn.commit()
    cur.close()
    print("Function finished in %s seconds" % round(time.time() - start_time, 3))


# For parts
def extract_h1(connection, table_name, record):
    soup = bsp(record[8], 'html.parser')
    htag = soup.find('h1')
    # Insert into table, only changing the html and type
    lst = [record[0],
           # subpart
           record[1],
           # section
           record[2],
           # subsection
           record[3],
           # reg
           record[4],
           # type
           'header',
           # fac
           record[6],
           # link
           record[7],
           # html
           str(htag)
           ]
    insert_values(connection, table_name, tuple(lst))
    

# For subparts
def extract_h2(connection, table_name, record):
    soup = bsp(record[8], 'html.parser')
    headers = soup.find_all('h2')
    for i in headers:
        header = i.get_text().strip()
        hsplit = header.split()
        hstr = ''
        # For most other subparts
        if header[0].isalpha():
            spart = hsplit[1].split('.')[1]
            typ = 'header'
        # For scope
        else:
            spart = 0
            typ = 'scope'
        # Insert values
        lst = [record[0],
               # subpart
               str(spart),
               # section
               record[2],
               # subsection
               record[3],
               # reg
               record[4],
               # type
               typ,
               # fac
               record[6],
               # link
               record[7],
               # html
               str(i)
               ]
        insert_values(connection, table_name, tuple(lst))

extract_headers2()


##############################################################################
# Add attributes to tags
    # headers = soup.find_all('h1')
    # for i in headers:
    #     header = i.get_text().strip()
    #     hsplit = header.split()
    #     hstr = ''
    #     for j in hsplit:
    #         hstr += j + ' '
    #     print(hstr)
    #     soup2 = bsp(hstr, 'html.parser')
    #     htag = soup2.new_tag('h2')
    #     htag.string = hstr
    #     htag['href'] = '#ugh_derp'
    #     print(htag)

##############################################################################
# Multiple try except attempts
    # Use this for TOC, if thats what you want...
    #print(h1_text)
    # try:
    #     toc = soup.find('div', class_ = 'body')
    # except AttributeError:
    #     pass
    # try:
    #     toc = soup.find('div', id = 'Table of Contents1')
    # except:
    #     toc = ''
    # toc_final = str(main_title) + str(toc)
    # print(toc_final)
    # for x, j in enumerate(soup2.find('div', class_ = )


##############################################################################
# Remove span classses
    # Remove all span classes in their separate objects
    # for i in soup.find_all('span'):
    #     i.unwrap()


##############################################################################
# Separate contents of sections/subsections
    # Use this for headers
    # Separate each article by section and save this into another table
    # for x, j in enumerate(soup2.find_all('h2')):
    #     if x == 2:
    #         # h2res = soup2.find('h2', id = j['id'])
    #         print(j.get_text().lstrip())
    #         print(j)
    #         print(j.next_sibling.next)
    #     else:
    #         continue
        # print(j['id'])
        # print(soup2.find_next_sibling('h2', id = j['id']))
    # print(soup2.find('h2', id="ariaid-title3").nextSibling.next)


##############################################################################
# Different types
# We'll make our own TOC!!!!!! Don't Extract!!!
# Insert all headings as titles
# Meaning, we will have:
# - main: all text combined
# - toc: table of contents
# - header: titles of subparts
# - body: sections and subsections


##############################################################################
# For Tomorrow:
# - extract main title from each section in FAR, save as title
#     - we dont' need to extract title and toc - we'll make them ourselves
#     - extract the h2, h3, h4 headings: try except with bold tags in lieu of headings













# Updates table to include html portion of the web link provided
def split_sections2():
    jname = rem_file('contents_dev7', 'html')
    # Connect to database
    conn = db_connect()
    cur = conn.cursor()
    tname = 'all_parts_dev_2'
    qry = 'select * from %s where part = %s and reg = %s;'
    cur.execute(qry, (AsIs(tname), '1', 'dtar'))
    res = cur.fetchall()
    soup = bsp(res[0][8], 'html.parser')
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
    with open('html/contents_dev6.html', 'r', encoding = 'utf8') as jf:
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























































