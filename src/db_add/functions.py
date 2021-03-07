
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup as bsp
import requests as rq
import re
import psycopg2 as pg2
from psycopg2 import sql
import time


# Tables to be used after running these functions:
# - dev_all_parts02
# - all_html01
# - reg_links01


#################################### Basics ###################################
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


################################## Add Data ##################################
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
    db = db_init()
    conn = db[0]
    cur = db[1]
    tname = 'reg_links01'
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
        lst = [reg, str(href), order_num]
        insert_values(conn, tname, tuple(lst))
        order_num += 1        
        # The supplemental AFFARS regs aren't normally found
        if reg == 'AFFARS':
            order_num = add_affars_supp(conn, tname, order_num)
    db_close(conn, cur)
    end_function(start_time)


# Add supplemental AFFARS regulations; used with dev_add_reg_links
def add_affars_supp(db_conn, table_name, order_num):
    lst = ['AFFARS MP', '/affars/mp', order_num]
    insert_values(db_conn, table_name, tuple(lst))
    # order_num gets added by 1 in order to add another level of affars regs
    order_num += 1
    lst.clear()
    lst = ['AFFARS PGI', '/affars/pgi', order_num]
    insert_values(db_conn, table_name, tuple(lst))
    order_num += 1
    return order_num


# Start extracting links to the Parts and save href in json file
# Runtime: 13.891"
def add_all_parts():
    start_time = start_function('add_all_parts')
    # Connect to database
    db = db_init()
    conn = db[0]
    cur = db[1]
    tname = 'dev_all_parts01'
    values1 = '''(reg varchar,
                  part varchar,
                  subpart varchar,
                  sction varchar,
                  subsction varchar,
                  paragraph varchar,
                  htype varchar,
                  hlink varchar,
                  htext varchar,
                  order_num numeric
                  )'''
    drop_create_tables(conn, tname, values1)
    qry_str1 = 'select * from {table1};'
    qry1 = sql.SQL(qry_str1).format(table1 = sql.Identifier('reg_links01'))
    res = qry_execute(conn, qry1, '', True)
    # Start adding values
    for i in res:
        htext = str(i[1])
        reg = htext.strip('/')
        print('Adding data to: ' + reg)
        parts_hrefs(conn, tname, reg, htext, i[2])
    db_close(conn, cur)
    end_function(start_time)


# Parse each part for each regulation; used with db_add_all_parts
def parts_hrefs(connection, table_name, regulation, htext, order):
    # Open the url and save it as an html object
    reg = regulation.strip()
    reg = reg.strip('_')
    base = 'https://www.acquisition.gov'
    hlink = base + htext
    html = rq.get(hlink).text
    soup = bsp(html, 'html.parser')
    # Finding this div applies to FAR, DFARS, and GSAM
    hres = soup.find('div', id = 'parts-wrapper')
    if hres is not None:
        # The clearfix tag has all the links
        res = hres.find_all('div', class_ = 'clearfix')
    # This only gets run for supplementals
    # The tbody tag will always have our information
    # The td tags have long class names, so regex was needed to parse it
    else:
        res = soup.tbody.find_all('td', class_ = re.compile('.*part-number'))
    add_to_list(connection, table_name, reg, res, base, order)


