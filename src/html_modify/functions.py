
import os
from os import path
from dotenv import load_dotenv
from bs4 import BeautifulSoup as bsp
import requests as rq
import re
import psycopg2 as pg2
from psycopg2 import sql
import time


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
    

################################# Update Data #################################
# Used for debugging specific sections
# Modify file_name and idnum as appropriate
def debug_headers(idnum, file_name, file_save):
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
    values1 = (idnum, )
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


################################# Protocol 0 ##################################
# Adds all data to postgres DB Modify
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
    # Create initial table
    tname1 = 'dev_all_html02'
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
    drop_create_tables(conn, tname1, values1)
    # Pull data
    tname2 = 'dev_all_parts05'
    qry_str2 = 'select * from {table1} where {field1} = %s;'
    # Depending on what variables are provided, this can either be prod or dev
    if id_num != '':
        qry2 = sql.SQL(qry_str2).format(table1 = sql.Identifier(tname2),
                                        field1 = sql.Identifier('id_num')
                                        )
        values2 = (id_num, )
    elif reg_name != '':
        qry2 = sql.SQL(qry_str2).format(table1 = sql.Identifier(tname2),
                                        field1 = sql.Identifier('reg')
                                        )
        values2 = (reg_name, )    
    else:
        qry2 = sql.SQL(qry_str2).format(table1 = sql.Identifier(tname2),
                                        field1 = sql.Identifier('protocol')
                                        )
        values2 = (0, )
    res = qry_execute(conn, qry2, values2, True)
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
            # Remove all breaks
            for j in soup.find_all('br'):
                j.unwrap()
            # Remove all span classes and subsequent autonumbers
            for j in soup.find_all('span'):
                j.unwrap()
            # Remove emphasis classes
            for j in soup.find_all('em'):
                j.unwrap()
            # Remove nav classes
            for j in soup.find_all('nav'):
                j.extract()
            # Modify headers
            for j in soup.find_all(re.compile('^h[1-6]$')):
                # Remove all classes
                del j['class']
                if j.get_text().strip() is None:
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
                hres = header_ids(reg, part, hstr, False, lf, idnum)
                if hres == 2:
                    ntag = soup.new_tag('b')
                    ntag.string = j.string
                    j.insert_after(ntag)
                    j.unwrap()
                    continue
                # Assign new IDs and replace with the old
                new_id = header_ids(reg, part, hstr, False, lf, idnum)
                j['id'] = new_id
            # Fix the TOC
            div_toc = soup.find('div', class_ = 'body')
            if div_toc is not None:
                # Change the class name to toc
                div_toc['id'] = 'toc'
                # Reformat the text in the a tags and modify the href's
                for k in div_toc.find_all('a'):
                    txt = k.get_text().strip()
                    k.string = txt
                    k['href'] = header_ids(reg, part, txt, True, lf, idnum)             
            else:
                print('No div body', file = lf)
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
                    jh = j['href']
                    if not jh.startswith('http') and not jh.startswith('#' + reg):
                        j.unwrap()
                except:
                    continue
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
            nested_class = ['nested4',
                            'nested3',
                            'nested2',
                            'nested1',
                            'nested0'
                            ]
            for j in nested_class:
                nested_number = int(j[len(j) - 1])
                for k in soup.find_all('article', class_ = j):
                    if len(k.find_all('article', class_ = j)):
                        k['class'] = 'nested' + str(nested_number - 1)
                        break
            # Start adding all text individually based on article classes
            for j in nested_class:
                for k in soup.find_all('article', class_ = j):
                    if k is None:
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
                    # Remove empty paragraphs
                    for p in k.find_all('p'):
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
def header_ids(reg, part, text, href_ind, log_file, idnum):
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


