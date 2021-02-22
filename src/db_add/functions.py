
import os
from os import path
from dotenv import load_dotenv
from bs4 import BeautifulSoup as bsp
import urllib as ul
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
    print('\nFunction: %s\nStarting...' % (func_name))
    return start_time


# End timer for functions
def end_function(start_time):
    print("Function finished in %s seconds" % round(time.time() - start_time, 3))



# Connect to DB
# Credentials loaded to .env file
def db_connect():
    load_dotenv('../.env')
    conn = pg2.connect(dbname = os.environ['DB_NAME'],
                       user = 'postgres',
                       host = 'localhost',
                       password = os.environ['DB_PW'])
    return conn


# Select all for a given table
def select_all(connection, table_name):
    # Tables can be concatenated in, but not the arguments
    cur = connection.cursor()
    qry = 'select * from %s;'
    # Single values in tuples require an extra comma to register as a tuple
    # Multiple values don't, since those are already multiples
    cur.execute(qry, (AsIs(table_name), ))
    results = cur.fetchall()
    for i in results:
        print(i)
    connection.commit()
    cur.close()


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
def drop_create_tables(curs, table_name, table_values):
    qry = 'drop table if exists %s; create table %s %s'
    # AsIs is required because table names don't require quotes
    curs.execute(qry, (AsIs(table_name),
                       AsIs(table_name),
                       AsIs(table_values)
                       ))


# Add links to href sites
# Runtime: 1.105 seconds
def add_reg_links():
    start_time = start_function('add_reg_links')
    # The following string could have been anywhere on acq.gov
    srch = 'https://www.acquisition.gov/browse/index/far'
    # Open the url and save it as an html object
    resp = ul.request.urlopen(srch)
    html_res = resp.read()
    # Turn it into html and parse out the content
    soup = bsp(html_res, 'html.parser')
    htext = soup.find('div', class_ = 'reg-container clearfix')
    res = htext.find_all('a')
    # Connect to database
    conn = db_connect()
    cur = conn.cursor()
    tname = 'dev_reg_links'
    values = '(reg varchar, link varchar, order_num integer)'
    drop_create_tables(cur, tname, values)
    order_num = 1
    # Start adding values
    for i in res:
        rtext = i.get_text()
        reg = rtext.strip()
        hrtext = i.attrs['href']
        href = hrtext.strip().replace('/browse/index', '')
        # Error checks
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
    conn.commit()
    cur.close()
    end_function(start_time)


# Add supplemental AFFARS regulations; used with dev_add_reg_links
def add_affars_supp(db_conn,
                    table_name,
                    order_num):
    lst = ['AFFARS MP',
           '/affars/mp',
           order_num
           ]
    insert_values(db_conn, table_name, tuple(lst))
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
# Runtime: 13.891 seconds
def add_all_parts():
    start_time = start_function('add_all_parts')
    # Connect to database
    conn = db_connect()
    cur = conn.cursor()
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
    drop_create_tables(cur, tname, values)
    cur.execute('select * from %s;', (AsIs('dev_reg_links'), ))
    res = cur.fetchall()
    # Start adding values
    for i in res:
        htext = str(i[1])
        reg = htext.strip('/')
        print('Adding data to: ' + reg)
        parts_hrefs(conn, tname, reg, htext, i[2])
    # Finish
    conn.commit()
    cur.close()
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
    html = ul.request.urlopen(hlink).read()
    hsoup = bsp(html, 'html.parser')
    # Finding this div applies to FAR, DFARS, and GSAM
    # If there were no results, it would be a null object
    hres = hsoup.find('div', id = 'parts-wrapper')
    if hres is not None:
        # All the a tags have our information within the div tag   
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
               # type
               'main',
               # fac
               '2021-04',
               # link
               hlnk,
               # html
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
# Runtime: 0.282 seconds
def add_row_nums():
    start_time = start_function('add_row_nums')
    conn = db_connect()
    cur = conn.cursor()
    sql_file = 'sql/add_row_nums.sql'
    cur.execute(open(sql_file, 'r', encoding = 'utf8').read())
    conn.commit()
    cur.close()
    end_function(start_time)


