
import os
from os import path
from dotenv import load_dotenv
from bs4 import BeautifulSoup as bsp
import urllib as ul
import requests as rq
import re
import psycopg2 as pg2
from psycopg2 import sql
from psycopg2.extensions import AsIs
import time
import datetime


#################################### Basics ###################################
# Remove all file contents before writing anything, but only if it exists
def init_write_file(file_name):
    if path.exists(file_name):
        open(file_name, 'w').close()
    return file_name


# Start timer for functinos
def start_function(func_name):
    start_time = time.time()
    print('\n' + ('#' * 80))
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


################################### DB Tasks ##################################
# DB Init
# Credentials loaded from .env file
def dbi():
    load_dotenv('../.env')
    conn = pg2.connect(dbname = os.environ['PG_DATABASE'],
                       user = os.environ['PG_USER'],
                       host = os.environ['PG_HOST'],
                       password = os.environ['PG_PASSWORD']
                       )
    return [conn, conn.cursor()]


# Credentials loaded from the command line
def dbi2():
    conn = pg2.connect(dbname = os.environ.get('PG_DATABASE'),
                       user = os.environ.get('PG_USER'),
                       host = os.environ.get('PG_HOST'),
                       password = os.environ.get('PG_PASSWORD')
                       )
    return [conn, conn.cursor()]


# DB Close connections
def dbcl(connection, cursor):
    connection.commit()
    cursor.close()
    connection.close()


# Select all for a given table
def select_all(connection, table_name):
    # Tables can be concatenated in, but not the arguments
    cur = connection.cursor()
    qry = 'select * from %s;'
    # Single values in tuples require an extra comma to register as a tuple
    # Multiple values don't, since those are already multiples
    cur.execute(qry,
                (AsIs(table_name),
                 ))
    results = cur.fetchall()
    for i in results:
        print(i)
    dbcl(connection, cur)


# Insert all values into a table
def insert_values(connection, table_name, values):
    cur = connection.cursor()
    len_values = len(values)
    values_string = '%s' + (', %s' * (len_values - 1))
    qry = 'insert into {table} values (' + values_string + ');'
    # Identifier is required here because there are other values to be inserted
    cur.execute(sql.SQL(qry).format(table = sql.Identifier(table_name)),
                values
                )
    connection.commit()
    
    
# Drop and create table
def drop_create_tables(connection, table_name, table_values):
    cur = connection.cursor()
    qry = 'drop table if exists %s; create table %s %s;'
    # AsIs is required because table names don't require quotes
    cur.execute(qry,
                (AsIs(table_name),
                 AsIs(table_name),
                 AsIs(table_values)
                 ))
    connection.commit()


# Updates only one field in a table
# Maybe later update to include logic to update multiple fields
def update_one(connection, table_name, field_name, value, id_num):
    cur = connection.cursor()
    qry = 'update {table} set {field} = %s where id_num = %s'
    cur.execute(sql.SQL(qry).format(table = sql.Identifier(table_name),
                                    field = sql.Identifier(field_name)),
                (value, id_num)
                )
    connection.commit()


# Main query execution function; captures errors
def qry_execute(connection, qry, values, fetch_ind):
    cur = connection.cursor()
    try:
        cur.execute(qry, values)
    except Exception as err:
        print('Error: ', err)
        print('Error Type: ', type(err))
        return
    connection.commit()
    if fetch_ind:
        return cur.fetchall()
    

