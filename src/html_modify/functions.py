
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

