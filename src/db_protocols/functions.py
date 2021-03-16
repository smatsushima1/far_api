
import os
from os import path
from dotenv import load_dotenv
from bs4 import BeautifulSoup as bsp
import requests as rq
import re
import psycopg2 as pg2
from psycopg2 import sql
import time


#################################### Dev Functions ###################################



#################################### Basics ###################################
# Remove all file contents before writing anything, but only if it exists
def init_write_file(file_name):
    if path.exists(file_name):
        open(file_name, 'w').close()
    return file_name


# Write to specified file; combines init_write_file functionality
def write_file(file_name, text, html):
    if path.exists(file_name):
        open(file_name, 'w').close()
    with open(file_name, 'w', encoding = 'utf8') as wf:
        if html:
            wf.write(text.prettify())
        else:
            wf.write(text)
        wf.close()


# Start timer for functinos
def start_function(func_name):
    start_time = time.time()
    print('\n' + cb())
    print('Function: %s\nStarting...' % (func_name))
    return start_time


# End timer for functions
def end_function(start_time):
    end_time = time.time() - start_time
    if end_time > 60:
        res = end_time / 60
        res_spl = str(res).split('.')
        mins = res_spl[0]
        secs = round(float('.' + res_spl[1]) * 60, 3)
        print('''Function finished in %s' %s"''' % (mins, secs))
    else:
        print('Function finished in %s"' % round(time.time() - start_time, 3))


# Comment block headers
def cb():
    return str('#' * 80)

################################### DB Tasks ##################################
# DB Init
# Credentials loaded from .env file
def db_init():
    load_dotenv('../.env')
    conn = pg2.connect(dbname = os.environ['PG_DATABASE'],
                       user = os.environ['PG_USER'],
                       host = os.environ['PG_HOST'],
                       password = os.environ['PG_PASSWORD']
                       )
    return [conn, conn.cursor()]


# Credentials loaded from the command line
def db_init2():
    conn = pg2.connect(dbname = os.environ.get('PG_DATABASE'),
                       user = os.environ.get('PG_USER'),
                       host = os.environ.get('PG_HOST'),
                       password = os.environ.get('PG_PASSWORD')
                       )
    return [conn, conn.cursor()]


# DB Close connections
def db_close(connection, cursor):
    connection.commit()
    cursor.close()
    connection.close()


# Insert all values into a table
def insert_values(connection, table_name, values):
    len_values = len(values)
    values_string = '%s' + (', %s' * (len_values - 1))
    qry_str = 'insert into {table} values (' + values_string + ');'
    # Identifier is required here because there are other values to be inserted
    qry = sql.SQL(qry_str).format(table = sql.Identifier(table_name))
    return qry_execute(connection, qry, values, False)
    
    
# Drop and create table
def drop_create_tables(connection, table_name, fields):
    qry_str = 'drop table if exists {table}; create table {table} %s;' % fields
    qry = sql.SQL(qry_str).format(table = sql.Identifier(table_name))
    return qry_execute(connection, qry, '', False)


# Main query execution function; captures errors
def qry_execute(connection, qry, values, fetch_all):
    cur = connection.cursor()
    try:
        cur.execute(qry, values)
        connection.commit()
        if fetch_all:
            return cur.fetchall() 
    except Exception as err:
        print('Error: ', err)
        print('Error Type: ', type(err))
        return 1


# Depending on the values provided, return specific results
def db_protocols(connection,
                 create_table_name,
                 id_num,
                 reg_name,
                 protocol
                 ):
    # Create initial table
    values1 = '''(reg varchar,
                  part numeric,
                  subpart numeric,
                  sction numeric,
                  subsction numeric,
                  supplementals_alt varchar,
                  htype varchar,
                  htitle varchar,
                  hlink varchar,
                  htext varchar
                  )'''
    drop_create_tables(connection, create_table_name, values1)
    # Pull data
    tname2 = 'dev_all_parts05'
    qry_str2 = 'select * from {table1} where {field1} = %s;'
    # Defaults to reg_name checks first
    if reg_name != '':
        qry2 = sql.SQL(qry_str2).format(table1 = sql.Identifier(tname2),
                                        field1 = sql.Identifier('reg')
                                        )
        values2 = (reg_name, )
    elif id_num != '':
        qry2 = sql.SQL(qry_str2).format(table1 = sql.Identifier(tname2),
                                        field1 = sql.Identifier('id_num')
                                        )
        values2 = (id_num, )
    else:
        qry2 = sql.SQL(qry_str2).format(table1 = sql.Identifier(tname2),
                                        field1 = sql.Identifier('protocol')
                                        )
        values2 = (protocol, )
    return qry_execute(connection, qry2, values2, True)


########################## CSS and JavaScript Parsing #########################
# Only one result found for 'autonumber', but not usable
def search_css(search_text):
    # First find CSS sheets
    html = open('html/css_sheets.html', 'r').read()
    # Turn it into html and parse out the content
    soup = bsp(html, 'html.parser')
    htext = soup.find_all('style')
    # First add all values in list
    list1 = []
    for i in htext:
        for j in i:
            list1.append(j)
    # Add the values of the previous list into another list
    list2 = []
    for k in list1:
        res = k.split(';')
        for l in res:
            if l == '':
                continue
            list2.append(l)
    # Parse the html out of each item and save to a new list
    list3 = []
    for m in list2:
        start = m.find('("') + len('("')
        end = m.find('")')
        link = m[start:end]
        if link == '':
            continue
        list3.append(link)
    # Search in each link and print each result if it contains the styles
    for n in list3:
        html = rq.get(n).text
        if search_text in str(html):
            print('Results found in: ' + n)