################################# Update Data #################################
# Add links to href sites
# Runtime: 1.105"
def add_reg_links():
    start_time = start_function('add_reg_links')
    # The following string could have been anywhere on acq.gov
    srch = 'https://www.acquisition.gov/browse/index/far'
    # Open the url and save it as an html object
    html_res = rq.get(srch).text
    # Turn it into html and parse out the content
    soup = bsp(html_res, 'html.parser')
    htext = soup.find('div', class_ = 'reg-container clearfix')
    res = htext.find_all('a')
    # Connect to database
    conn = dbi()[0]
    cur = dbi()[1]
    tname = 'dev_reg_links'
    values = '(reg varchar, link varchar, order_num integer)'
    drop_create_tables(conn, tname, values)
    order_num = 1
    # Start adding values
    for i in res:
        rtext = i.get_text()
        reg = rtext.strip()
        hrtext = i.attrs['href']
        href = hrtext.strip().replace('/browse/index', '')
        # Skip over the smart regs
        if 'Smart' in reg:
            continue
        lst = [reg,
               str(href),
               order_num]
        insert_values(conn, tname, tuple(lst))
        order_num += 1        
        # The supplemental AFFARS regs aren't normally found
        if reg == 'AFFARS':
            order_num = add_affars_supp(conn, tname, order_num)
    # Finish
    dbcl(conn, cur)
    end_function(start_time)


# Add supplemental AFFARS regulations; used with dev_add_reg_links
def add_affars_supp(db_conn, table_name, order_num):
    lst = ['AFFARS MP',
           '/affars/mp',
           order_num
           ]
    insert_values(db_conn, table_name, tuple(lst))
    # order_num gets added by 1 in order to add another level of affars regs
    order_num += 1
    lst.clear()
    lst = ['AFFARS PGI',
           '/affars/pgi',
           order_num
           ]
    insert_values(db_conn, table_name, tuple(lst))
    order_num += 1
    return order_num


# Start extracting links to the Parts and save href in json file
# Runtime: 13.891"
def add_all_parts():
    start_time = start_function('add_all_parts')
    # Connect to database
    db = dbi()
    conn = db[0]
    cur = db[1]
    tname = 'dev_all_parts'
    values = '''(part varchar,
                subpart varchar,
                section varchar,
                subsection varchar,
                paragraph varchar,
                reg varchar,
                htype varchar,
                fac varchar,
                hlink varchar,
                htext varchar,
                order_num numeric,
                import_date varchar)
                '''
    drop_create_tables(conn, tname, values)
    cur.execute('select * from %s;', (AsIs('dev_reg_links'), ))
    res = cur.fetchall()
    # Start adding values
    for i in res:
        htext = str(i[1])
        reg = htext.strip('/')
        print('Adding data to: ' + reg)
        parts_hrefs(conn, tname, reg, htext, i[2])
    # Finish
    dbcl(conn, cur)
    end_function(start_time)


# Parse each part for each regulation; used with db_add_all_parts
def parts_hrefs(connection,
                table_name,
                regulation,
                htext,
                order):
    # Open the url and save it as an html object
    reg = regulation.strip()
    reg = reg.strip('_')
    base = 'https://www.acquisition.gov'
    hlink = base + htext
    html = rq.get(hlink).text
    hsoup = bsp(html, 'html.parser')
    # Finding this div applies to FAR, DFARS, and GSAM
    # If there were no results, it would be a null object
    hres = hsoup.find('div', id = 'parts-wrapper')
    if hres is not None:
        # All the a tags have our information within the div tag
        # ind variable used depending on which option we use here
        res = hres.div.find_all('a')
        ind = 1
    # This only gets run for supplementals
    # The tbody tag will always have our information
    # The td tags have long class names, so regex was needed to parse it
    else:
        res = hsoup.tbody.find_all('td', class_ = re.compile('.*part-number'))
        ind = 0
    add_to_list(connection, table_name, reg, res, base, ind, order)


# Adds everything to db; used with db_parts_hrefs
def add_to_list(connection,
                table_name,
                regulation,
                rlist,
                addr,
                reg_ind,
                order):
    for i in rlist:
        # The part numbers will always just be the text
        hpart = return_part(i.get_text()).strip()
        part_final = final_part(hpart)
        # If its for the main regs, 'href' will be in the 'attrs'
        if reg_ind == 1:
            hlnk = addr + i.attrs['href'].strip()
        else:
            hlnk = addr + i.a['href'].strip()
        # Start populating list with part
        lst = [part_final,
               # subpart
               0,
               # section
               0,
               # subsection
               0,
               # paragraph
               0,
               # reg
               regulation.replace('/', ''),
               # htype
               'main',
               # fac
               '2021-04',
               # hlink
               hlnk,
               # htext
               'N/A',
               # order_num
               order,
               # import_date
               datetime.datetime.now()
               ]
        insert_values(connection, table_name, tuple(lst))