# Adds everything to db; used with parts_hrefs
def add_to_list(connection, table_name, regulation, rlist, addr, order):
    # This first for loop is only really used the DFARS Appendix's
    # The DFARS Appendix gets run twice, everything else runs once
    for i in rlist:
        for j in i.find_all('a'):
            hpart = return_part(j.get_text()).strip()
            part_final = final_part(hpart)
            hlnk = addr + j['href'].strip()
            # Start populating list with the reg
            lst = [regulation.replace('/', ''),
                   # part
                   part_final,
                   # subpart
                   0,
                   # section
                   0,
                   # subsection
                   0,
                   # paragraph
                   0,
                   # htype
                   'main',
                   # hlink
                   hlnk,
                   # htext
                   'N/A',
                   # order_num
                   order
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


# Update the AFFARS MP parts; performed after add_row_nums
# Runtime: 0.09"
def update_affars_mp():
    start_time = start_function('update_affars_mp')
    db = db_init()
    conn = db[0]
    cur = db[1]
    # This new table will have all the updated affarsmp values
    tname = 'dev_all_parts02'
    qry_str1 = '''drop table if exists {table1};
                  create table {table1} as
                  select *
                  from {table2};
                  '''
    qry1 = sql.SQL(qry_str1).format(table1 = sql.Identifier(tname),
                                    table2 = sql.Identifier('dev_all_parts01')
                                    )
    qry_execute(conn, qry1, '', False)
    # Run a separate query for just the affars mp regs
    qry_str2 = 'select * from {table1} where {field1} = %s'
    qry2 = sql.SQL(qry_str2).format(table1 = sql.Identifier(tname),
                                    field1 = sql.Identifier('reg')
                                    )
    values2 = ('affarsmp', )
    results = qry_execute(conn, qry2, values2, True)
    for i in results:
        part = i[1]
        hlink = i[7]
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
        # Take the rest of the paragraph sring at the leftmost point
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
        qry_str3 = '''update {table1}
                      set {field1} = %s,
                          {field2} = %s,
                          {field3} = %s,
                          {field4} = %s,
                          {field5} = %s
                          where {field6} = %s
                     '''
        qry3 = sql.SQL(qry_str3).format(table1 = sql.Identifier(tname),
                                        field1 = sql.Identifier('part'),
                                        field2 = sql.Identifier('subpart'),
                                        field3 = sql.Identifier('sction'),
                                        field4 = sql.Identifier('subsction'),
                                        field5 = sql.Identifier('paragraph'),
                                        field6 = sql.Identifier('hlink')
                                        )
        values3 = (final_part,
                   final_subpart,
                   final_section,
                   final_subsection,
                   final_paragraph,
                   hlink
                   )
        qry_execute(conn, qry3, values3, False)
    db_close(conn, cur)
    end_function(start_time)


# Updates table to include html portion of the web link provided
# Runtime: 42' 30.683"
def add_html():
    start_time = start_function('add_html')
    # Connect to database
    db = db_init()
    conn = db[0]
    cur = db[1]
    tname = 'all_html01'
    old_tname = 'dev_all_parts02'
    # Need select * statement since it will be what we fetch
    qry_str1 = '''drop table if exists {table1};
                  create table {table1} as
                  select {field1},
                         {field2}
                  from {table2};
                  select * from {table1};
                  '''
    qry1 = sql.SQL(qry_str1).format(table1 = sql.Identifier(tname),
                                    table2 = sql.Identifier(old_tname),
                                    field1 = sql.Identifier('hlink'),
                                    field2 = sql.Identifier('htext')
                                    )
    res = qry_execute(conn, qry1, '', True)
    # Start adding html to the DB
    for i in res:
        url = i[0]
        print('%s: Working' % (url))
        try:
            html = rq.get(url).text
        except:
            print("Can't read URL - skipping for now...")
            continue
        soup = bsp(html, 'html.parser')
        # All the main content is listed under the class below
        hres = soup.find('div', class_ = 'field-items')
        # For all others, content is listed under 'field-items'
        qry_str2 = 'update {table1} set {field1} = %s where {field2} = %s;'
        qry2 = sql.SQL(qry_str2).format(table1 = sql.Identifier(tname),
                                        field1 = sql.Identifier('htext'),
                                        field2 = sql.Identifier('hlink')
                                        )
        values2 = (str(hres), url)
        qry_execute(conn, qry2, values2, False)
    db_close(conn, cur)
    end_function(start_time)
    # The following is the old method to convert non-ascii characters
    # Using requests instead of urllib solves this but keeping the below anyway
    # try:
    #     html = rq.get(url).text
    # except:
    #     print('UTF-8 Problems...')
    #     url = str(str(url).encode('utf-8'))
    #     url_final = url[2:len(url) - 1]
    #     update_one(conn, tname, 'hlink', url_final, idnum)
    #     print('%s: Updated' % (str(idnum)))
    #     html = rq.get(url).text