# Update the AFFARS MP parts; performed after add_row_nums
# Runtime: 0.09 seconds
def update_affars_mp():
    start_time = start_function('update_affars_mp')
    conn = db_connect()
    cur = conn.cursor()
    tname = 'dev_all_parts2'
    fname = 'id_num'
    qry = 'select * from {table} where {field} >= %s and {field} <= %s'
    cur.execute(sql.SQL(qry).format(table = sql.Identifier(tname),
                                    field = sql.Identifier(fname)),
                (277, 296)
                )
    results = cur.fetchall()
    for i in results:
        idnum = i[12]
        part = i[0]
        spart = part.split('.')
        final_part = str(spart[0][2:]).lstrip('0')
        # First split on hyphens
        spart2 = spart[1].split('-')
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
            final_subpart = spl2_1[:1]
            final_section = spl2_1[2:].lstrip('0')
        # These never had a - and are much longer
        else:
            spl_spart2 = spl2_1.split('(')[0]
            if len(spl_spart2) == 3:
                final_subpart = spl_spart2[0]
                final_section = spl_spart2[1:].lstrip('0')
            else:
                final_subpart = spl_spart2[:1]
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
        qry2 = '''update {table}
                  set {field1} = %s,
                      {field2} = %s,
                      {field3} = %s,
                      {field4} = %s,
                      {field5} = %s
                  where {field6} = %s
                  '''
        cur.execute(sql.SQL(qry2).format(table = sql.Identifier(tname),
                                         field1 = sql.Identifier('part'),
                                         field2 = sql.Identifier('subpart'),
                                         field3 = sql.Identifier('section'),
                                         field4 = sql.Identifier('subsection'),
                                         field5 = sql.Identifier('paragraph'),
                                         field6 = sql.Identifier('id_num')),
                    (final_part,
                    final_subpart,
                    final_section,
                    final_subsection,
                    final_paragraph,
                    idnum
                    ))
    # Finish
    conn.commit()
    cur.close()
    end_function(start_time)


# Updates table to include html portion of the web link provided
# Total run time: 1595.066 seconds
def add_html():
    start_time = time.time()
    print('\nFunction: add_html\nStarting...')
    # Connect to database
    conn = db_connect()
    cur = conn.cursor()
    tname = 'dev_all_parts2'
    qry = 'select * from %s order by %s;'
    cur.execute(qry, (AsIs(tname), 
                      AsIs('id_num')
                      ))
    res = cur.fetchall()
    # Start adding html to the DB
    for i in res:
        url = i[8]
        idnum = i[12]
        print('%s: Working' % (str(idnum)))
        # id_num 96 and 144 have ASCII characters in their title
        # This converts their characters to UTF-8
        try:
            html = ul.request.urlopen(url).read()
        except:
            url = str(str(url).encode('utf-8'))
            url_final = url[2:len(url) - 1]
            update_one(cur, tname, 'hlink', url_final, idnum)
            print('%s: Updated' % (str(idnum)))
            html = ul.request.urlopen(url_final).read()
        soup = bsp(html, 'html.parser')
        # All the main content is listed under the class below
        hres = soup.find('div', class_ = 'field-items')
        # For all others, content is listed under 'field-items'
        update_one(cur, tname, 'htext', str(hres), idnum)
    # Finish
    conn.commit()
    cur.close()
    print('Function finished in %s seconds' % round(time.time() - start_time, 3))
    

# Updates only one field in a table
# Maybe later update to include logic to update multiple fields
def update_one(cur, table_name, field_name, value, id_num):
    qry = 'update {table} set {field} = %s where id_num = %s'
    cur.execute(sql.SQL(qry).format(table = sql.Identifier(table_name),
                                    field = sql.Identifier(field_name)),
                (value, id_num)
                )









