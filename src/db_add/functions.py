
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup as bsp
import urllib as ul
import re
import psycopg2 as pg2
from psycopg2 import sql
from psycopg2.extensions import AsIs


################################## PostgreSQL #################################
# Connect to DB
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


# Add all FAR parts and titles
def db_far_parts():
    print('\nStarting db_far_parts')
    # https://acqnotes.com/acqnote/careerfields/federal-acquisition-regulation-index
    far = ['Part 1-Federal Acquisition Regulations System', 
           'Part 2-Definitions of Words and Terms', 
           'Part 3-Improper Business Practices and Personal Conflicts of Interest', 
           'Part 4-Administrative Matters', 
           'Part 5-Publicizing Contract Actions', 
           'Part 6-Competition Requirements', 
           'Part 7-Acquisition Planning', 
           'Part 8-Required Sources of Supplies and Services', 
           'Part 9-Contractor Qualifications', 
           'Part 10-Market Research', 
           'Part 11-Describing Agency Needs', 
           'Part 12-Acquisition of Commercial Items', 
           'Part 13-Simplified Acquisition Procedures', 
           'Part 14-Sealed Bidding', 
           'Part 15-Contracting by Negotiation', 
           'Part 16-Types of Contracts', 
           'Part 17-Special Contracting Methods', 
           'Part 18-Emergency Acquisitions', 
           'Part 19-Small Business Programs', 
           'Part 20-[RESERVED, not currently in use]', 
           'Part 21-[RESERVED, not currently in use]', 
           'Part 22-Application of Labor Laws to Government Acquisitions', 
           'Part 23-Environment, Energy and Water Efficiency, Renewable Energy Technologies, Occupational Safety, and Drug-Free Workplace', 
           'Part 24-Protection of Privacy and Freedom of Information', 
           'Part 25-Foreign Acquisition', 
           'Part 26-Other Socioeconomic Programs', 
           'Part 27-Patents, Data, and Copyrights', 
           'Part 28-Bonds and Insurance', 
           'Part 29-Taxes', 
           'Part 30-Cost Accounting Standards Administration', 
           'Part 31-Contract Cost Principles and Procedures', 
           'Part 32-Contract Financing', 
           'Part 33-Protests, Disputes, and Appeals', 
           'Part 34-Major System Acquisition', 
           'Part 35-Research and Development Contracting', 
           'Part 36-Construction and Architect-Engineer Contracts', 
           'Part 37-Service Contracting', 
           'Part 38-Federal Supply Schedule Contracting', 
           'Part 39-Acquisition of Information Technology', 
           'Part 40-[RESERVED, not currently in use]', 
           'Part 41-Acquisition of Utility Services', 
           'Part 42-Contract Administration and Audit Services', 
           'Part 43-Contract Modifications', 
           'Part 44-Subcontracting Policies and Procedures', 
           'Part 45-Government Property', 
           'Part 46-Quality Assurance', 
           'Part 47-Transportation', 
           'Part 48-Value Engineering', 
           'Part 49-Termination of Contracts', 
           'Part 50-Extraordinary Contractual Actions', 
           'Part 51-Use of Government Sources by Contractors', 
           'Part 52-Solicitation Provisions and Contract Clauses', 
           'Part 53-Forms'
           ]
    
    # Connect to database
    conn = db_connect()
    cur = conn.cursor()
    tname = 'far_parts'
    values = '(part integer, title text)'
    drop_create_tables(cur, tname, values)

    # Start adding values
    for i in far:
        spl = i.split('-')
        part = spl[0]
        name = spl[1]
        fpart = part.split(' ')[1]
        fname = name.replace(fpart + '-', '')
        # Error checks
        if 'RESERVED' in fname:
            fname = 'RESERVED'
        lst = []
        lst.append(int(fpart))
        lst.append(str(fname))
        tup = tuple(lst)
        insert_values(conn, tname, tup)
        
    # Finish
    conn.commit()
    select_all(conn, tname)
    cur.close()
    print('Done updating ' + tname)