# Search through each script tag
# No results found for 'autonumber'
def search_jscripts(srch_text):
    html = open('html/css_sheets.html', 'r').read()
    # Turn it into html and parse out the content
    soup = bsp(html, 'html.parser')
    htext = soup.find_all('script')
    # First add all values in list
    list4 = []
    for p in htext:
        if p.attrs['src'].startswith('//code'):
            continue
        list4.append(p.attrs['src'])
    # Search for string inside each jscript file
    for q in list4:
        txt = rq.get(q).text
        if srch_text in str(txt):
            print('Results found in: ' + q)


############################ Debugging and Testing ############################
# Used for debugging specific sections
# Modify file_name and idnum as appropriate
def debug_headers(id_num, file_name, file_save):
    jname = init_write_file(file_name)
    # Connect to database
    db = db_init()
    conn = db[0]
    cur = db[1]
    tname = 'dev_all_parts04'
    qry_str1 = 'select {field1} from {table1} where {field2} = %s;'
    qry1 = sql.SQL(qry_str1).format(table1 = sql.Identifier(tname),
                                    field1 = sql.Identifier('htext'),
                                    field2 = sql.Identifier('id_num')
                                    )
    values1 = (id_num, )
    res = qry_execute(conn, qry1, values1, True)
    soup = bsp(res[0][0], 'html.parser')
    db_close(conn, cur)
    # Save to file only if specified
    if file_save:
        with open(jname, 'w', encoding = 'utf8') as jf:
            jf.write(soup.prettify())
            jf.close()
    # Start looping through headers
    hlist = ['h1', 'h2', 'h3', 'h4', 'b', 'strong', 'li', 'article']
    for i in hlist:
        headers = soup.find_all(i)
        print('\n')
        print('#' * 80)
        print('Heading: %s\nNumber of headings = %s\n' % (i, str(len(headers))))
        for x, j in enumerate(headers):
            # Make all the text look pretty
            hstr1 = j.get_text().strip()
            hsplit = hstr1.split()
            hstr2 = ''
            for k in hsplit:
                hstr2 += k + ' '
            print(hstr2 + '\n')
            if x == 4:
                break


# Pull html for id_num for various checks
def html_pull(idnum, file_name):
    # Connect to database
    db = db_init()
    conn = db[0]
    cur = db[1]
    tname2 = 'dev_all_parts05'
    qry_str1 = 'select * from {table1} where {field1} = %s;'
    qry1 = sql.SQL(qry_str1).format(table1 = sql.Identifier(tname2),
                                    field1 = sql.Identifier('id_num')
                                    )
    values1 = (idnum, )
    res = qry_execute(conn, qry1, values1, True)
    html = res[0][9]
    soup = bsp(html, 'html.parser')
    write_file(file_name, soup, True)
    db_close(conn, cur)


# Extract all headers to log file
# Currently no h6 tags
# Runtime: 25.965"
def extract_headers(protocol, log_file, get_text_ind):
    start_time = start_function('extract_headers')
    # Connect to database
    db = db_init()
    conn = db[0]
    cur = db[1]
    qry_str1 = 'select * from {table1} where {field1} = %s;'
    qry1 = sql.SQL(qry_str1).format(table1 = sql.Identifier('dev_all_parts05'),
                                    field1 = sql.Identifier('protocol')
                                    )
    values1 = (protocol, )
    res = qry_execute(conn, qry1, values1, True)
    # Start parsing html
    lfile = init_write_file(log_file)
    with open(lfile, 'w', encoding = 'utf8') as lf:
        # Start looping through values
        for i in res:
            idnum = i[0]
            html = i[9]
            soup = bsp(html, 'html.parser')
            for j in soup.find_all(re.compile('^h[1-6]$')):
                if get_text_ind:
                    jprint = j.get_text().strip()
                else:
                    jprint = j
                print('%s: %s' % (idnum, jprint), file = lf)
    db_close(conn, cur)
    end_function(start_time)


# Identify all headers that aren't the norm
# Runtime: 0.038"
def extract_headers_test(read_file, write_file):
    start_time = start_function('extract_headers_test')
    rfile = open(read_file, 'r', encoding = 'utf8')
    lfile = init_write_file(write_file)
    with open(lfile, 'w', encoding = 'utf8') as lf:
        for i in rfile.readlines():
            itext = i.strip().split(' ')[0]
            if itext.lower().startswith('part'):
                continue
            elif itext.lower().startswith('subpart'):
                continue
            elif itext.count('.') > 0:
                continue
            elif itext.lower() == 'pgi':
                continue
            else:
                print(i, file = lf)
    end_function(start_time)