# Returns the part number regardless of what type it is; used with parts_href
def return_part(ptext):
    sp_text = ptext.split()
    cnt = len(sp_text)
    # If its just a number, the list will be 1 object
    if cnt > 1:
        ptext = sp_text[cnt - 1]
    return ptext


# Return only the far equivalent part; used with db_add_to_list
def final_part(part):
    strip_part1 = part.strip("mp_")
    strip_part2 = strip_part1.strip("pgi_")
    lp = len(strip_part2)
    if lp <= 2:
        return strip_part2
    elif lp == 3:
        if strip_part2[1] == str(0):
            return strip_part2[2]
        else:
            return strip_part2[1:]
    elif lp == 4:
        if strip_part2[2] == str(0):
            return strip_part2[3]
        else:
            return strip_part2[2:]
    else:
        return strip_part2


# Adds crucial row numbers to each record
# Runtime: 0.282"
def add_id_nums():
    start_time = start_function('add_id_nums')
    db = dbi()
    conn = db[0]
    cur = db[1]
    sql_file = 'sql/add_id_nums.sql'
    cur.execute(open(sql_file, 'r', encoding = 'utf8').read())
    # Finish
    dbcl(conn, cur)
    end_function(start_time)


# Update the AFFARS MP parts; performed after add_row_nums
# Runtime: 0.09"
def update_affars_mp():
    start_time = start_function('update_affars_mp')
    db = dbi()
    conn = db[0]
    cur = db[1]
    # First create another table just in case we need to use the other
    tname = 'dev_all_parts3'
    qry_str1 = 'drop table if exists %s; create table %s as select * from %s;'
    values1 = (AsIs(tname),
               AsIs(tname),
               AsIs('dev_all_parts2')
               )
    qry_execute(conn, qry_str1, values1, False)
    # Run a separate query for just the affars mp regs
    qry_str2 = 'select * from %s where %s = %s'
    values2 = (AsIs(tname),
               AsIs('reg'),
               ('affarsmp',
               ))
    results = qry_execute(conn, qry_str2, values2, True)
    for i in results:
        idnum = i[0]
        part = i[1]

        spart = part.split('.')
        final_part = str(spart[0][2:]).lstrip('0')
        # Most, not all, affarsmp parts are citations to be parsed        
        # First split on hyphens
        try:
            spart2 = spart[1].split('-')
        except:
            continue
        spl2_1 = spart2[0]
        num_spart2 = len(spart2)
        lspart2 = len(spl2_1)
        # First get subpart and section
        if lspart2 <= 3:
            final_subpart = spl2_1[0]
            if lspart2 == 1:
                final_section = 0
            else:
                final_section = spl2_1[1:].lstrip('0')
        # Also a regular reference but 4 characters long
        elif lspart2 == 4:
            final_subpart = spl2_1[:2]
            final_section = spl2_1[2:].lstrip('0')
        # These never had a - and are much longer
        else:
            spl_spart2 = spl2_1.split('(')[0]
            if len(spl_spart2) == 3:
                final_subpart = spl_spart2[0]
                final_section = spl_spart2[1:].lstrip('0')
            else:
                final_subpart = spl_spart2[:2]
                final_section = spl_spart2[2:].lstrip('0')
        # Pull subsections
        if num_spart2 == 2:
            if '(' not in str(spart2[1]):
                final_subsection = spart2[1]
            else:
                final_subsection = spart2[1].split('(')[0]
        else:
            final_subsection = 0
        find_para = part.find('(')
        final_paragraph = 0
        if find_para != -1:
            final_paragraph = part[find_para:]
        print('%s: %s - %s - %s - %s - %s' % (part,
                                              final_part,
                                              final_subpart,
                                              final_section,
                                              final_subsection,
                                              final_paragraph
                                              ))
        # Updates all values in table
        qry_str3 = '''update {table}
                      set {field1} = %s,
                          {field2} = %s,
                          {field3} = %s,
                          {field4} = %s,
                          {field5} = %s
                          where {field6} = %s
                     '''
        qry3 = sql.SQL(qry_str3).format(table = sql.Identifier(tname),
                                        field1 = sql.Identifier('part'),
                                        field2 = sql.Identifier('subpart'),
                                        field3 = sql.Identifier('section'),
                                        field4 = sql.Identifier('subsection'),
                                        field5 = sql.Identifier('paragraph'),
                                        field6 = sql.Identifier('id_num'))
        values = (final_part,
                  final_subpart,
                  final_section,
                  final_subsection,
                  final_paragraph,
                  idnum
                  )
        qry_execute(conn, qry3, values, False)
    # Finish
    dbcl(conn, cur)
    end_function(start_time)