# Add links to href sits
def db_add_reg_links():
    print('\nStarting db_add_reg_links')
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
    tname = 'reg_links'
    values = '(reg text, link text)'
    drop_create_tables(cur, tname, values)
    
    # Start adding values
    for i in res:
        rtext = i.get_text()
        reg = rtext.strip()
        hrtext = i.attrs['href']
        href = hrtext.strip().replace('/browse/index', '')
        # Error checks
        if 'Smart' in reg:
            continue
        lst = []
        lst.append(reg)
        lst.append(str(href))
        tup = tuple(lst)
        insert_values(conn, tname, tup)
        
    # Add AFFARS regs to the list
    lst = []
    lst.append('AFFARS MP')
    lst.append('/affars/mp')
    tup = tuple(lst)
    insert_values(conn, tname, tup)
    lst.clear()
    lst.append('AFFARS PGI')
    lst.append('/affars/pgi')
    tup = tuple(lst)
    insert_values(conn, tname, tup)
    lst.clear()
    # Finish
    conn.commit()
    select_all(conn, tname)
    cur.close()
    print('Done updating ' + tname)


# Start extracting links to the Parts and save href in json file
def db_add_all_parts():
    print('\nStarting db_add_all_parts')
    # Connect to database
    conn = db_connect()
    cur = conn.cursor()
    tname = 'all_parts'
    values = '''(part text,
                subpart text,
                section text,
                subsection text,
                reg text,
                type text,
                fac text,
                link text,
                html text)
                '''
    drop_create_tables(cur, tname, values)
    qry2 = 'select * from reg_links;'
    cur.execute(qry2)
    res = cur.fetchall()
    
    # Start adding values
    for i in res:
        htext = str(i[1])
        reg = htext.strip('/')
        print('Adding data to: ' + reg)
        db_parts_hrefs(conn, reg, htext)
        
    # Add row numbers to each value
    add_row_nums(cur, tname, tname + '_final')
    # Finish
    conn.commit()
    cur.close()
    print('Done with ' + tname)


# Parse each part for each regulation; used with add_all_parts
def db_parts_hrefs(connection, regulation, htext):
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
    db_add_to_list(connection, reg, res, base, ind)


# Adds everything to db
def db_add_to_list(connection, regulation, rlist, addr, reg_ind):
    for i in rlist:
        # The part numbers will always just be the text
        hpart = return_part(i.get_text()).strip()
        part_final = final_part(hpart)
        # If its for the main regs, 'href' will be in the 'attrs'
        if reg_ind == 1:
            hlnk = addr + i.attrs['href'].strip()
        else:
            hlnk = addr + i.a['href'].strip()
        lst = []
        # part
        lst.append(part_final)
        # subpart
        lst.append(0)
        # section
        lst.append(0)
        # subsection
        lst.append(0)
        # reg
        lst.append(regulation.replace('/', ''))
        # type
        lst.append('main')
        # fac
        lst.append('2021-04')
        # link
        lst.append(hlnk)
        # html
        lst.append('N/A')
        tup = tuple(lst)
        insert_values(connection, 'all_parts', tup)


# Returns the part number regardless of what type it is; used with parts_href
def return_part(ptext):
    sp_text = ptext.split()
    cnt = len(sp_text)
    # If its just a number, the list will be 1 object
    if cnt > 1:
        ptext = sp_text[cnt - 1]
    return ptext


# Return only the far equivalent part; used with add_to_dict
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


def add_row_nums(curs, orig_tname, new_tname):
    qry = '''drop table if exists %s;
             create table %s as
             select %s.*,
                    row_number() over() as id_num
             from %s;
             drop table %s;
             '''
    curs.execute(qry, (AsIs(new_tname),
                       AsIs(new_tname),
                       AsIs(orig_tname),
                       AsIs(orig_tname),
                       AsIs(orig_tname)
                       ))
    
    