# List all article attributes to find their classes
# Runtime: 23.403"
def article_classes(log_file):
    start_time = start_function('article_classes')
    db = db_init()
    conn = db[0]
    cur = db[1]
    tname1 = 'dev_all_parts05'
    qry_str1 = 'select * from {table1} where {field1} = %s;'
    # Run for the real results
    qry1 = sql.SQL(qry_str1).format(table1 = sql.Identifier(tname1),
                                    field1 = sql.Identifier('protocol')
                                    )
    values1 = (0, )
    res = qry_execute(conn, qry1, values1, True)
    with open(log_file, 'w', encoding = 'utf8') as lf:
        # Start looping through values
        for i in res:
            idnum = i[0]
            reg = i[1]
            part = i[2]
            html = i[9]
            soup = bsp(html, 'html.parser')
            classes = ['nested4',
                       'nested3',
                       'nested2',
                       'nested1',
                       'nested0'
                       ]
            for j in soup.find_all('article'):
                # Need to this in case the articles doesn't have a class
                try:
                    ind = 0
                    for k in j['class']:
                        # Exit early
                        if k in ['topic', 'concept']:
                            continue
                        # Only trigger break if class is not in the lst
                        elif k in classes:
                            ind = 1
                            break
                    # Only list if classes aren't in list
                    if ind == 0:
                        # if not j.find('h5'):
                        print('%s\n%s - %s - %s\n%s' % (cb(),
                                                        idnum,
                                                        reg,
                                                        part,
                                                        j.attrs
                                                        ), file = lf
                              )
                # Runs if there are no classes for the article
                except:
                    continue
    db_close(conn, cur)
    end_function(start_time)


# This lists all the article classes
def article_text(id_num, log_file):
    start_time = start_function('article_text')
    # Connect to database
    db = db_init()
    conn = db[0]
    cur = db[1]
    # Pull data
    tname1 = 'dev_all_parts05'
    qry_str1 = 'select * from {table1} where {field1} = %s;'
    qry1 = sql.SQL(qry_str1).format(table1 = sql.Identifier(tname1),
                                    field1 = sql.Identifier('id_num')
                                    )
    values1 = (id_num, )
    res = qry_execute(conn, qry1, values1, True)
    # Start parsing html
    lfile = init_write_file(log_file)
    with open(lfile, 'w', encoding = 'utf8') as lf:
        # Start looping through values
        for i in res:
            html = i[9]
            soup = bsp(html, 'html.parser')
            for j in soup.find_all('article'):
                print('%s\n%s\n%s' % (cb(),
                                      j.attrs,
                                      j.find_all_next('p')
                                      ), file = lf
                      )
    db_close(conn, cur)
    end_function(start_time)