# The results of the searches suggest that the tags I'm looking for are
# embedded somewhere else. If I can't find them anywhere, then the only
# other way to go about this is to save everything as is and apply my own
# tags. For obvious reasons, this would be much too impractical. It would
# invovled:
# - saving all the text as is, only find non-header tags, check to see if it
#   starts with an open parenthesis then go to the first close parenthesis
# - this would leave me to parse-out the paragraph
# - depending on what type of paragraph it is, it could require a specific
#   indent
# - we already know the strucutre of the FAR, so this would be a simple test
# - they will always go a, 1, i, A, 1, i
# - knowing this would mean I can set-up indents based on what value this is


# Links within html should be the following:
#   PART_SUBPART_SECTION_SUBSECTION_REG_TYPE
# For example: FAR 1.105-2 = 1_1_5_2_far_body
# PART: integers from 0-53
# SUPBART: integers from 0-?
# SECTION: integers from 0-?
# SUBSECTION: integers from 0-?
# REG: the regulation in lower case with no spaces; citations shall not include
#      the supplemental regulation number in front; for example, a reference
#      for DFARS 202.101 will not be 202_1_1_0_dfars_body, but instead will be
#      1_1_1_0_dfars_body
# TYPE: the type of link in reference:
#   - body: the most prevalent, the citation html body
#   - toc: the toc for each part and each associated regulation
#   - main: the concatentation of the toc, and all appropriate bodies

# As such, the associated database will be structured similarly:
# 'part'
# 'subpart'
# 'section'
# 'subsection'
# 'reg'
# 'type'
# 'fac'
# 'link'
# 'html'


################################ HTML Scraping ################################
# Calling it:
# cdev = paragraph_attributes(num2)
# final_list = []
# for x, i in enumerate(num2):
#     final_list.append(cdev.get_attributes(x))
# for i in final_list:
#     idict = json.loads(i)
#     print('paragraph: ' + idict['para'])

# Create attributes for the paragraph citations listed
# Attributes:
# lst: list of all paragraphs; returns list
# lnum: list number, starts at 0; returns integer
# paragraph: paragraph is pulled from the list number; returns string
# is_alpha: paragraph is a letter; returns boolean
# is_caps: paragraph is a capital letter; returns boolean
# prev_value: previous value in the list; returns string
# prev_is_alpha: previous value is a letter; returns boolean
# prev_letter: previous letter, skips over numbers; returns string
# prev_letter_caps: previous letter is in caps; returns boolean
# next_value: next value in the list; returns string
# next_is_alpha: next value is a letter; returns boolean
# next_letter: next letter, excludes integers; returns string
# next_letter_caps: next letter is in caps; returns boolean
# is_rom_numeral =  paragraph is a roman numeral; returns boolean
# is_num_last = paragraph is number after capital paragraphs; returns boolean
# is_rom_num_last = paragraph is roman numeral after last numbers; returns boolean
class paragraph_attributes:
    def __init__(self, list_object):
        self.lst = list_object
    # Define all the attributes listed above
    def get_attributes(self, list_number):
        lnum = list_number
        paragraph = self.lst[lnum]
        is_alpha = paragraph.isalpha()
        is_caps = paragraph.isupper()
        # Previous value attributes
        if lnum != 0:
            prev_value = self.lst[lnum - 1]
            prev_is_alpha = prev_value.isalpha()
        else:
            prev_value = 'N/A'
            prev_is_alpha = False
        # Next value attributes
        if (lnum + 1) != len(self.lst):
            next_value = self.lst[lnum + 1]
            next_is_alpha = next_value.isalpha()
        else:
            next_value = 'N/A'
            next_is_alpha = False
        # Check whether is a value or roman numeral
        is_rom_numeral = is_rnum(lnum,
                                 self.lst,
                                 paragraph,
                                 is_alpha,
                                 next_value,
                                 next_is_alpha
                                 )
        # Finally, find the indentation level of the paragraph
        # Currently, can't find any way to detect if the number or roman
        #   numeral citation is the first or second tier
        # As such, it will remain as false for now; taking too long to solve...
        if not is_alpha:
            is_alpha2 = is_number2(lnum, self.lst, paragraph)        
        if is_rom_numeral:
            is_rom_numeral2 = is_rnum2(lnum, self.lst, paragraph)
        indentation = find_indentation(paragraph,
                                       is_alpha,
                                       is_rom_numeral,
                                       is_caps,
                                       is_alpha2,
                                       is_rom_numeral2
                                       )
        # Save data in a dictionary, and return it
        d = {'iter': lnum,
             'para': paragraph,
             'ind': indentation,
             'pv': prev_value,
             'pv_al': prev_is_alpha,
             'nv': next_value,
             'nv_al': next_is_alpha
             }
        return json.dumps(d, indent = 2)