# Updates table to include html portion of the web link provided
# Runtime: 21' 14.195"
def add_html():
    start_time = start_function('add_html')
    # Connect to database
    db = dbi()
    conn = db[0]
    cur = db[1]
    tname = 'dev_all_parts2'
    qry = 'select * from %s order by %s;'
    cur.execute(qry,
                (AsIs(tname), 
                 AsIs('id_num')
                 ))
    res = cur.fetchall()
    # Start adding html to the DB
    for i in res:
        url = i[9]
        idnum = i[0]
        print('%s: Working' % (str(idnum)))
        try:
            html = rq.get(url).text
        except:
            print("Can't read URL - skipping for now...")
            continue
        # The following is the old method to convert non-ascii characters
        # Using requests instead of urllib solves this but keeping the below anyway
        # # id_num 96 and 144 have ASCII characters in their title
        # # This converts their characters to UTF-8
        # try:
        #     html = rq.get(url).text
        # except:
        #     print('UTF-8 Problems...')
        #     url = str(str(url).encode('utf-8'))
        #     url_final = url[2:len(url) - 1]
        #     update_one(conn, tname, 'hlink', url_final, idnum)
        #     print('%s: Updated' % (str(idnum)))
        #     html = rq.get(url).text
        soup = bsp(html, 'html.parser')
        # All the main content is listed under the class below
        hres = soup.find('div', class_ = 'field-items')
        # For all others, content is listed under 'field-items'
        update_one(conn, tname, 'htext', str(hres), idnum)
    # Finish
    dbcl(conn, cur)
    end_function(start_time)


# Count the amount of tags for each reg
# Runtime: 1' 2.646"
def tag_counts():
    start_time = start_function('tag_counts')
    db = dbi()
    conn = db[0]
    cur = db[1]
    tname = 'dev_tag_counts'
    values = '''(id_num numeric,
                 part varchar,
                 reg varchar,
                 h1 numeric,
                 h2 numeric,
                 h3 numeric,
                 h4 numeric,
                 bld numeric,
                 strong numeric,
                 li numeric,
                 htext varchar
                 )'''
    drop_create_tables(conn, tname, values)
    qry = 'select %s, %s, %s, %s from %s order by %s;'
    cur.execute(qry,
                (AsIs('id_num'),
                 AsIs('part'),
                 AsIs('reg'),
                 AsIs('htext'),
                 AsIs('dev_all_parts2'),
                 AsIs('id_num')
                 ))
    results = cur.fetchall()
    for i in results:
        print(i[0])
        soup = bsp(i[3], 'html.parser')
        h1count = len(soup.find_all('h1'))
        h2count = len(soup.find_all('h2'))
        h3count = len(soup.find_all('h3'))
        h4count = len(soup.find_all('h4'))
        bcount = len(soup.find_all('b'))
        strcount = len(soup.find_all('strong'))
        licount = len(soup.find_all('li'))
        # Add values to list, starting with id_num
        lst = [i[0],
               # part
               i[1],
               # reg
               i[2],
               # h1
               h1count,
               # h2
               h2count,
               # h3
               h3count,
               # h4
               h4count,
               # b
               bcount,
               # strong
               strcount,
               # lists
               licount,
               # htext
               i[3]
               ]
        insert_values(conn, tname, tuple(lst))
    dbcl(conn, cur)
    end_function(start_time)