################################# Protocol 0 ##################################
# Protocol 0: everything has articles and headers, with no bold or lists (366)
# Adds all data for protocol 0
# Depending on the parameters, may be dev or prod
# Runs for:
# far
# dfars
# dfarspgi
# diar
# gsam
# epaar
# hsar
# hudar
# Runtime: 59.802"
def add_prot0(id_num, reg_name, log_file):
    start_time = start_function('mod_protocol0')
    # Connect to database
    db = db_init()
    conn = db[0]
    cur = db[1]
    tname1 = 'dev_all_html_prot0'
    # Depending on what variables are provided, this can either be prod or dev    
    res = db_protocols(conn, tname1, id_num, reg_name, 0)
    # Start parsing html
    lfile = init_write_file(log_file)
    with open(lfile, 'w', encoding = 'utf8') as lf:
        # Start looping through values
        for i in res:
            idnum = i[0]
            reg = i[1]
            part = i[2] 
            url = i[8]
            html = i[9]
            soup = bsp(html, 'html.parser')
            ######################### General Clean-Up ########################
            # Unwrap the following tags
            tag_list = ['br',
                        'span',
                        'nav',
                        'strong'
                        ]
            for j in tag_list:
                [k.unwrap() for k in soup.find_all(j)]
            # Fix the TOC
            # Wrap nested0 article class with header tags
            for j in soup.find_all('article', class_ = 'nested0'):
                if not j:
                    break
                ntag = soup.new_tag('header')
                ntag['class'] = 'toc'
                j.wrap(ntag)
                j.unwrap()
            # Convert the div body tag to nav, but only on the first iteration
            for j in soup.find_all('div', class_ = 'body', limit = 1):
                if not j:
                    break
                # Change the class name to toc
                ntag = soup.new_tag('nav')
                ntag['class'] = 'toc'
                j.wrap(ntag)
                j.unwrap()
            # Reformat the text in the a tags and modify the href's
            for j in soup.find('nav', class_ = 'toc').find_all('a'):
                txt = j.get_text().strip()
                j.string = txt
                j['href'] = header_ids(reg, part, txt, True, lf)             
            # Remove all formatting from tables
            for j in soup.find_all('table'):
                del j['class']
                for k in j.find_all('th'):
                    del k['class']
                    del k['id']
                for k in j.find_all('td'):
                    del k['class']
                for k in j.find_all('p'):
                    k.unwrap()
            # Remove all links to the FAR - they won't work anyway in the app
            for j in soup.find_all('a'):
                try:
                    if not j['href'].startswith('http'):
                        j.unwrap()
                except:
                    continue
            ######################## Table of Contents ########################
            # Modify headers
            for j in soup.find_all(re.compile('^h[1-6]$')):
                # Remove all classes
                del j['class']
                if not j.get_text().strip():
                    j.unwrap()
                    continue
                # Extract all the text and clean-up
                hstr = j.get_text().strip()
                # Unwrap empty header tags
                if hstr == '':
                    j.unwrap()
                    continue                
                # Replace special dash characters
                hstr = hstr.replace('–', '-').replace('—', '-').replace('—', '-')
                # Regex find and reformat heading titles
                hstr = reformat_headers(hstr)
                # Save the header text as the new text
                j.string = hstr
                # Convert headers to bold if they are within other articles
                hres = header_ids(reg, part, hstr, False, lf)
                if hres == 2:
                    ntag = soup.new_tag('b')
                    ntag.string = j.string
                    j.insert_after(ntag)
                    j.unwrap()
                    continue
                # Assign new IDs and replace with the old
                new_id = header_ids(reg, part, hstr, False, lf)
                j['id'] = new_id
            ############################ Main Text ############################
            # Start converting all article classes
            # GSAM = could be subsections or sections, search if contains h4, then process
            # GSAR = (see GSAM)
            # nested4 = supplemental sections
            # nested3 = subsections
            # nested2 = sections
            # 2Col = table with two columns (why?)
            # TOP = subparts (why?)
            # TOLP = subparts (why? - must be a typo...)
            # ANYWHERE = subparts (why?)
            # nested1 = subparts
            # TORP = 1.000 part (why?)
            # nested0 = parts
            for j in soup.find_all('article'):
                # Need to add this in case the articles don't have a class
                try:
                    for k in j['class']:
                        # When converting classes, add it as a list, not a string
                        # Exit searching early
                        if k in ['topic', 'concept']:
                            continue
                        # Replace the following with nested1
                        elif k == 'TORP':
                            j['class'] = ['nested1']
                            continue
                        # Replace the following classes with nested2
                        elif k in ['2Col', 'TOP', 'TOLP', 'ANYWHERE']:
                            j['class'] = ['nested2']
                            continue
                        # The following classes have different headers
                        # Headers start at the largest level and move downoward
                        elif k in ['GSAM', 'GSAR', 'FAC', 'CHANGE']:
                            if j.find('h2') is not None:
                                j['class'] = ['nested1']
                                continue
                            elif j.find('h3') is not None:
                                j['class'] = ['nested2']
                                continue
                            elif j.find('h4') is not None:
                                j['class'] = ['nested3']
                                continue                            
                            elif j.find('h5') is not None:
                                j['class'] = ['nested4']
                                continue
                # Runs if there are no classes for the article
                except:
                    continue
            # For certain articles, the same article classes are nested within them
            # This will check to see if the same articles classes are within
            # If they are, then make it the parent-level nested class
            nested_class1 = ['nested4',
                             'nested3',
                             'nested2',
                             'nested1'
                             ]
            for j in nested_class1:
                nested_number = int(j[len(j) - 1])
                for k in soup.find_all('article', class_ = j):
                    if len(k.find_all('article', class_ = j)):
                        k['class'] = 'nested' + str(nested_number - 1)
                        break
            # Convert all subparts to sections
            for j in soup.find_all('article', class_ = 'nested1'):
                ntag = soup.new_tag('section')
                ntag['class'] = 'subparts'
                j.wrap(ntag)
                j.unwrap()
            # Rename articles to semantic class names
            nested_class2 = ['nested4',
                             'nested3',
                             'nested2'
                             ]
            for j in nested_class2:
                for k in soup.find_all('article', class_ = j):
                    k.attrs = {}
                    if j == 'nested4':
                        k['class'] = 'supplementals'
                    elif j == 'nested3':
                        k['class'] = 'subsections'
                    else:
                        k['class'] = 'sections'
            # Remove all div tags only now since we won't need them anymore
            [j.unwrap() for j in soup.find_all('div')]
            ############################ Add to DB ############################
            # Start adding all text individually based on article classes
            alst = [('article', 'supplementals'),
                    ('article', 'subsections'),
                    ('article', 'sections'),
                    ('section', 'subparts'),
                    ('header', 'toc')
                    ]
            for j in alst:
                for k in soup.find_all(j[0], class_ = j[1]):
                    # Skip if nothing
                    if not k:
                        continue
                    # Unwrap the article if there are no headers:
                    if k.find(re.compile('^h[1-6]$')) is None:
                        print('%s\n%s\n%s\n%s' % (cb(),
                                                  'Missing header, unwrapping from tree. Here is the text:',
                                                  k,
                                                  cb()
                                                  ), file = lf
                              )
                        k.unwrap()
                        continue
                    # Extract the first heading id number for the DB
                    hid = k.find(re.compile('^h[1-6]$'))
                    htext = hid.get_text().strip()
                    # Remove empty paragraphs, delete all attributes
                    for p in k.find_all('p'):
                        p.attrs = {}
                        if p.find('article') or len(p.get_text()) <= 1:
                            p.unwrap()
                    # Insert data
                    res = insert_htext(conn,
                                       tname1,
                                       hid['id'],
                                       k,
                                       htext,
                                       url,
                                       idnum,
                                       lf
                                       )
                    # Exit if error
                    if res == 1:
                        print('%s\n%s\n%s' % (cb(),
                                              'Stopping because of error above.',
                                              cb()
                                              ), file = lf
                              )
                        break
                    # Remove so text won't be copied again
                    k.decompose()
    ################################# Finish ##################################
    # Save the html of the current url to the file
    # fname = init_write_file('html/dev_all_prot0.html')
    # write_file(fname, soup, True)
    db_close(conn, cur)
    end_function(start_time)