# Returns whether the paragraph is a roman numeral
# All roman numerals share the following characteristics:
#   - prev value may be number
#   - next value may be capital A
#   - next value may be ii
#   - prev actual letter could have been <= h
#   - NOT: next value is 1
#   - next value may be i
#   - is alpha and has two or more characters
def is_rnum(para_iteration,
            para_list,
            para_val,
            para_is_alpha,
            next_val,
            next_val_is_alpha
            ):
    if para_iteration == 0:
        return False
    elif para_val == 'i':
        new_list = []
        for x, i in reversed(list(enumerate(para_list[:(para_iteration)]))):
            # Skip over upper-case paragraphs
            if str(i).isupper():
                continue
            new_list.append(i)
            # Only do testing if the string is a letter
            if str(i).isalpha():
                # ...'g', 1, 2, 3, 'i', 1...
                if next_val == 1:
                    return False
                # ...'g', 1, 2, 3, 'i', 4...
                elif next_val_is_alpha == False and next_val != 1:
                    return True
                # ...'g', 1, 2, 3, 'i', 'ii'...
                elif next_val_is_alpha and next_val[0] in 'ivx':
                    return True
                # Tests for 'i' to 'i' lists
                if str(i)[0] in 'ivx':
                    # ...'h', 1, 'i', 'i'...
                    if len(new_list) == 1:
                        return False
                    # ...'h', 1, 'i', 2, 3, 'i', 'j'...
                    elif next_val_is_alpha and next_val[0] not in 'ivx':
                        return False
                # Tests for non 'i' to 'i' lists
                else:
                    # ...'g', 1, 'h', 'i'...
                    if len(new_list) == 1:
                        return True
                    # ...'g', 1, 2, 3, 'i', 'h'...
                    elif next_val_is_alpha and next_val[0] not in 'ivx':
                        return True
                break
    elif para_is_alpha and para_val[0] in 'ivx' and next_val != 1:
        return True
    

# FAR 52.209-5
# 1  3  4  4  4  4  5  6  6   5  6  6   6     6   3  2  1  1  1  1
# a, i, A, B, C, D, 1, i, ii, 2, 1, ii, iii, iv, ii, 2, b, c, d, e
#                                         \/ no             \/ yes
# a, b, c, 1, 2, 3, i, ii, A, B, 1, 2, 3, 4, i, C, 1, i, D, 4, 5
#                                         \/ no             \/ yes
# a, b, c, 1, 2, 3, i, ii, A, B, 1, 2, 3, 4, i, C, 1, i, D, 4, 5
#                                         \/ yes               \/ no
# a, b, c, 1, 2, 3, i, ii, A, B, 1, 2, 3, 4, iii, A, 1, iv, A, 4, 5
#                                         \/ yes               \/ no
# a, b, c, 1, 2, 3, i, ii, A, B, 1, 2, 3, 4, C, 1, iv, A, 4, 5    
#                                         \/ yes
# a, b, c, 1, 2, 3, i, ii, A, B, 1, 2, 3, 4, d, 1, i, A, 1, 2
#                                         \/ no
# a, b, c, 1, 2, 3, i, ii, A, B, 1, 2, 3, 4, d, 1, i, A, 1, 2


