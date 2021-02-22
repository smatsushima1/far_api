
from bs4 import BeautifulSoup as bsp
import urllib as ul
import re
import psycopg2 as pg2
import datetime
from functions import *


# Used for debugging specific sections
# Modify file_name and idnum as appropriate
def debug_headers():
    jname = rem_file('dev_contents3', 'html')
    # Connect to database
    conn = db_connect()
    cur = conn.cursor()
    tname = 'dev_all_parts2'
    qry = 'select * from %s where id_num = %s;'
    idnum = '177'
    cur.execute(qry, (AsIs(tname), idnum))
    res = cur.fetchall()
    soup = bsp(res[0][9], 'html.parser')
    hres = soup.prettify()
    # hres = str(hres)
    with open(jname, 'w', encoding = 'utf8') as jf:
        jf.write(hres)
        jf.close()
    # Finish
    conn.commit()
    cur.close()
    # Used for debugging specific sections; used with debug_write_to_file
    with open(jname, 'r', encoding = 'utf8') as jf:
        contents = jf.read()
        jf.close()
    soup = bsp(contents, 'html.parser')
    headers = soup.find_all('h2')
    for i in headers:
        print(i.get_text().strip())
    

# Extracts headers in a separate table
# Runtime: 100.789 seconds
def extract_headers():
    start_time = start_function('extract_headers')
    # Connect to database
    conn = db_connect()
    cur = conn.cursor()
    tname = 'dev_all_parts_headers'
    tname_orig = 'dev_all_parts2'
    # Create new table from original instead of creating it from scratch
    qry = '''drop table if exists %s;
             create table %s as
             select * from %s limit 1;
             truncate table %s;
             alter table %s drop column %s;
             '''
    cur.execute(qry,
                (AsIs(tname),
                 AsIs(tname),
                 AsIs(tname_orig),
                 AsIs(tname),
                 AsIs(tname),
                 AsIs('id_num')
                ))
    # Run for the real results
    cur.execute('select * from %s order by %s;',
                (AsIs(tname_orig),
                AsIs('id_num')
                ))
    results = cur.fetchall()
    for i in results:
        lfile = init_write_file('log/log_add_headers.txt')
        with open(lfile, 'a', encoding = 'utf8') as lf:
            idnum = str(i[12])
            print('%s - %s - %s - Working' % (idnum, i[0], i[5]), file = lf)
            # Skipped sections: these will take more time to debug
            if idnum in [
                         ]:
                print("Skipping for now...", file = lf)
                continue
            # Start extracting headers
            extract_h1(conn, tname, i, lf)
            extract_h2(conn, tname, i, lf)
    # Finish
    conn.commit()
    cur.close()
    end_function(start_time)


# For parts
def extract_h1(connection, table_name, record, file_name):
    soup = bsp(record[9], 'html.parser')
    headers = soup.find('h1')
    if headers is None:
        print("Leaving: no h1's...", file = file_name)
        return
    # Insert into table, only changing the html and type
    lst = [record[0],
           # subpart
           record[1],
           # section
           record[2],
           # subsection
           record[3],
           # paragraph
           record[4],
           # reg
           record[5],
           # htype
           'header',
           # fac
           record[7],
           # hlink
           record[8],
           # htext
           str(headers),
           # order_num
           record[10],
           # import_date
           datetime.datetime.now()
           ]
    insert_values(connection, table_name, tuple(lst))
    

# For subparts
def extract_h2(connection, table_name, record, file_name):
    soup = bsp(record[9], 'html.parser')
    headers = soup.find_all('h2')
    if headers is None:
        print("Leaving: no h2's...", file = file_name)
        return
    for i in headers:
        header = i.get_text().strip()
        hsplit = header.split()
        hstr = ''
        # For most other subparts
        try:
            header[0].isalpha()
            spart = hsplit[1].split('.')[1]
            typ = 'header'
        # For scope
        except:
            spart = 0
            if 'scope' in header:
                typ = 'scope'
            elif 'definitions' in header:
                typ = 'definitions'
            else:
                typ = 'other'
        # Insert values
        lst = [record[0],
               # subpart
               str(spart),
               # section
               record[2],
               # subsection
               record[3],
               # paragraph
               record[4],
               # reg
               record[5],
               # htype
               typ,
               # fac
               record[7],
               # hlink
               record[8],
               # htext
               str(i),
               # order_num
               record[10],
               # import_date
               datetime.datetime.now()
               ]
        insert_values(connection, table_name, tuple(lst))

# debug_headers()
extract_headers()





##############################################################################
# 21 February:
# - great progress! - the database needed much cleaning
# - everything seems cleaned for now...
# - first started extracting headers but lots to improve:
#    - route stdout to a file
#    - add in scope and definition types
#    - be sure subparts can be entered in
#    - read over data in db and find missing information
#    - lots of regs left early...

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























