# Use regex to identify any matches
def reformat_headers(text):
    # Add spaces for -, in case there aren't any
    text2 = text.replace('- ', ' - ').replace('  ', ' ')
    text3 = text2.replace(' -', ' - ').replace('  ', ' ')
    text4 = text3.replace('--', ' - ')
    # Identifies matches for dashes with no spaces inbetween
    if re.match('.*[0-9]-[a-z].*', text4, re.I):
        return text4.replace('-', ' - ')
    elif re.match('.*[0-9]reserved.*', text4, re.I):
        return text4.replace('Reserved', ' RESERVED')
    elif text4.startswith('2426.7001-2426.7002'):
        return text4.replace('-', ' - ')
    else:
        return text4


# Returns the new ID for each header or href; prepends with # if returning href
def header_ids(reg, part, text, href_ind, log_file):
    # Reformat the string to make it lower
    text2 = text.lower()
    # Perform special functions if headers are of a certain type
    res = header_types(reg, text2)
    if res == 1:
        return dfarspgi_idstr(text2)
    elif res == 2:
        return 2
    # Isolate the citation
    hsp = text2.split()
    hs0 = hsp[0]
    if hs0.startswith('subpart') or \
       hs0.startswith('pgi') or\
       hs0.startswith('§'):
        hs0 = hsp[1]
    if hs0.count('.'):
        hs1 = hs0.split('.')[1]
    else:
        hs1 = ''
    # Only do this for one header in GSAM
    if hs0.startswith('appendix'):
        part = 1
        subpart = 0
        sction = 0
        subsction = 0
        supp_alt = text2.replace(' ', '-')
        htype = 'body'
    # This one section is for idnum 978
    elif hs0.startswith('[reserved]'):
        subpart = 11
        sction = 0
        subsction = 0
        supp_alt = 0
        htype = 'body'
    # Parts
    elif hs0.startswith('part'):
        subpart = 0
        sction = 0
        subsction = 0
        supp_alt = 0
        htype = 'header'
    # Subparts
    elif len(hs1) != '' and len(hs1) <= 2:
        subpart = hs1
        sction = 0
        subsction = 0
        supp_alt = 0
        htype = 'header'
    # Special case for paragraph citations
    elif hs0.count('(') > 0:
        # If there are paragraph citations in the first split, extract them
        fcit = hs0.find('(')
        supp = hs0[fcit:]
        new_cit = hs0.replace(supp, '')
        sub_sct = header_link_section(new_cit.split('.')[1])
        subpart = sub_sct[0]
        sction = sub_sct[1]
        subsction = 0
        supp_alt = supp
        htype = 'body'
    # Sections
    elif hs0.count('-') == 0:
        sub_sct = header_link_section(hs1)
        subpart = sub_sct[0]
        sction = sub_sct[1]
        subsction = 0
        supp_alt = 0
        htype = 'body'
    # Subsections
    elif hs0.count('-') == 1:
        ss_sp = hs0.split('-')
        hsp2 = ss_sp[0].split('.')
        hsp1 = hsp2[1]
        sub_sct = header_link_section(hsp1) 
        subpart = sub_sct[0]
        sction = sub_sct[1]
        subsction = ss_sp[1]
        supp_alt = 0
        htype = 'body'
    # Supplementals
    elif hs0.count('-') > 1:
        ss_sp = hs0.split('-')
        hsp2 = ss_sp[0].split('.')
        hsp1 = hsp2[1]
        sub_sct = header_link_section(hsp1)
        subpart = sub_sct[0]
        sction = sub_sct[1]
        subsction = ss_sp[1]
        supp_alt = ss_sp[2]
        htype = 'body'
    id_str = '%s_%s_%s_%s_%s_%s_%s' % (reg,
                                       part,
                                       subpart,
                                       sction,
                                       subsction,
                                       supp_alt,
                                       htype
                                       )
    # print('%s ##### %s' % (text, id_str))
    # href's require # in order to go to the link on the page
    if href_ind:
        return '#' + id_str
    else:
        return id_str


# Identify the different types of of headers
# 0: process normally
# 1: special DFARS cases
# 2: process all other alternatives
def header_types(reg, text):
    # Isolate the first part of the citation
    # § is replaced brecause if it is still here, then text2[1] won't work
    text2 = text.replace('§ ', '').split(' ')[0]
    # Return for DFARS
    if text2.startswith('assignments') or \
       text2.startswith('spare') or \
       text2[1] == '-':
        return 1
    # Majority of the other citations
    # Process normally for the vast majority of the others
    # appendix and [reserved] are kept here because they are only two sections
    elif text2.startswith('part') or \
         text2.startswith('subpart') or \
         text2.count('.') or \
         text2.startswith('appendix') or \
         text2.startswith('[reserved]') or \
         text2.startswith('pgi'):
        return 0
    # Process alternatives
    # These are headers that will get converted to bold headings
    else:
        return 2


# Returns the section and subsectino; used with header_ids
def header_link_section(text):
    if len(text) == 3:
        subpart = text[0]
        sction = text[1:]
        if sction.startswith('0'):
            sction = text[2]
        else:
            sction = sction.lstrip('0')
    elif len(text) == 4:
        subpart = text[:2]
        sction = text[2:]
        if sction.startswith('0'):
            sction = text[3]
        else:
            sction = sction.lstrip('0')
    # Only found for 3035.70-1 Policy
    elif len(text) == 2:
        subpart = text
        sction = 0
    # This really won't matter as it won't get inserted in the table anyway
    else:
        subpart = 'xxx'
        sction = 'xxx'
    return (subpart, sction)