# Determine if this is the second set of roman numerals
# IN PROCESS: currently just returning False
def is_rnum2(para_iteration,
             para_list,
             para_val
             ):
    return False  
    

# Determine if this is the second set of numbers
# IN PROCESS: currently just returning False
def is_number2(para_iteration,
               para_list,
               para_val
               ):
    return False 


# Returns the indentation level
# Paragraphs will be listed in the following format:
# (a)
# (1)
# (i)
# (A)
# (1)
# (i)
def find_indentation(para_val,
                     para_is_alpha,     
                     para_is_rnum,
                     para_is_caps,
                     para_is_num2,
                     para_is_rnum2
                     ):
    if para_is_alpha and para_is_caps != True and para_is_rnum != True:
        return 1
    elif para_is_alpha != True and para_is_num2 != True:
        return 2
    elif para_is_rnum:
        return 3
    elif para_is_caps:
        return 4
    elif para_is_num2:
        return 5
    elif para_is_rnum2:
        return 6


#prev_is_alpha == False and \
# print(chr(ord(char) - 25))


#charac = input()

# if charac == "Z": # If Z encountered change to A
#    print(chr(ord(charac)-25))

# else:
#    change = ord(charac) + 1
#    print(chr(change))

# Old copy just in case
# class PCitation:
#     def __init__(self, list_object):
#         self.lst = list_object

#     # Define all the attributes listed above
#     def get_attributes(self, list_number):
#         lnum = list_number
#         citation = str(self.lst[lnum])
#         is_alpha = citation.isalpha()
#         is_caps = citation.isupper()

#         # Previous value attributes
#         if lnum != 0:
#             prev_value = str(self.lst[lnum - 1])
#             prev_is_alpha = prev_value.isalpha()
#             prev_letter = 'N/A'
#             prev_letter_caps = False
#             for x, i in reversed(list(enumerate(self.lst[:(lnum)]))):
#                 if str(i).isalpha():
#                     prev_letter = str(i)
#                     prev_letter_caps = prev_letter.isupper()
#                     break
#         else:
#             prev_value = 'N/A'
#             prev_is_alpha = False
#             prev_letter = 'N/A'
#             prev_letter_caps = False

#         # Next value attributes
#         if (lnum + 1) != len(self.lst):
#             next_value = str(self.lst[lnum + 1])
#             next_is_alpha = next_value.isalpha()
#             next_letter = 'N/A'
#             next_letter_caps = False
#             for x, i in enumerate(self.lst[(lnum + 1):len(self.lst)]):
#                 if str(i).isalpha():
#                     next_letter = str(i)
#                     next_letter_caps = next_letter.isupper()
#                     break
#         else:
#             next_value = 'N/A'
#             next_is_alpha = False
#             next_letter = 'N/A'
#             next_letter_caps = False

#         # Finally, check if the value is roman numeral, or just a letter
#         # All roman numerals share the following characteristics:
#         #   - prev value may be number
#         #   - next value may be capital A
#         #   - next value may be ii
#         #   - prev actual letter could have been <= h
#         #   - NOT: next value is 1
#         #   - next value may be i
#         #   - is alpha and has two or more characters
#         if is_alpha and \
#            citation[0] in 'ivx' and \
#            next_value != 1:
#             is_rom_numeral = True
#         else:
#             is_rom_numeral = False

#         # Special roman numeral check but only if this is an 'i'
#         if citation == 'i':
#             is_rom_numeral = case_i_rnum(lnum,
#                                          self.lst,
#                                          next_value,
#                                          next_is_alpha)


#         # Save data in a dictionary, and return it
#         d = {
#             'citation': citation,
#             # 'prev_letter': prev_letter,
#             # 'next_letter': next_letter,
#             'is_rnumeral': is_rom_numeral          
#             # 'is_alpha': is_alpha,
#             # 'prev_val_alpha': prev_is_alpha

#             }
#         #print(json.dumps(d, indent = 2))
#         return d

