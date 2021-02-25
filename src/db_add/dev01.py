
from functions import *


# Used for debugging specific sections
# Modify file_name and idnum as appropriate
def debug_headers(go_ind, idnum, file_name, file_save):
    if go_ind == 0:
        return
    jname = init_write_file(file_name)
    # Connect to database
    db = dbi()
    conn = db[0]
    cur = db[1]
    tname = 'dev_all_parts2'
    qry = 'select %s from %s where %s = %s;'
    cur.execute(qry,
                (AsIs('htext'),
                 AsIs(tname),
                 AsIs('id_num'),
                 idnum
                 ))
    
    res = cur.fetchall()
    soup = bsp(res[0][0], 'html.parser')
    # Finish
    dbcl(conn, cur)
    # Save to file only if specified
    if file_save:
        with open(jname, 'w', encoding = 'utf8') as jf:
            jf.write(soup.prettify())
            jf.close()
    # Start looping through headers
    hlist = ['h1', 'h2', 'h3', 'h4', 'b', 'strong', 'li']
    for i in hlist:
        headers = soup.find_all(i)
        print('\n')
        print('#' * 80)
        print('Heading: %s\nNumber of headings = %s\n' % (i, str(len(headers))))
        for j in headers:
            # Make all the text look pretty
            hstr1 = j.get_text().strip()
            hsplit = hstr1.split()
            hstr2 = ''
            for k in hsplit:
                hstr2 += k + ' '
            print(hstr2)

            
            
            

# Extracts headers in a separate table
# Runtime: 100.789 seconds
def extract_headers(go_ind):
    if go_ind == 1:
        return
    start_time = start_function('extract_headers')
    # Connect to database
    db = dbi()
    conn = db[0]
    cur = db[1]
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
    lfile = init_write_file('log/log_add_headers.txt')    
    with open(lfile, 'w', encoding = 'utf8') as lf:
        for i in results:
            idnum = str(i[12])
            print('%s - %s - %s' % (idnum, i[0], i[5]), end = '', file = lf)
            # Skipped sections: these will take more time to debug
            if idnum in [
                         ]:
                print(' - Skipping for now...', file = lf)
                continue
            # Start extracting headers
            extract_h1(conn, tname, i, lf)
            extract_h2(conn, tname, i, lf)
            #lf.write(pstr)
    # Finish
    conn.commit()
    cur.close()
    end_function(start_time)


# For parts
def extract_h1(connection, table_name, record, file_name):
    soup = bsp(record[9], 'html.parser')
    headers = soup.find_all('h1')
    if len(headers) == 0:
        print(' - No', end = '', file = file_name)
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
           str(headers[0]),
           # order_num
           record[10],
           # import_date
           datetime.datetime.now()
           ]
    insert_values(connection, table_name, tuple(lst))
    print(' - +', end = '', file = file_name)
    

# For subparts
def extract_h2(connection, table_name, record, file_name):
    soup = bsp(record[9], 'html.parser')
    headers = soup.find_all('h2')
    if len(headers) == 0:
        print(' - No', file = file_name)
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
    print(' - +', file = file_name)


# 1 for debug, 0 for extract_headers
go_ind = 1
debug_headers(go_ind,
              447,
              'html/dev_contents.html',
              False
              )
extract_headers(go_ind)





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
# Possible steps forward:
# - create separate functions for parsing headers of different types
#     - traditional headings (god bless them)
#     - bold headings
#     - strong headings (why...)
#     - missplaced h2 headings
# - all these should add up to the total amount of records we have to parse

##############################################################################
# Desired format:
# - only headers in the regular format
# - only paragraphs
#     - first isolate all sections, remove all formatting, convert to paragraphs
#     - no lists
# - no unaltered

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























