# Insert htext sections in dev_all_html02 table
def insert_htext(connection,
                 table_name,
                 header_id,
                 text,
                 header_text,
                 url,
                 id_num,
                 log_file
                 ):
    # The header IDs need to be the ones we made, exit function if not
    if header_id.count('_') < 6:
        return
    hid_spl = str(header_id).split('_')
    # Start adding values
    values = (hid_spl[0],
              # part
              hid_spl[1],
              # subpart
              hid_spl[2],
              # sction
              hid_spl[3],
              # subsction
              hid_spl[4],
              # supplemental
              hid_spl[5],
              # htype
              hid_spl[6],
              # htitle,
              header_text,
              # hlink
              url,
              # htext
              str(text)
              )
    print('%s - %s - %s - %s - %s - %s - %s - %s - %s' % (id_num,
                                                          # reg
                                                          hid_spl[0],
                                                          # part
                                                          hid_spl[1],
                                                          # subpart
                                                          hid_spl[2],
                                                          # sction
                                                          hid_spl[3],
                                                          # subsction
                                                          hid_spl[4],
                                                          # supplemental
                                                          hid_spl[5],
                                                          # htype
                                                          hid_spl[6],
                                                          # htitle
                                                          header_text
                                                          # htext
                                                          # text
                                                          ), file = log_file)
    return insert_values(connection, table_name, values)

# Extract specific headers for dfarspgi
def dfarspgi_idstr(text):
    tspl = text.split(' ')[0]
    sub_sect = tspl[len(tspl) - 1]
    supp_alt = tspl.lower().replace('_', '-')
    # For assignments in part 8
    if tspl.lower().startswith('assignment'):
        part = 8
        subpart = 70
        sction = 6
    # Spare headers in part 17
    elif tspl.lower().startswith('spare'):
        part = 17
        subpart = 75
        sction = 6
    # All sections below the spare headers
    elif text[1] == '-':
        part = 17
        subpart = 75
        sction = 6
    id_str = '%s_%s_%s_%s_%s_%s_%s' % ('dfarspgi',
                                       part,
                                       subpart,
                                       sction,
                                       sub_sect,
                                       supp_alt,
                                       'body'
                                       )
    return id_str


