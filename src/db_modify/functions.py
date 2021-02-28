
import os
from os import path
from dotenv import load_dotenv
from bs4 import BeautifulSoup as bsp
import requests as rq
import re
import psycopg2 as pg2
from psycopg2 import sql
from psycopg2.extensions import AsIs
import time


# Tables to be used after running this code:
# dev_all_parts05


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
    qry_execute(connection, qry, values, False)
    
    
# Drop and create table
def drop_create_tables(connection, table_name, fields):
    qry_str = 'drop table if exists {table}; create table {table} %s;' % fields
    qry = sql.SQL(qry_str).format(table = sql.Identifier(table_name))
    qry_execute(connection, qry, '', False)


# Main query execution function; captures errors
def qry_execute(connection, qry, values, fetch_all):
    cur = connection.cursor()
    try:
        cur.execute(qry, values)
    except Exception as err:
        print('Error: ', err)
        print('Error Type: ', type(err))
        return
    connection.commit()
    if fetch_all:
        return cur.fetchall()
    

################################# Update Data #################################
# Adds crucial row numbers to each record
# Runtime: 0.282"
def add_id_nums():
    start_time = start_function('add_id_nums')
    db = db_init()
    conn = db[0]
    cur = db[1]
    sql_file = 'sql/add_id_nums.sql'
    cur.execute(open(sql_file, 'r', encoding = 'utf8').read())
    db_close(conn, cur)
    end_function(start_time)
    

# Add the main html to the main table
# Runtime: 0.829"
def add_main_html():
    start_time = start_function('add_main_html')
    db = db_init()
    conn = db[0]
    cur = db[1]
    sql_file = 'sql/add_main_html.sql'
    cur.execute(open(sql_file, 'r', encoding = 'utf8').read())
    db_close(conn, cur)
    end_function(start_time)


# Count the amount of tags for each reg
# Runtime: 57.325"
def tag_counts():
    start_time = start_function('tag_counts')
    db = db_init()
    conn = db[0]
    cur = db[1]
    tname = 'dev_tag_counts01'
    values = '''(id_num numeric,
                 reg varchar,
                 part varchar,
                 h1 numeric,
                 h2 numeric,
                 h3 numeric,
                 h4 numeric,
                 bld numeric,
                 strong numeric,
                 li numeric,
                 article numeric
                 )'''
    drop_create_tables(conn, tname, values)
    qry_str1 = 'select %s, %s, %s, %s from %s order by %s;'
    values1 = (AsIs('id_num'),
               AsIs('reg'),
               AsIs('part'),
               AsIs('htext'),
               AsIs('dev_all_parts04'),
               AsIs('id_num')
               )
    results = qry_execute(conn, qry_str1, values1, True)
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
        artcount = len(soup.find_all('article'))
        # Add values to list, starting with id_num
        lst = [i[0],
               # reg
               i[1],
               # part
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
               # articles
               artcount
               ]
        insert_values(conn, tname, tuple(lst))
    db_close(conn, cur)
    end_function(start_time)


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


# Add protocols as a result of the tag counts, respective of their reg
# Also update the all_parts table to include their new protocol
# Runtime: 0.234"
def add_protocols():
    start_time = start_function('add_protocols')
    db = db_init()
    conn = db[0]
    cur = db[1]
    sql_file = 'sql/add_protocols.sql'
    cur.execute(open(sql_file, 'r', encoding = 'utf8').read())
    db_close(conn, cur)
    end_function(start_time)