################################# Protocol 1 ##################################
# Protocol 1: no headers, bold and lists for paragraphs (526)
# Add values for protocol 1
# Regs affected:
# sofars
# agar
# aidar
# car
# dears
# dolar
# dosar
# dtar
# edar
# fehbar
# hhsar
# iaar
# jar
# lifar
# nrcar
# tar
def add_prot1(id_num, reg_name, log_file):
    start_time = start_function('add_prot1')
    # Connect to database
    db = db_init()
    conn = db[0]
    cur = db[1]
    tname1 = 'dev_all_html_prot1'
    # Depending on what variables are provided, this can either be prod or dev    
    res = db_protocols(conn, tname1, id_num, reg_name, 1)
    # Start parsing html
    lfile = init_write_file(log_file)
    with open(lfile, 'w', encoding = 'utf8') as lf:
        # Start looping through values
        for i in res:
            idnum = i[0]
            reg = i[1]
            part = i[2] 
            url = i[8]
            html = i[9]
            soup = bsp(html, 'html.parser')
            print(idnum)
            ######################### General Clean-Up #########################
            # Unwrap the initial div tags
            soup.find('div', class_ = 'field-item even').decompose()
            soup.find('div', class_ = 'field-items').unwrap()
            try:
                soup.find('div', class_ = 'regnavigation').decompose()
            except:
                pass
            # Unwrap all blockqoute tags
            try:
                [i.unwrap() for i in soup.find_all('blockquote')]
            except:
                pass
            #################### Header - Table of Contents ####################
            # First remove all the strong tags
            for x, i in enumerate(soup.find_all('p')):
                # The first iteration will be the h1 heading
                if x == 0:
                    if soup.find('h1'):
                        res = soup.find('h1')
                        hstr = str(res)
                        continue
                    else:
                        res = i
                        hstr = str(i)
                        continue
                # If the paragraphs contain strong tags, then those are headers
                # Each time we find a strong tag, we want to decompose the tag
                elif i.find('strong'):
                    htext = i.get_text().strip()
                    # Stop the for loop when you find the Part after the TOC
                    if re.match('.*(\s)part(\s)[1-9].*', htext, re.I):
                        break
                    # In either case, add the text to the main string to be added later
                    else:
                        hstr += str(i) + ''
                        i.decompose()
                else:
                    hstr += str(i) + ''
                    i.decompose()
            # Add nav to encompass all the text
            ntag1 = soup.new_tag('nav')
            # htext is currently a string - it needs to be converted to html       
            ntag1.append(bsp(hstr, 'html.parser'))
            # Replace the first h1 paragraph to the new tag
            res.replace_with(ntag1)
            # Wrap nav tags with headers
            ntag2 = soup.new_tag('header')
            ntag2['class'] = 'toc'
            soup.find('nav').wrap(ntag2) 
            # Fix tags in the toc
            # Convert h1 headers
            if soup.find('h1'):
                for i in soup.find_all('h1'):
                    i['id'] = '%s_1_0_0_0_0_header' % reg
                    i.string = htext
                    soup.find('nav').insert_before(i)
                    i.decompose()
            else:
                for i in soup.find_all('p'):
                    htext = i.get_text().strip()
                    if re.match('.*(\s)part(\s)[1-9].*', htext, re.I):
                        ntag = soup.new_tag('h1')
                        ntag['id'] = '%s_1_0_0_0_0_header' % reg
                        ntag.string = htext
                        soup.find('nav').insert_before(ntag)
                        i.decompose()
                        break
            # Remove all strong headers to plain paragraph
            for i in soup.find('header').find_all('p'):
                if i.find('strong'):
                    strong = i.find('strong')
                    ntag = soup.new_tag('p')
                    ntag.string = strong.get_text().strip()
                    i.insert_before(ntag)
                    strong.decompose()
                    continue
            # Clean-up text in the nav section, but only for SOFARS Part 1
            if reg == 'sofars' and \
                part == '1':
                # Fix the nav section
                for i in soup.find('nav').find_all('p'):
                    htext = i.get_text().strip()
                    # Remove all empty paragraph tags
                    if not htext:
                        i.decompose()
                        continue
                    # Check the first elements in each list of title strings
                    htsp = htext.split()
                    if not htsp[0][0].isalpha() and \
                        not htsp[0].startswith('(') and \
                        not htsp[0].lower().startswith('subpart') and \
                        not htsp[0].lower().startswith('attachment'):
                        jstr = []
                        # Search through the list backwards in order to add in the later
                        #     citations first, since inserting tags first will end up
                        #     showing up last
                        for x, j in reversed(list(enumerate(htsp[:len(htsp)]))):
                            jstr.insert(0, j)
                            # Stop iterating through lists as soon as you come across a citation
                            # Lists get cleared and reset once you come across a citation
                            if not j[0].isalpha() and \
                                not j.lower().startswith('(removed') and \
                                not j.startswith('-') and \
                                not j.count(')'):
                                ntag = soup.new_tag('p')
                                ntag.string = ' '.join(jstr)
                                i.insert_after(ntag)
                                jstr = []
                        # All paragraph tags get decomposed, since they're all inserted anyway
                        i.decompose()
                    else:
                        continue
            # Add href to toc listing
            for i in soup.find('nav').find_all('p'):
                htext = i.get_text().strip()
                # Don't run for paragraph text that starts with '(', which are typically
                #     for removed and added notes
                if not htext.startswith('('):
                    hrf = header_ids(reg, part, htext, True, lf)
                    # The only a tags already present already have href
                    if i.find('a'):
                        hrf = i.find('a')['href']
                    i.clear()
                    ntag = soup.new_tag('a')
                    ntag.string = htext
                    ntag['href'] = hrf
                    i.append(ntag)
            # Add in hr after h1 and at the very end
            try:
                [i.unwrap() for i in soup.find_all('hr')]
            except:
                pass
            ntag1 = soup.new_tag('hr')
            soup.find('h1').insert_after(ntag1)
            ntag2 = soup.new_tag('hr')
            soup.find('header').append(ntag2)
            ############################ Main Text ############################
            # Wrap everything outside the header tag in main tag
            res = soup.find('header').find_next_sibling()
            hstr = str(res)
            for i in res.find_next_siblings():
                hstr += str(i) + ''
                i.decompose()
            ntag = soup.new_tag('main')
            ntag.append(bsp(hstr, 'html.parser'))
            res.replace_with(ntag)
            main = soup.find('main')
            main_p = main.find_all('p')
            # Remove the main part paragraph - it's already h1
            for i in main_p:
                htext = i.get_text().strip()
                if re.match('.*(\s)part(\s)[1-9].*', htext, re.I):
                    i.decompose()
                    break
            # Convert all p tags that contain supposed headers, which have span anchor class
            for i in main_p:
                if i.find('span', class_ = 'anchor'):
                    htext = i.get_text().strip()
                    hfirst = htext.lower().split()[0]
                    hdr = return_header(hfirst, htext)
                    if hdr == '':
                        i.find('span').unwrap()
                        continue
                    ntag = soup.new_tag(hdr)
                    ntag.string = htext
                    ntag['id'] = header_ids(reg, part, htext, False, lf)
                    i.insert_after(ntag)
                    i.decompose()
            # Convert other p tags to headers based on their first text
            for i in main_p:
                htext = i.get_text().strip()
                if not len(htext):
                    i.decompose()
                    continue
                hfirst = htext.lower().split()[0]
                # Can't start with '(' and must start with subpart or number
                if not hfirst.startswith('(') and \
                    (hfirst.startswith('subpart') or \
                    not hfirst[0].isalpha()):
                    hdr = return_header(hfirst, htext)
                    if hdr == '':
                        continue
                    ntag = soup.new_tag(hdr)
                    ntag.string = htext
                    ntag['id'] = header_ids(reg, part, htext, False, lf)
                    i.insert_after(ntag)
                    i.decompose()
            # Remove all strong tags; conver to bold if in a table
            for i in soup.find_all('strong'):
                if i.parent.name == 'th' or \
                    i.parent.name == 'td':
                    ntag = soup.new_tag('b')
                    ntag.string = i.get_text().strip()
                    i.replace_with(ntag)
                # Only need to unwrap the tags if theyre in a normal paragraph
                else:
                    i.unwrap()
            # Wrap headers in tags
            htags = ['h2', 'h3', 'h4', 'h5']
            for i in htags:
                if i == 'h2':
                    tg = 'section'
                    clss = 'subparts'
                elif i == 'h3':
                    tg = 'article'
                    clss = 'sections'
                elif i == 'h4':
                    tg = 'article'
                    clss = 'subsections'
                else:
                    tg = 'article'
                    clss = 'supplementals'
                # Separate all subparts into sections
                for j in soup.find_all(i):
                    jstr = str(j)
                    for k in j.find_next_siblings():
                        # Stop when you find another header of the same type
                        if k.name == j.name:
                            break
                        # After everything, append strings
                        else:
                            jstr += str(k) + ''
                            k.decompose()
                    ntag = soup.new_tag(tg)
                    ntag['class'] = clss
                    ntag.append(bsp(jstr, 'html.parser'))
                    j.replace_with(ntag)
            # Fix ordered lists, if present
            ptype = para_type(soup)
            if ptype == 'ol':
                for i in soup.find_all('ol'):
                    for j in i.find_all('li'):
                        #print('%s\n%s' % (cb(), j), file = log_file)
                        j.unwrap()
                    ptype = i['type']
                    try:
                        pstart = i['start']
                    except:
                        pstart = 1
                    for x, j in enumerate(i.find_all('p')):
                        pcit = return_para(ptype, int(pstart) + x)
                        j.contents.insert(0, pcit)
                        kstr = ''
                        for k in j.contents:
                            kstr += str(k) + ''
                        # ''.join(j.contents)
                        # print(pfin)
                        ntag = soup.new_tag('p')
                        ntag.append(bsp(kstr, 'html.parser'))
                        j.replace_with(ntag)
                    i.unwrap()
            elif ptype == 'ul':
                print('ul type: skipped for now...')
            # Remove all links except those that were created by header_ids
            for j in soup.find_all('a'):
                try:
                    jh = j['href']
                    if not jh.startswith('http') and \
                        not jh.startswith('#' + reg):
                        j.unwrap()
                except:
                    continue
            ######################### Add to Database #########################
            # First add in supplementals
            alst = [('article', 'supplementals'),
                    ('article', 'subsections'),
                    ('article', 'sections'),
                    ('section', 'subparts'),
                    ('header', 'toc')
                    ]
            for i in alst:
                for j in soup.find_all(i[0], class_ = i[1]):
                    if j:
                        hid = j.find(re.compile('^h[1-6]$'))
                        htext = hid.get_text().strip()
                        # Insert data
                        res = insert_htext(conn,
                                           tname1,
                                           hid['id'],
                                           j,
                                           htext,
                                           url,
                                           id_num,
                                           lf
                                           )
                        # Exit if error
                        if res == 1:
                            print('%s\n%s\n%s' % (cb(),
                                                  'Stopping because of error above.',
                                                  cb()
                                                  ), file = lf
                                  )
                            break
                        # Remove so text won't be copied again
                        j.decompose()    
    ################################## Finish #################################
    # Save the html of the current url to the file
    fname = init_write_file('html/dev_all_prot1.html')
    write_file(fname, soup, True)
    db_close(conn, cur)
    end_function(start_time)


def return_header(first, full_text):
    dcount = first.count('-')
    if first.startswith('('):
        return ''
    elif first.startswith('subpart'):
        return 'h2'
    elif first.count('.') == 1:
        if dcount == 0:
            return 'h3'
        elif dcount == 1:
            return 'h4'
        elif dcount > 1:
            return 'h5'
    else:
        return ''


# Define how to process the paragraph types:
# ol = ol type with types and start with no citations in the text
# ol2 = ol type with no types or starts
# ul = unordered lists with citations already in the text
def para_type(soup):
    ol_res = soup.find_all('ol')
    if ol_res:
        try:
            for i in ol_res:
                if i['type'] == 'a' or \
                    i['type'] == '1' or \
                    i['type'] == 'i':
                    return 'ol'
        except:
            return 'ol2'
    else:
        return 'ul'


# Convert number to roman numeral
def return_para(val, num):
    # For regular letters
    if val.isalpha() and \
        val != 'i':
        letters = 'abcdefghijklmnopqrstuvwxyz'
        return '(%s) ' % letters[num - 1]
    # For numbers
    if not val.isalpha():
        return '(%s) ' % (str(int(val) + num - 1))
    # For roman numerals
    else:
        nstr = str(num)
        nlen = len(nstr)
        # Right-most value of val
        rnum = int(nstr[nlen - 1])
        if rnum <= 3:
            rval = 'i' * int(rnum)
        elif rnum == 4:
            rval = 'iv'
        elif rnum == 5:
            rval = 'v'
        elif rnum >= 6 and rnum <= 8:
            rval = 'v' + ('i' * (int(rnum) - 5))
        elif rnum == 9:
            rval  = 'ix'
        # Left-most value of val
        x_qty = 0
        if nlen > 1:
            x_qty = int(nstr[0])
        lval = 'x' * x_qty
        # Return final value
        return '(%s) ' % (lval + rval)


################################# Protocol 2 ##################################
# Protocol 2: vaar specific, strong for everything and h2 = h1 (47)


################################# Protocol 3 ##################################
# Protocol 3: nfs specific, only p tags and literally nothing else (49)


################################# Protocol 4 ##################################
# Protocol 4: contains headers, but no articles (294)


